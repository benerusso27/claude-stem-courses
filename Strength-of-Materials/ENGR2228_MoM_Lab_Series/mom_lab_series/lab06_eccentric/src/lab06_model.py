"""Lab 6 physics in Python (SI base units: N, m, Pa). Independent re-implementation of what
lab06_simulation.html computes, by different methods wherever possible:
  * section properties by Green's theorem on polygons plus adaptive quadrature for curved parts
    (the page uses composite-rectangle formulas and cell grids);
  * stresses from the general (non-principal) form sigma = P/A + P [yP zP] S^-1 [y z]^T
    (the page uses Beer's Eq. 4.58 in principal axes, and a 3 x 3 equilibrium solve on a grid);
  * the kern as an intersection of half-planes (scipy HalfspaceIntersection)
    (the page uses antipoles of the hull edges, and bisection along rays);
  * the beam-column by scipy's collocation BVP solver (the page uses cosh/cos closed forms and
    finite differences);
  * the tube under combined loads by adaptive quadrature.

Beer 8e conventions: x along the member, y up, z completing a right-handed set (section views are
drawn looking along -x, so z points left). Tension positive. Eq. 4.58: sigma_x = P/A - Mz y/Iz + My z/Iy
in principal centroidal axes; a force P (tension +) through the point (yP, zP) gives My = P zP and
Mz = -P yP. Deflection y (or w) positive toward the load line in the beam-column.
"""
import math

import numpy as np
from scipy import integrate, optimize
from scipy.spatial import ConvexHull, HalfspaceIntersection


# ----------------------------------------------------------------------------- section integrals
def poly_integrals(verts):
    """Integrals over a simple polygon given as [(z, y), ...] (either orientation), about the origin:
    A, Sz = int z dA, Sy = int y dA, Jzz = int z^2 dA, Jyy = int y^2 dA, Jzy = int z y dA (Green's theorem)."""
    v = np.asarray(verts, float)
    x, y = v[:, 0], v[:, 1]
    x1, y1 = np.roll(x, -1), np.roll(y, -1)
    c = x * y1 - x1 * y
    out = dict(A=c.sum() / 2, Sz=((x + x1) * c).sum() / 6, Sy=((y + y1) * c).sum() / 6,
               Jzz=((x * x + x * x1 + x1 * x1) * c).sum() / 12, Jyy=((y * y + y * y1 + y1 * y1) * c).sum() / 12,
               Jzy=((x * y1 + 2 * x * y + 2 * x1 * y1 + x1 * y) * c).sum() / 24)
    if out["A"] < 0:
        out = {k: -val for k, val in out.items()}
    return out


def spandrel_integrals(z0, y0, r):
    """Root fillet of an angle whose vertical leg face is z = z0 (material toward +z) and whose horizontal leg
    top face is y = y0, the horizontal leg extending toward -z: the region z0 - r <= z <= z0, y0 <= y <= arc,
    outside the circle of radius r centered at (z0 - r, y0 + r). Adaptive quadrature (dblquad)."""
    if r <= 0:
        return dict(A=0.0, Sz=0.0, Sy=0.0, Jzz=0.0, Jyy=0.0, Jzy=0.0)
    top = lambda z: y0 + r - math.sqrt(max(r * r - (z - (z0 - r)) ** 2, 0.0))  # noqa: E731
    f = {"A": lambda y, z: 1.0, "Sz": lambda y, z: z, "Sy": lambda y, z: y, "Jzz": lambda y, z: z * z,
         "Jyy": lambda y, z: y * y, "Jzy": lambda y, z: z * y}
    return {k: integrate.dblquad(g, z0 - r, z0, lambda z: y0, top, epsabs=1e-22, epsrel=1e-10)[0] for k, g in f.items()}


def annulus_integrals(zc, yc, Ro, Ri):
    """Annulus (Ri = 0: disk) by polar quadrature."""
    f = {"A": lambda r, t: r, "Sz": lambda r, t: (zc + r * math.cos(t)) * r, "Sy": lambda r, t: (yc + r * math.sin(t)) * r,
         "Jzz": lambda r, t: (zc + r * math.cos(t)) ** 2 * r, "Jyy": lambda r, t: (yc + r * math.sin(t)) ** 2 * r,
         "Jzy": lambda r, t: (zc + r * math.cos(t)) * (yc + r * math.sin(t)) * r}
    return {k: integrate.dblquad(g, 0, 2 * math.pi, Ri, Ro, epsabs=1e-24, epsrel=1e-12)[0] for k, g in f.items()}


# ----------------------------------------------------------------------------- shapes
def rect(h, b):
    """Depth h along y, width b along z, centered on the origin."""
    P = [(-b / 2, -h / 2), (b / 2, -h / 2), (b / 2, h / 2), (-b / 2, h / 2)]
    return dict(kind="rect", polys=[P], spandrels=[], annuli=[], hull=P)


def angle(bV, bH, t, r=0.0):
    """Angle drawn as an "L" in Beer's section view (z to the left): heel at the origin, vertical leg bV along +y
    (outer face z = 0, material at -t <= z <= 0), horizontal leg bH along -z (outer face y = 0), thickness t,
    optional root fillet of radius r at the re-entrant corner (z, y) = (-t, t)."""
    P = [(0, 0), (0, bV), (-t, bV), (-t, t), (-bH, t), (-bH, 0)]
    hull = [(0, 0), (0, bV), (-t, bV), (-bH, t), (-bH, 0)]
    return dict(kind="angle", polys=[P], spandrels=[(-t, t, r)] if r > 0 else [], annuli=[], hull=hull)


def tee(B, H, tf, tw):
    """Flange B x tf on top, stem tw wide; bottom of the stem at y = 0, symmetric about z = 0."""
    P = [(-tw / 2, 0), (tw / 2, 0), (tw / 2, H - tf), (B / 2, H - tf), (B / 2, H), (-B / 2, H), (-B / 2, H - tf), (-tw / 2, H - tf)]
    hull = [(-tw / 2, 0), (tw / 2, 0), (B / 2, H - tf), (B / 2, H), (-B / 2, H), (-B / 2, H - tf)]
    return dict(kind="tee", polys=[P], spandrels=[], annuli=[], hull=hull)


def channel(B, H, tf, tw):
    """Web tw thick at z in [0, tw], flanges B wide extending toward +z, depth H."""
    P = [(0, 0), (B, 0), (B, tf), (tw, tf), (tw, H - tf), (B, H - tf), (B, H), (0, H)]
    hull = [(0, 0), (B, 0), (B, H), (0, H)]
    return dict(kind="channel", polys=[P], spandrels=[], annuli=[], hull=hull)


def zsec(B, H, tf, tw):
    """Z-section: web tw centered on z = 0; top flange extends toward +z, bottom flange toward -z."""
    a = tw / 2
    P = [(a - B, 0), (a, 0), (a, H - tf), (B - a, H - tf), (B - a, H), (-a, H), (-a, tf), (a - B, tf)]
    hull = [(a - B, 0), (a, 0), (B - a, H - tf), (B - a, H), (-a, H), (a - B, tf)]
    return dict(kind="zsec", polys=[P], spandrels=[], annuli=[], hull=hull)


def tube(Do, Di):
    n = 720
    hull = [(Do / 2 * math.cos(2 * math.pi * k / n), Do / 2 * math.sin(2 * math.pi * k / n)) for k in range(n)]
    return dict(kind="tube", polys=[], spandrels=[], annuli=[(0.0, 0.0, Do / 2, Di / 2)], hull=hull)


def props(sec):
    tot = dict(A=0.0, Sz=0.0, Sy=0.0, Jzz=0.0, Jyy=0.0, Jzy=0.0)
    parts = [poly_integrals(P) for P in sec["polys"]] + [spandrel_integrals(*s) for s in sec["spandrels"]] + \
            [annulus_integrals(*a) for a in sec["annuli"]]
    for p in parts:
        for k in tot:
            tot[k] += p[k]
    A = tot["A"]
    zc, yc = tot["Sz"] / A, tot["Sy"] / A
    Iy = tot["Jzz"] - A * zc * zc          # int z'^2 dA (about the centroidal y axis)
    Iz = tot["Jyy"] - A * yc * yc          # int y'^2 dA (about the centroidal z axis)
    Iyz = tot["Jzy"] - A * zc * yc         # int y'z' dA
    S = np.array([[Iz, Iyz], [Iyz, Iy]])   # order (y, z)
    w, V = np.linalg.eigh(S)
    # eigenvector of S for eigenvalue w_k is the direction of greatest/least spread; the moment of inertia
    # about the axis perpendicular to it equals w_k
    return dict(A=A, yc=yc, zc=zc, Iz=Iz, Iy=Iy, Iyz=Iyz, S=S, Imax=w[1], Imin=w[0], spread_max=V[:, 1], spread_min=V[:, 0])


def to_centroidal(pr, pts):
    return [(y - pr["yc"], z - pr["zc"]) for (z, y) in pts]


# ----------------------------------------------------------------------------- stresses
def stress_coeffs(pr, P, yP, zP, naive=False):
    """sigma = P/A + b y + c z (centroidal y, z). General form: [b c] = P S^-1 [yP zP]. naive=True ignores Iyz."""
    if naive:
        b, c = P * yP / pr["Iz"], P * zP / pr["Iy"]
    else:
        b, c = np.linalg.solve(pr["S"], P * np.array([yP, zP]))
    return P / pr["A"], float(b), float(c)


def stress(pr, P, yP, zP, y, z, naive=False):
    a, b, c = stress_coeffs(pr, P, yP, zP, naive)
    return a + b * y + c * z


def na_angle(pr, P, yP, zP):
    """Angle (rad) of the neutral axis with the z axis, in (-pi/2, pi/2]."""
    _, b, c = stress_coeffs(pr, P, yP, zP)
    return math.atan2(-c, b) if b != 0 else math.pi / 2


def kern(pr, hull_c):
    """Kern polygon (centroidal (y, z) vertices) as the intersection of the half-planes sigma(vertex) >= 0
    for a unit tension through the load point, one per hull vertex."""
    Sinv = np.linalg.inv(pr["S"])
    hs = []
    for (y, z) in hull_c:
        g = Sinv @ np.array([y, z])            # sigma/P = 1/A + g . (yP, zP)
        hs.append([-g[0], -g[1], -1.0 / pr["A"]])
    H = HalfspaceIntersection(np.array(hs), np.array([0.0, 0.0]))
    pts = H.intersections
    hull = ConvexHull(pts)
    return pts[hull.vertices], hull.volume  # 2-D: volume = area


def kern_radius_along(pr, hull_c, ang):
    """Distance from the centroid to the kern boundary along the direction (cos ang, sin ang) in the (y, z) plane:
    the largest lambda with sigma >= 0 at every hull vertex (root by brentq)."""
    d = np.array([math.cos(ang), math.sin(ang)])
    Sinv = np.linalg.inv(pr["S"])
    lam = math.inf
    for (y, z) in hull_c:
        g = float(d @ (Sinv @ np.array([y, z])))
        if g < 0:
            lam = min(lam, -1.0 / (pr["A"] * g))
    return lam


# ----------------------------------------------------------------------------- beam-column (eccentric axial load)
def beam_column(P, EI, L, a, e):
    """Bar of free length L between rigid end blocks; the load line is at distance e from the centroid at the pins,
    a distance a beyond each end of the free length. P > 0 tension, P < 0 compression.
    Returns C_mid = M_mid/(P e), C_end = M(at the ends of the free length)/(P e), w_mid/e and the shape function.
    w = displacement of the centroid toward the load line."""
    if P == 0:
        return dict(Cmid=1.0, Cend=1.0, wmid=0.0, w=lambda x: 0.0 * x, M=lambda x: 1.0 + 0.0 * x)
    k = math.sqrt(abs(P) / EI)
    u = k * L / 2
    if P > 0:
        C = 1.0 / (math.cosh(u) + k * a * math.sinh(u))
        shape = lambda x: np.cosh(k * (np.asarray(x) - L / 2))  # noqa: E731
    else:
        den = math.cos(u) - k * a * math.sin(u)
        if den <= 0:
            return dict(Cmid=math.inf, Cend=math.inf, wmid=-math.inf, w=None, M=None, buckled=True)
        C = 1.0 / den
        shape = lambda x: np.cos(k * (np.asarray(x) - L / 2))  # noqa: E731
    return dict(Cmid=C, Cend=C * float(shape(0.0)), wmid=1 - C, w=lambda x: e * (1 - C * shape(x)), M=lambda x: C * shape(x), buckled=False)


def beam_column_bvp(P, EI, L, a, e, n=401):
    """Same problem by collocation: EI w'' = P (w - e); w(0) - a w'(0) = 0, w(L) + a w'(L) = 0."""
    x = np.linspace(0, L, n)

    def f(xx, Y):
        return np.vstack([Y[1], P * (Y[0] - e) / EI])

    def bc(ya, yb):
        return np.array([ya[0] - a * ya[1], yb[0] + a * yb[1]])

    sol = integrate.solve_bvp(f, bc, x, np.zeros((2, n)), tol=1e-10, max_nodes=200000)
    if not sol.success:
        raise RuntimeError(sol.message)
    wm = float(sol.sol(L / 2)[0])
    w0 = float(sol.sol(0.0)[0])
    return dict(Cmid=(e - wm) / e, Cend=(e - w0) / e, wmid=wm / e, sol=sol)


def euler_load_blocks(EI, L, a):
    """Buckling load of the bar with rigid end blocks (pinned at the load points): tan u = 1/(k a), u = kL/2."""
    if a == 0:
        return math.pi ** 2 * EI / L ** 2
    g = lambda u: math.cos(u) - (2 * a / L) * u * math.sin(u)  # noqa: E731
    u = optimize.brentq(g, 1e-9, math.pi / 2)
    return EI * (2 * u / L) ** 2


# ----------------------------------------------------------------------------- tube (or solid shaft) under combined loads
def tube_loads(F, Lb, a_lever, P=0.0):
    """Cantilever tube; a downward force F at the end of a lever arm a_lever, at distance Lb from the section.
    Internal forces on the section (Beer 8.3 free body of the outer part): bending moment about z of magnitude F Lb
    (hogging: tension on top), torque F a_lever, shear F, axial P."""
    return dict(M=F * Lb, T=F * a_lever, V=F, P=P)


def tube_point_stress(Do, Di, loads, phi):
    """Tube (Di > 0). Point on the outer surface at angle phi from the top (phi = 0 top, pi/2 the side). Closed forms:
    sigma = P/A + M c cos(phi)/I (tension on top for the hogging cantilever moment); tau_T = T c/J;
    tau_V = V Q(phi)/(I t) with Q = (ro^3 - ri^3) sin(phi)/3 for the wall from the top to the cut, t = ro - ri."""
    ro, ri = Do / 2, Di / 2
    A = math.pi * (ro ** 2 - ri ** 2)
    I = math.pi * (ro ** 4 - ri ** 4) / 4
    J = 2 * I
    sig = loads["P"] / A + loads["M"] * ro * math.cos(phi) / I
    tT = loads["T"] * ro / J
    tV = loads["V"] * (ro ** 3 - ri ** 3) * math.sin(phi) / 3 / (I * (ro - ri))   # signed: + on the side 0 < phi < pi
    return dict(sigma=sig, tauT=tT, tauV=tV, A=A, I=I, J=J)


def tube_quadrature(Do, Di, phi):
    """A, I, J and Q(phi) of the wall between the top and a radial cut at phi, by quadrature."""
    ro, ri = Do / 2, Di / 2
    A = integrate.dblquad(lambda r, t: r, 0, 2 * math.pi, ri, ro)[0]
    I = integrate.dblquad(lambda r, t: (r * math.cos(t)) ** 2 * r, 0, 2 * math.pi, ri, ro)[0]
    J = integrate.dblquad(lambda r, t: r ** 3, 0, 2 * math.pi, ri, ro)[0]
    Q = integrate.dblquad(lambda r, t: r * math.cos(t) * r, 0, phi, ri, ro)[0]
    return dict(A=A, I=I, J=J, Q=Q)
