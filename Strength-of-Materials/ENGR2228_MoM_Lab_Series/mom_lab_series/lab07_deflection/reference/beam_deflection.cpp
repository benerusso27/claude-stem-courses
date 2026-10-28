// ============================================================================
//  beam_deflection.cpp  --  Beam Deflection Explorer (Strength of Materials)
// ============================================================================
//
//  The deflection table in the back of a Strength of Materials book looks like
//  dozens of unrelated formulas. It isn't. Every row is the SAME equation,
//
//                      E I y''''(x) = w(x)
//
//  integrated four times, with the four constants fixed by the supports.
//  This program makes that visible:
//
//    1. Tour       Builds every classic table case, solves it numerically
//                  (finite elements), and prints the table formula next to
//                  the simulation so you can watch them agree.
//    2. Detail     One case up close: sketch, reactions, shear, moment, slope
//                  and deflected shape as terminal plots, plus a CSV file.
//    3. Custom     Any supports, any mix of point loads, uniform/triangular
//                  loads and couples -- including beams the table can't do
//                  (indeterminate beams, overhangs, partial loads).
//    4. Superpose  How to combine table rows correctly.
//    5. Theory     The derivation behind the table, step by step.
//
//  Build:   g++ -std=c++17 -O2 -Wall -o beam beam_deflection.cpp
//  Run:     ./beam                 interactive menu
//           ./beam --tour          whole table, formula vs simulation
//           ./beam --case 8        one table case in detail (1-15)
//           ./beam --superpose     superposition demo
//           ./beam --theory        the one equation behind the table
//           add --us to any of these for US units (kip, ft, ksi, in^4)
//
//  Want real graphics? beam_gui.cpp is a live raylib window that reuses this
//  file's solver. Keep both files in the same folder; see its header to build.
//
//  SIGN CONVENTION (used everywhere below)
//    x       distance from the LEFT end of the beam
//    y       deflection, POSITIVE DOWNWARD (a sagging beam has y > 0)
//    theta   slope dy/dx (positive = beam heading downward to the right)
//    loads   forces positive DOWNWARD, couples positive CLOCKWISE
//    V, M    textbook convention: M > 0 is sagging ("smile"), dM/dx = V,
//            dV/dx = -w.  With y downward:  E I y'' = -M  and  E I y''' = -V.
//
//  MODEL: Euler-Bernoulli beam -- slender, small deflections, linear elastic,
//         constant E I, shear deformation ignored. Same assumptions as the table.
// ============================================================================

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace {

// ============================================================================
//  0. Small helpers: number formatting and keyboard input
// ============================================================================
std::string fmt(double v, int sig = 5) {
    if (std::fabs(v) < 1e-300) v = 0.0;
    char buf[64];
    std::snprintf(buf, sizeof buf, "%.*g", sig, v);
    std::string s = buf;
    if (s == "-0") s = "0";
    return s;
}

// 5 significant figures, keeping trailing zeros (6 -> "6.0000") so columns line up
std::string num(double v) {
    char buf[64];
    std::snprintf(buf, sizeof buf, "%#.5g", std::fabs(v) < 1e-300 ? 0.0 : v);
    return buf;
}

std::string fix(double v, int decimals = 3) {
    char buf[64];
    std::snprintf(buf, sizeof buf, "%.*f", decimals, v);
    std::string s = buf;
    if (s[0] == '-' && s.find_first_not_of("-0.") == std::string::npos) s.erase(0, 1);  // "-0.000" -> "0.000"
    return s;
}

std::string sci(double v) {
    char buf[32];
    std::snprintf(buf, sizeof buf, "%.1e", v);
    return buf;
}

std::string padR(const std::string& s, size_t w) { return s.size() >= w ? s : s + std::string(w - s.size(), ' '); }
std::string padL(const std::string& s, size_t w) { return s.size() >= w ? s : std::string(w - s.size(), ' ') + s; }

std::string trim(const std::string& s) {
    const size_t a = s.find_first_not_of(" \t\r\n");
    if (a == std::string::npos) return "";
    const size_t b = s.find_last_not_of(" \t\r\n");
    return s.substr(a, b - a + 1);
}

std::string readLineOrQuit() {
    std::string s;
    if (!std::getline(std::cin, s)) { std::cout << "\n"; std::exit(0); }
    return trim(s);
}

double askDouble(const std::string& prompt, double def) {
    for (;;) {
        std::cout << "  " << prompt << " [" << fmt(def, 6) << "]: " << std::flush;
        const std::string s = readLineOrQuit();
        if (s.empty()) return def;
        char* end = nullptr;
        const double v = std::strtod(s.c_str(), &end);
        if (end != s.c_str() && trim(end).empty() && std::isfinite(v)) return v;
        std::cout << "    Please type a number, or just press Enter to keep the default.\n";
    }
}

double askPositive(const std::string& prompt, double def) {
    for (;;) {
        const double v = askDouble(prompt, def);
        if (v > 0) return v;
        std::cout << "    This value has to be greater than zero.\n";
    }
}

int askInt(const std::string& prompt, int def, int lo, int hi) {
    for (;;) {
        const double v = askDouble(prompt, def);
        if (v == std::floor(v) && v >= lo && v <= hi) return static_cast<int>(v);
        std::cout << "    Please choose a whole number from " << lo << " to " << hi << ".\n";
    }
}

// ============================================================================
//  1. Units
// ============================================================================
//  Internally everything is in a consistent base set (SI: N, m, Pa;
//  US: lb, in, psi). k* = how many base units are in one display unit, so
//  internal = typed * k   and   display = internal / k.
struct Units {
    bool si;
    std::string len, force, dist, moment, modulus, inertia, defl, stress, depth;
    double kLen, kForce, kDist, kMoment, kModulus, kInertia, kDefl, kStress, kDepth;
};

Units siUnits() {
    return {true, "m", "kN", "kN/m", "kN*m", "GPa", "mm^4", "mm", "MPa", "mm",
            1.0, 1e3, 1e3, 1e3, 1e9, 1e-12, 1e-3, 1e6, 1e-3};
}
Units usUnits() {
    return {false, "ft", "kip", "kip/ft", "kip*ft", "ksi", "in^4", "in", "ksi", "in",
            12.0, 1e3, 1e3 / 12.0, 12e3, 1e3, 1.0, 1.0, 1e3, 1.0};
}
std::string unitsName(const Units& u) { return u.si ? "SI: kN, m, GPa, mm^4" : "US: kip, ft, ksi, in^4"; }

// ============================================================================
//  2. The beam model
// ============================================================================
enum class SupportType { Pin, Roller, Fixed };  // pin and roller both stop vertical motion only
struct Support { SupportType type; double x; };

enum class LoadType { Point, Distributed, Couple };
struct Load {
    LoadType type;
    double a, b;    // Point/Couple act at x = a. Distributed acts from x = a to x = b.
    double q1, q2;  // Point: P = q1 (down +). Couple: C = q1 (clockwise +).
                    // Distributed: intensity q1 at x = a and q2 at x = b (down +), linear between.
};
Load pointLoad(double P, double x) { return {LoadType::Point, x, x, P, 0.0}; }
Load coupleLoad(double C, double x) { return {LoadType::Couple, x, x, C, 0.0}; }
Load distLoad(double wa, double wb, double a, double b) { return {LoadType::Distributed, a, b, wa, wb}; }

struct Beam {
    double L = 1.0, E = 1.0, I = 1.0;
    std::vector<Support> supports;
    std::vector<Load> loads;
    double EI() const { return E * I; }
};

const SupportType FIX = SupportType::Fixed, PIN = SupportType::Pin, ROL = SupportType::Roller;

// Intensity of one distributed load at x (zero outside its span)
double intensity(const Load& ld, double x) {
    if (ld.type != LoadType::Distributed || x < ld.a || x > ld.b || ld.b <= ld.a) return 0.0;
    return ld.q1 + (ld.q2 - ld.q1) * (x - ld.a) / (ld.b - ld.a);
}
double totalIntensity(const Beam& bm, double x) {
    double q = 0.0;
    for (const auto& ld : bm.loads) q += intensity(ld, x);
    return q;
}

// For the part of a distributed load lying LEFT of a cut at x:
//   F  = its resultant force (down +)
//   Mx = its moment about the cut, i.e. integral of w(s) (x - s) ds
void distLeftOf(const Load& ld, double x, double& F, double& Mx) {
    F = Mx = 0.0;
    if (ld.type != LoadType::Distributed || x <= ld.a) return;
    const double T = std::min(x, ld.b) - ld.a;  // loaded length left of the cut
    const double D = x - ld.a;                  // distance from load start to the cut
    const double k = (ld.q2 - ld.q1) / (ld.b - ld.a);
    F = ld.q1 * T + k * T * T / 2.0;
    Mx = ld.q1 * (D * T - T * T / 2.0) + k * (D * T * T / 2.0 - T * T * T / 3.0);
}

// ============================================================================
//  3. Finite element solver
// ============================================================================
//  The beam is chopped into short elements. Each node has two unknowns:
//  deflection y and slope theta. Inside an element the deflection is the cubic
//  that matches y and theta at both ends (Hermite interpolation) -- exactly the
//  shape an unloaded beam segment takes, because E I y'''' = 0 gives a cubic.
//  Element stiffness matrix (h = element length):
//
//              E I  [  12    6h   -12    6h  ]
//      k_e =  ----- [  6h   4h^2  -6h   2h^2 ]
//              h^3  [ -12   -6h    12   -6h  ]
//                   [  6h   2h^2  -6h   4h^2 ]
//
//  Assemble K u = F, lock the restrained DOFs, solve. For a uniform
//  Euler-Bernoulli beam this gives the EXACT nodal deflections, which is why
//  the simulation matches the table to round-off.

struct Reaction { double x; SupportType type; double F_up; double M_cw; };

struct Solution {
    bool ok = false;
    std::string error;
    std::vector<double> xn, yn, tn;  // node positions, deflection (down +), slope
    std::vector<Reaction> reactions;
};

void sortUnique(std::vector<double>& v, double tol) {
    std::sort(v.begin(), v.end());
    std::vector<double> out;
    for (double x : v)
        if (out.empty() || x - out.back() > tol) out.push_back(x);
    v.swap(out);
}

int nearestNode(const std::vector<double>& xn, double x) {
    const int i = static_cast<int>(std::lower_bound(xn.begin(), xn.end(), x) - xn.begin());
    if (i >= static_cast<int>(xn.size())) return static_cast<int>(xn.size()) - 1;
    if (i > 0 && std::fabs(xn[i - 1] - x) < std::fabs(xn[i] - x)) return i - 1;
    return i;
}

// Cubic Hermite shape functions on an element of length h, xi in [0,1].
// N[] gives y from (y1, theta1, y2, theta2); dN[] is d/dx (gives the slope).
void hermite(double xi, double h, double N[4], double dN[4]) {
    const double xi2 = xi * xi, xi3 = xi2 * xi;
    N[0] = 1 - 3 * xi2 + 2 * xi3;
    N[1] = h * (xi - 2 * xi2 + xi3);
    N[2] = 3 * xi2 - 2 * xi3;
    N[3] = h * (-xi2 + xi3);
    dN[0] = (-6 * xi + 6 * xi2) / h;
    dN[1] = 1 - 4 * xi + 3 * xi2;
    dN[2] = (6 * xi - 6 * xi2) / h;
    dN[3] = -2 * xi + 3 * xi2;
}

// A beam with no axial load has two rigid-body motions: sliding up/down and
// rotating. The supports must stop both.
std::string stabilityProblem(const Beam& bm) {
    if (bm.supports.empty()) return "The beam has no supports, so nothing holds it up.";
    bool fixed = false;
    double lo = 1e300, hi = -1e300;
    for (const auto& s : bm.supports) {
        if (s.type == FIX) fixed = true;
        lo = std::min(lo, s.x);
        hi = std::max(hi, s.x);
    }
    if (!fixed && hi - lo < 1e-9 * bm.L)
        return "A single pin or roller can't stop the beam from rotating about it. "
               "Add a second support or make one fixed.";
    return "";
}

// Mesh: ~nElem equal elements, plus a node exactly at every support, every
// concentrated load and every start/end of a distributed load.
std::vector<double> buildMesh(const Beam& bm, int nElem) {
    std::vector<double> keys = {0.0, bm.L};
    for (const auto& s : bm.supports) keys.push_back(s.x);
    for (const auto& ld : bm.loads) {
        keys.push_back(ld.a);
        if (ld.type == LoadType::Distributed) keys.push_back(ld.b);
    }
    for (double& k : keys) k = std::clamp(k, 0.0, bm.L);
    sortUnique(keys, 1e-12 * bm.L);

    std::vector<double> nodes = keys;
    const double h = bm.L / nElem;
    for (int i = 1; i < nElem; ++i) {
        const double x = i * h;
        bool tooClose = false;
        for (double k : keys)
            if (std::fabs(x - k) < 0.3 * h) { tooClose = true; break; }
        if (!tooClose) nodes.push_back(x);
    }
    sortUnique(nodes, 1e-12 * bm.L);
    return nodes;
}

Solution solveBeam(const Beam& bm, int nElem = 120) {
    Solution sol;
    sol.error = stabilityProblem(bm);
    if (!sol.error.empty()) return sol;

    const double EI = bm.EI();
    sol.xn = buildMesh(bm, nElem);
    const int nn = static_cast<int>(sol.xn.size());
    const int nd = 2 * nn;  // unknowns: y and theta at every node
    std::vector<double> K(static_cast<size_t>(nd) * nd, 0.0), F(nd, 0.0);
    auto Kij = [&](int i, int j) -> double& { return K[static_cast<size_t>(i) * nd + j]; };

    // 3-point Gauss quadrature on [0,1]: exact for the polynomials that appear here
    const double gx[3] = {0.5 - 0.5 * std::sqrt(0.6), 0.5, 0.5 + 0.5 * std::sqrt(0.6)};
    const double gw[3] = {5.0 / 18.0, 8.0 / 18.0, 5.0 / 18.0};

    for (int e = 0; e + 1 < nn; ++e) {
        const double h = sol.xn[e + 1] - sol.xn[e];
        const double c = EI / (h * h * h);
        const double ke[4][4] = {{12 * c, 6 * h * c, -12 * c, 6 * h * c},
                                 {6 * h * c, 4 * h * h * c, -6 * h * c, 2 * h * h * c},
                                 {-12 * c, -6 * h * c, 12 * c, -6 * h * c},
                                 {6 * h * c, 2 * h * h * c, -6 * h * c, 4 * h * h * c}};
        const int dof[4] = {2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3};
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j) Kij(dof[i], dof[j]) += ke[i][j];

        // Distributed load -> equivalent nodal forces and moments ("consistent loads")
        for (int g = 0; g < 3; ++g) {
            const double q = totalIntensity(bm, sol.xn[e] + gx[g] * h);
            if (q == 0.0) continue;
            double N[4], dN[4];
            hermite(gx[g], h, N, dN);
            for (int i = 0; i < 4; ++i) F[dof[i]] += gw[g] * h * N[i] * q;
        }
    }
    for (const auto& ld : bm.loads) {
        const int n = nearestNode(sol.xn, ld.a);
        if (ld.type == LoadType::Point) F[2 * n] += ld.q1;       // force works through y
        if (ld.type == LoadType::Couple) F[2 * n + 1] += ld.q1;  // couple works through theta
    }

    // Supports: pin/roller lock y; fixed locks y and theta
    std::vector<int> locked;
    for (const auto& s : bm.supports) {
        const int n = nearestNode(sol.xn, s.x);
        locked.push_back(2 * n);
        if (s.type == FIX) locked.push_back(2 * n + 1);
    }
    std::sort(locked.begin(), locked.end());
    locked.erase(std::unique(locked.begin(), locked.end()), locked.end());

    // Keep the original equations of the locked DOFs: they give the reactions later
    std::vector<std::vector<double>> origRow;
    std::vector<double> origF;
    for (int d : locked) {
        origRow.emplace_back(K.begin() + static_cast<long>(d) * nd, K.begin() + static_cast<long>(d + 1) * nd);
        origF.push_back(F[d]);
    }
    for (size_t k = 0; k < locked.size(); ++k) {
        const int d = locked[k];
        for (int j = 0; j < nd; ++j) { Kij(d, j) = 0.0; Kij(j, d) = 0.0; }
        Kij(d, d) = origRow[k][d];  // keeps the matrix well scaled; forces u[d] = 0
        F[d] = 0.0;
    }

    // Gaussian elimination. K is banded (each DOF only couples to DOFs at most
    // 3 away), so elimination only has to touch the band: O(n) work.
    const int hb = 3;
    double maxDiag = 0.0;
    for (int i = 0; i < nd; ++i) maxDiag = std::max(maxDiag, std::fabs(Kij(i, i)));
    for (int k = 0; k < nd; ++k) {
        const double piv = Kij(k, k);
        if (std::fabs(piv) < 1e-12 * maxDiag) {
            sol.error = "The supports don't hold the beam in place (the stiffness matrix is singular).";
            return sol;
        }
        const int iEnd = std::min(nd - 1, k + hb);
        for (int i = k + 1; i <= iEnd; ++i) {
            const double m = Kij(i, k) / piv;
            if (m == 0.0) continue;
            for (int j = k; j <= iEnd; ++j) Kij(i, j) -= m * Kij(k, j);
            F[i] -= m * F[k];
        }
    }
    std::vector<double> u(nd, 0.0);
    for (int i = nd - 1; i >= 0; --i) {
        double s = F[i];
        for (int j = i + 1; j <= std::min(nd - 1, i + hb); ++j) s -= Kij(i, j) * u[j];
        u[i] = s / Kij(i, i);
    }

    sol.yn.resize(nn);
    sol.tn.resize(nn);
    for (int n = 0; n < nn; ++n) { sol.yn[n] = u[2 * n]; sol.tn[n] = u[2 * n + 1]; }

    // Reaction = what the support must supply = (K u - F) in the original equation
    std::map<int, double> R;
    for (size_t k = 0; k < locked.size(); ++k) {
        double s = -origF[k];
        for (int j = 0; j < nd; ++j) s += origRow[k][j] * u[j];
        R[locked[k]] = s;
    }
    std::set<int> used;
    for (const auto& s : bm.supports) {
        const int n = nearestNode(sol.xn, s.x);
        Reaction r{sol.xn[n], s.type, 0.0, 0.0};
        if (!used.count(2 * n)) { r.F_up = -R[2 * n]; used.insert(2 * n); }  // R is down +, report up +
        if (s.type == FIX && !used.count(2 * n + 1)) { r.M_cw = R[2 * n + 1]; used.insert(2 * n + 1); }
        sol.reactions.push_back(r);
    }
    sol.ok = true;
    return sol;
}

// Deflection (and optionally slope) anywhere, by Hermite interpolation
double deflectionAt(const Solution& sol, double x, double* slope = nullptr) {
    const auto& xn = sol.xn;
    int e = static_cast<int>(std::upper_bound(xn.begin(), xn.end(), x) - xn.begin()) - 1;
    e = std::clamp(e, 0, static_cast<int>(xn.size()) - 2);
    const double h = xn[e + 1] - xn[e];
    double N[4], dN[4];
    hermite((x - xn[e]) / h, h, N, dN);
    const double d[4] = {sol.yn[e], sol.tn[e], sol.yn[e + 1], sol.tn[e + 1]};
    double y = 0.0, t = 0.0;
    for (int i = 0; i < 4; ++i) { y += N[i] * d[i]; t += dN[i] * d[i]; }
    if (slope) *slope = t;
    return y;
}

// ============================================================================
//  4. Shear and moment by statics (free body of everything LEFT of the cut)
// ============================================================================
//  V(x) = sum of upward forces left of x
//  M(x) = sum of their moments about the cut (sagging +) + clockwise couples
void internalForces(const Beam& bm, const Solution& sol, double x, double& V, double& M) {
    V = M = 0.0;
    for (const auto& r : sol.reactions)
        if (r.x < x) { V += r.F_up; M += r.F_up * (x - r.x) + r.M_cw; }
    for (const auto& ld : bm.loads) {
        if (ld.type == LoadType::Point && ld.a < x) { V -= ld.q1; M -= ld.q1 * (x - ld.a); }
        if (ld.type == LoadType::Couple && ld.a < x) M += ld.q1;
        if (ld.type == LoadType::Distributed) {
            double Fd, Md;
            distLeftOf(ld, x, Fd, Md);
            V -= Fd;
            M -= Md;
        }
    }
}

// Overall equilibrium (should be ~0): forces up +, moments about x = 0 clockwise +
void equilibrium(const Beam& bm, const Solution& sol, double& sumF, double& sumM) {
    sumF = sumM = 0.0;
    for (const auto& r : sol.reactions) { sumF += r.F_up; sumM += -r.F_up * r.x + r.M_cw; }
    for (const auto& ld : bm.loads) {
        if (ld.type == LoadType::Point) { sumF -= ld.q1; sumM += ld.q1 * ld.a; }
        if (ld.type == LoadType::Couple) sumM += ld.q1;
        if (ld.type == LoadType::Distributed) {
            double Fd, Md;
            distLeftOf(ld, bm.L, Fd, Md);  // Md is the moment about x = L
            sumF -= Fd;
            sumM += Fd * bm.L - Md;
        }
    }
}

// ============================================================================
//  5. Sampling the solution along the beam
// ============================================================================
struct Curves { std::vector<double> x, w, V, M, th, y; };

Curves sampleBeam(const Beam& bm, const Solution& sol, int perElem = 6) {
    std::vector<double> xs;
    for (size_t e = 0; e + 1 < sol.xn.size(); ++e)
        for (int k = 0; k < perElem; ++k)
            xs.push_back(sol.xn[e] + (sol.xn[e + 1] - sol.xn[e]) * k / perElem);
    xs.push_back(bm.L);
    // sample just either side of every jump in V or M so the diagrams show the step
    const double eps = 1e-9 * bm.L;
    auto addJump = [&](double p) {
        if (p - eps > 0) xs.push_back(p - eps);
        if (p + eps < bm.L) xs.push_back(p + eps);
    };
    for (const auto& s : bm.supports) addJump(s.x);
    for (const auto& ld : bm.loads)
        if (ld.type != LoadType::Distributed) addJump(ld.a);
    sortUnique(xs, 1e-12 * bm.L);

    // size of the loading, used to wipe out round-off noise (e.g. 1e-12 kN of "shear")
    double Fs = 0.0;
    for (const auto& ld : bm.loads) {
        if (ld.type == LoadType::Point) Fs += std::fabs(ld.q1);
        if (ld.type == LoadType::Couple) Fs += std::fabs(ld.q1) / bm.L;
        if (ld.type == LoadType::Distributed) Fs += (std::fabs(ld.q1) + std::fabs(ld.q2)) / 2 * (ld.b - ld.a);
    }

    Curves cv;
    for (double x : xs) {
        double th, V, M;
        const double y = deflectionAt(sol, x, &th);
        internalForces(bm, sol, x, V, M);
        if (std::fabs(V) < 1e-9 * Fs) V = 0.0;
        if (std::fabs(M) < 1e-9 * Fs * bm.L) M = 0.0;
        cv.x.push_back(x);
        cv.w.push_back(totalIntensity(bm, x));
        cv.V.push_back(V);
        cv.M.push_back(M);
        cv.th.push_back(th);
        cv.y.push_back(y);
    }
    return cv;
}

struct Peak { double x, y; };

// Largest |deflection|: best sample, then polished with a golden-section search
Peak maxDeflection(const Solution& sol, const Curves& cv) {
    size_t i = 0;
    for (size_t j = 1; j < cv.y.size(); ++j)
        if (std::fabs(cv.y[j]) > std::fabs(cv.y[i])) i = j;
    double a = cv.x[i > 0 ? i - 1 : 0], b = cv.x[std::min(i + 1, cv.x.size() - 1)];
    auto f = [&](double x) { return std::fabs(deflectionAt(sol, x)); };
    const double g = (std::sqrt(5.0) - 1.0) / 2.0;
    double c = b - g * (b - a), d = a + g * (b - a), fc = f(c), fd = f(d);
    for (int it = 0; it < 80; ++it) {
        if (fc > fd) { b = d; d = c; fd = fc; c = b - g * (b - a); fc = f(c); }
        else         { a = c; c = d; fc = fd; d = a + g * (b - a); fd = f(d); }
    }
    const double xm = 0.5 * (a + b), ym = deflectionAt(sol, xm);
    if (std::fabs(ym) < std::fabs(cv.y[i])) return {cv.x[i], cv.y[i]};
    return {xm, ym};
}

// ============================================================================
//  6. Terminal graphics: beam sketch and plots
// ============================================================================
std::string loadText(const Load& ld, const Units& u) {
    const std::string at = fix(ld.a / u.kLen) + " " + u.len;
    if (ld.type == LoadType::Point)
        return "point load P = " + fmt(std::fabs(ld.q1) / u.kForce) + " " + u.force +
               (ld.q1 >= 0 ? " down" : " up") + " at x = " + at;
    if (ld.type == LoadType::Couple)
        return "couple M0 = " + fmt(std::fabs(ld.q1) / u.kMoment) + " " + u.moment +
               (ld.q1 >= 0 ? " clockwise" : " counterclockwise") + " at x = " + at;
    const std::string mag = (ld.q1 == ld.q2)
        ? "uniform load w = " + fmt(ld.q1 / u.kDist)
        : "varying load w = " + fmt(ld.q1 / u.kDist) + " -> " + fmt(ld.q2 / u.kDist);
    return mag + " " + u.dist + " (down +) from x = " + at + " to " + fix(ld.b / u.kLen) + " " + u.len;
}

std::string supportName(SupportType t) { return t == FIX ? "fixed" : t == PIN ? "pin" : "roller"; }

void drawBeam(const Beam& bm, const Units& u) {
    const int W = 60, off = 3, tot = W + 2 * off;
    auto col = [&](double x) { return off + static_cast<int>(std::lround(x / bm.L * (W - 1))); };
    std::string rNum(tot, ' '), rArr(tot, ' '), rBeam(tot, ' '), rSup(tot, ' '), rAx(tot, ' ');
    for (int c = off; c < off + W; ++c) rBeam[c] = '=';

    for (size_t k = 0; k < bm.loads.size(); ++k) {
        const Load& ld = bm.loads[k];
        const char id = k < 9 ? static_cast<char>('1' + k) : static_cast<char>('A' + (k - 9));
        if (ld.type == LoadType::Point) {
            const int c = col(ld.a);
            rArr[c] = ld.q1 >= 0 ? 'v' : '^';
            rNum[c] = id;
        } else if (ld.type == LoadType::Couple) {
            const int c = col(ld.a);
            rArr[c] = '@';
            rNum[c] = id;
        } else {
            const int c0 = col(ld.a), c1 = col(ld.b);
            for (int c = c0; c <= c1; c += 2) rArr[c] = (ld.q1 + ld.q2 >= 0) ? 'v' : '^';
            rNum[(c0 + c1) / 2] = id;
        }
    }
    for (const auto& s : bm.supports) {
        const int c = col(s.x);
        if (s.type == PIN) rSup[c] = '^';
        else if (s.type == ROL) rSup[c] = 'o';
        else if (s.x < 1e-9 * bm.L) { for (int k : {off - 2, off - 1}) rArr[k] = rBeam[k] = rSup[k] = '#'; }
        else if (s.x > bm.L * (1 - 1e-9)) { for (int k : {off + W, off + W + 1}) rArr[k] = rBeam[k] = rSup[k] = '#'; }
        else rSup[c] = '#';
    }
    rAx[off] = '0';
    const std::string lab = "x = " + fmt(bm.L / u.kLen) + " " + u.len;
    for (size_t i = 0; i < lab.size(); ++i) rAx[off + W - lab.size() + i] = lab[i];

    std::cout << "  " << rNum << "\n  " << rArr << "\n  " << rBeam << "\n  " << rSup << "\n  " << rAx << "\n";
    std::cout << "  Supports: ";
    for (size_t k = 0; k < bm.supports.size(); ++k)
        std::cout << (k ? ", " : "") << supportName(bm.supports[k].type) << " at x = "
                  << fix(bm.supports[k].x / u.kLen) << " " << u.len;
    std::cout << "\n  Loads:\n";
    for (size_t k = 0; k < bm.loads.size(); ++k) {
        const char id = k < 9 ? static_cast<char>('1' + k) : static_cast<char>('A' + (k - 9));
        std::cout << "    " << id << "  " << loadText(bm.loads[k], u) << "\n";
    }
    std::cout << "  Beam: L = " << fmt(bm.L / u.kLen) << " " << u.len << ", E = " << fmt(bm.E / u.kModulus)
              << " " << u.modulus << ", I = " << fmt(bm.I / u.kInertia, 6) << " " << u.inertia << "\n";
}

// ASCII plot of one quantity along the beam. fill = shade between curve and
// axis (shear/moment diagrams); flip = draw downward values below the axis.
void plot(const std::string& title, const Curves& cv, const std::vector<double>& val, double L,
          const Units& u, double scale, const std::string& unit, bool fill, bool flip) {
    const int W = 60, H = 11;
    const double half = L / (2.0 * (W - 1));
    std::vector<double> colv(W, 0.0);
    for (int c = 0; c < W; ++c) {
        const double xc = L * c / (W - 1);
        bool found = false;
        double best = 0.0;
        for (size_t i = 0; i < cv.x.size(); ++i) {
            if (std::fabs(cv.x[i] - xc) > half) continue;
            const double v = val[i] / scale;
            if (!found || std::fabs(v) > std::fabs(best)) { best = v; found = true; }
        }
        colv[c] = flip ? -best : best;
    }
    double lo = 0.0, hi = 0.0;
    for (double v : colv) { lo = std::min(lo, v); hi = std::max(hi, v); }
    if (hi == lo) {
        std::cout << "\n  " << title << ": zero everywhere\n";
        return;
    }
    auto rowOf = [&](double v) { return static_cast<int>(std::lround((hi - v) / (hi - lo) * (H - 1))); };
    std::vector<std::string> grid(H, std::string(W, ' '));
    const int z = rowOf(0.0);
    for (int c = 0; c < W; ++c) grid[z][c] = '-';
    for (int c = 0; c < W; ++c) {
        const int r = rowOf(colv[c]);
        if (fill)
            for (int k = std::min(r, z) + 1; k < std::max(r, z); ++k) grid[k][c] = ':';
        grid[r][c] = '*';
    }
    const double sgn = flip ? -1.0 : 1.0;
    std::cout << "\n  " << title << "   [" << unit << "]\n";
    for (int r = 0; r < H; ++r) {
        std::string lab;
        if (r == 0) lab = fmt(sgn * hi, 4);
        else if (r == H - 1) lab = fmt(sgn * lo, 4);
        else if (r == z) lab = "0";
        std::cout << padL(lab, 11) << " |" << grid[r] << "\n";
    }
    std::string axis(W, ' ');
    auto put = [&](const std::string& s, int at) {
        for (size_t i = 0; i < s.size(); ++i)
            if (at + static_cast<int>(i) >= 0 && at + static_cast<int>(i) < W) axis[at + i] = s[i];
    };
    const std::string mid = fmt(L / 2 / u.kLen, 4), end = fmt(L / u.kLen, 4) + " " + u.len;
    put("0", 0);
    put(mid, (W - static_cast<int>(mid.size())) / 2);
    put(end, W - static_cast<int>(end.size()));
    std::cout << std::string(13, ' ') << axis << "\n";
}

void plots(const Beam& bm, const Curves& cv, const Units& u) {
    plot("Shear force V(x)", cv, cv.V, bm.L, u, u.kForce, u.force, true, false);
    plot("Bending moment M(x)   (+ = sagging)", cv, cv.M, bm.L, u, u.kMoment, u.moment, true, false);
    plot("Slope theta(x) = dy/dx", cv, cv.th, bm.L, u, 1.0, "rad", false, false);
    plot("Deflected shape (drawn as it really bends; values: + = down)", cv, cv.y, bm.L, u, u.kDefl, u.defl,
         false, true);
}

// ============================================================================
//  7. Results report and CSV export
// ============================================================================
void report(const Beam& bm, const Solution& sol, const Curves& cv, const Units& u, double cDepth,
            bool showDeflection) {
    std::cout << "\n  RESULTS\n";
    if (showDeflection) {
        const Peak pk = maxDeflection(sol, cv);
        std::cout << "    Max deflection   " << num(std::fabs(pk.y) / u.kDefl) << " " << u.defl
                  << (pk.y >= 0 ? " down" : " up") << " at x = " << fix(pk.x / u.kLen) << " " << u.len;
        if (pk.y != 0.0) std::cout << "   (L/" << fmt(bm.L / std::fabs(pk.y), 4) << ")";
        std::cout << "\n";
    }
    const double t0 = cv.th.front(), t1 = cv.th.back();
    const double deg = 180.0 / 3.14159265358979323846;
    std::cout << "    End slopes       left " << fmt(t0, 4) << " rad (" << fix(t0 * deg) << " deg),  right "
              << fmt(t1, 4) << " rad (" << fix(t1 * deg) << " deg)\n";

    std::cout << "    Reactions\n";
    for (const auto& r : sol.reactions) {
        std::cout << "      " << padR(supportName(r.type) + " at x = " + fix(r.x / u.kLen) + " " + u.len, 26)
                  << "R = " << fix(std::fabs(r.F_up) / u.kForce) << " " << u.force << (r.F_up >= 0 ? " up" : " down");
        if (r.type == FIX)
            std::cout << ",  M = " << fix(std::fabs(r.M_cw) / u.kMoment) << " " << u.moment
                      << (r.M_cw >= 0 ? " clockwise" : " counterclockwise");
        std::cout << "\n";
    }

    size_t iV = 0, iMp = 0, iMn = 0;
    for (size_t i = 1; i < cv.x.size(); ++i) {
        if (std::fabs(cv.V[i]) > std::fabs(cv.V[iV])) iV = i;
        if (cv.M[i] > cv.M[iMp]) iMp = i;
        if (cv.M[i] < cv.M[iMn]) iMn = i;
    }
    std::cout << "    Max |shear|      " << fix(std::fabs(cv.V[iV]) / u.kForce) << " " << u.force << " at x = "
              << fix(cv.x[iV] / u.kLen) << " " << u.len << "\n";
    std::cout << "    Max sagging M    ";
    if (cv.M[iMp] > 0) std::cout << fix(cv.M[iMp] / u.kMoment) << " " << u.moment << " at x = " << fix(cv.x[iMp] / u.kLen) << " " << u.len << "\n";
    else std::cout << "none\n";
    std::cout << "    Max hogging M    ";
    if (cv.M[iMn] < 0) std::cout << fix(cv.M[iMn] / u.kMoment) << " " << u.moment << " at x = " << fix(cv.x[iMn] / u.kLen) << " " << u.len << "\n";
    else std::cout << "none\n";

    if (cDepth > 0) {
        const double Mmax = std::max(std::fabs(cv.M[iMp]), std::fabs(cv.M[iMn]));
        std::cout << "    Bending stress   sigma_max = M c / I = " << fmt(Mmax * cDepth / bm.I / u.kStress) << " "
                  << u.stress << "  (c = " << fmt(cDepth / u.kDepth) << " " << u.depth << ")\n";
    }
    double sF, sM;
    equilibrium(bm, sol, sF, sM);
    std::cout << "    Equilibrium      sum Fy = " << sci(sF / u.kForce) << " " << u.force << ",  sum M = "
              << sci(sM / u.kMoment) << " " << u.moment << "  (both should be ~0)\n";
}

void writeCsv(const std::string& file, const Curves& cv, const Units& u,
              const std::function<double(double)>& table = nullptr) {
    std::ofstream f(file);
    if (!f) { std::cout << "\n  (Could not write " << file << ")\n"; return; }
    f << "x_" << u.len << ",w_" << u.dist << ",V_" << u.force << ",M_" << u.moment << ",slope_rad,deflection_" << u.defl;
    if (table) f << ",table_deflection_" << u.defl;
    f << "\n" << std::setprecision(10);
    for (size_t i = 0; i < cv.x.size(); ++i) {
        f << cv.x[i] / u.kLen << "," << cv.w[i] / u.kDist << "," << cv.V[i] / u.kForce << "," << cv.M[i] / u.kMoment
          << "," << cv.th[i] << "," << cv.y[i] / u.kDefl;
        if (table) f << "," << table(cv.x[i]) / u.kDefl;
        f << "\n";
    }
    std::cout << "\n  Saved " << cv.x.size() << " points to " << file << " (plot it in Excel, Sheets or Python).\n";
}

// ============================================================================
//  8. The classic deflection table
// ============================================================================
//  Each row: how to build the beam, the table's deflection curve y(x), the
//  table's max deflection and where it happens. The tour checks all of them
//  against the solver.
struct Ref {
    double L, E, I, P, w, M0;  // internal units; w is the peak intensity w0 for triangles
    double EI() const { return E * I; }
};

Ref defaultRef(const Units& u) {
    if (u.si) return {4.0 * u.kLen, 200.0 * u.kModulus, 50e6 * u.kInertia, 20.0 * u.kForce, 10.0 * u.kDist, 30.0 * u.kMoment};
    return {12.0 * u.kLen, 29000.0 * u.kModulus, 120.0 * u.kInertia, 5.0 * u.kForce, 0.8 * u.kDist, 10.0 * u.kMoment};
}

struct TableCase {
    std::string name, formula, where, curve;
    char kind;  // 'P' point load, 'w' distributed load, 'M' couple
    std::function<Beam(const Ref&)> build;
    std::function<double(const Ref&, double)> y;  // table deflection curve (down +)
    std::function<double(const Ref&)> dmax;       // table max deflection
    std::function<double(const Ref&)> xmax;       // where it happens
};

Beam mk(const Ref& r, double len, std::vector<Support> s, std::vector<Load> l) {
    Beam b;
    b.L = len;
    b.E = r.E;
    b.I = r.I;
    b.supports = std::move(s);
    b.loads = std::move(l);
    return b;
}

// Cantilever fixed at x = 0 with a point load P at x = a (the building block of many rows)
double yCantPoint(double P, double a, double EI, double x) {
    return x <= a ? P * x * x * (3 * a - x) / (6 * EI) : P * a * a * (3 * x - a) / (6 * EI);
}
// Simply supported, point load P at x = a
double ySSPoint(const Ref& r, double a, double x) {
    const double L = r.L, b = L - a;
    if (x <= a) return r.P * b * x * (L * L - b * b - x * x) / (6 * L * r.EI());
    const double xr = L - x;
    return r.P * a * xr * (L * L - a * a - xr * xr) / (6 * L * r.EI());
}
double ySSTriangle(const Ref& r, double x) {
    const double L = r.L;
    return r.w * x * (7 * std::pow(L, 4) - 10 * L * L * x * x + 3 * std::pow(x, 4)) / (360 * L * r.EI());
}
double ySSCouple(const Ref& r, double x) {
    const double L = r.L;
    return r.M0 * x * (2 * L * L - 3 * L * x + x * x) / (6 * L * r.EI());
}
// Propped cantilever, P at midspan = cantilever with P at L/2, minus a cantilever
// pushed UP at its tip by the roller reaction 5P/16 (superposition!)
double yProppedP(const Ref& r, double x) {
    return yCantPoint(r.P, r.L / 2, r.EI(), x) - yCantPoint(5 * r.P / 16, r.L, r.EI(), x);
}
double yProppedW(const Ref& r, double x) {
    const double L = r.L;
    return r.w * x * x * (3 * L * L - 5 * L * x + 2 * x * x) / (48 * r.EI());
}
double yOverhang(const Ref& r, double x) {
    const double L = r.L, a = r.L / 4, EI = r.EI();
    if (x <= L) return -r.P * a * x * (L * L - x * x) / (6 * L * EI);
    const double s = x - L;
    return r.P * s * (2 * a * L + 3 * a * s - s * s) / (6 * EI);
}

std::vector<TableCase> tableCases() {
    const double S3 = std::sqrt(3.0), S5 = std::sqrt(5.0);
    std::vector<TableCase> c;

    // ---------------- Cantilevers (fixed at x = 0, free at x = L) ----------------
    c.push_back({"Cantilever: P at free end", "P L^3 / (3EI)", "x = L (free end)",
                 "y = P x^2 (3L - x) / (6EI)", 'P',
                 [](const Ref& r) { return mk(r, r.L, {{FIX, 0.0}}, {pointLoad(r.P, r.L)}); },
                 [](const Ref& r, double x) { return yCantPoint(r.P, r.L, r.EI(), x); },
                 [](const Ref& r) { return r.P * std::pow(r.L, 3) / (3 * r.EI()); },
                 [](const Ref& r) { return r.L; }});

    c.push_back({"Cantilever: P at x = a (a = 0.6L)", "P a^2 (3L - a) / (6EI)", "x = L (free end)",
                 "y = P x^2 (3a - x)/(6EI) for x <= a,  P a^2 (3x - a)/(6EI) for x >= a", 'P',
                 [](const Ref& r) { return mk(r, r.L, {{FIX, 0.0}}, {pointLoad(r.P, 0.6 * r.L)}); },
                 [](const Ref& r, double x) { return yCantPoint(r.P, 0.6 * r.L, r.EI(), x); },
                 [](const Ref& r) { const double a = 0.6 * r.L; return r.P * a * a * (3 * r.L - a) / (6 * r.EI()); },
                 [](const Ref& r) { return r.L; }});

    c.push_back({"Cantilever: uniform w", "w L^4 / (8EI)", "x = L (free end)",
                 "y = w x^2 (6L^2 - 4Lx + x^2) / (24EI)", 'w',
                 [](const Ref& r) { return mk(r, r.L, {{FIX, 0.0}}, {distLoad(r.w, r.w, 0.0, r.L)}); },
                 [](const Ref& r, double x) {
                     return r.w * x * x * (6 * r.L * r.L - 4 * r.L * x + x * x) / (24 * r.EI()); },
                 [](const Ref& r) { return r.w * std::pow(r.L, 4) / (8 * r.EI()); },
                 [](const Ref& r) { return r.L; }});

    c.push_back({"Cantilever: triangle, w0 at wall", "w0 L^4 / (30EI)", "x = L (free end)",
                 "y = w0 x^2 (10L^3 - 10L^2 x + 5L x^2 - x^3) / (120 L EI)", 'w',
                 [](const Ref& r) { return mk(r, r.L, {{FIX, 0.0}}, {distLoad(r.w, 0.0, 0.0, r.L)}); },
                 [](const Ref& r, double x) {
                     const double L = r.L;
                     return r.w * x * x * (10 * L * L * L - 10 * L * L * x + 5 * L * x * x - x * x * x) / (120 * L * r.EI()); },
                 [](const Ref& r) { return r.w * std::pow(r.L, 4) / (30 * r.EI()); },
                 [](const Ref& r) { return r.L; }});

    c.push_back({"Cantilever: couple M0 at free end", "M0 L^2 / (2EI)", "x = L (free end)",
                 "y = M0 x^2 / (2EI)   (a circular arc: M is constant)", 'M',
                 [](const Ref& r) { return mk(r, r.L, {{FIX, 0.0}}, {coupleLoad(r.M0, r.L)}); },
                 [](const Ref& r, double x) { return r.M0 * x * x / (2 * r.EI()); },
                 [](const Ref& r) { return r.M0 * r.L * r.L / (2 * r.EI()); },
                 [](const Ref& r) { return r.L; }});

    // ---------------- Simply supported (pin at 0, roller at L) ----------------
    c.push_back({"Simply supported: P at midspan", "P L^3 / (48EI)", "x = L/2",
                 "y = P x (3L^2 - 4x^2) / (48EI) for x <= L/2 (mirror image beyond)", 'P',
                 [](const Ref& r) { return mk(r, r.L, {{PIN, 0.0}, {ROL, r.L}}, {pointLoad(r.P, r.L / 2)}); },
                 [](const Ref& r, double x) { return ySSPoint(r, r.L / 2, x); },
                 [](const Ref& r) { return r.P * std::pow(r.L, 3) / (48 * r.EI()); },
                 [](const Ref& r) { return r.L / 2; }});

    c.push_back({"Simply supported: P at x = a (0.7L)", "Pb(L^2-b^2)^1.5/(9sqrt3 LEI)",
                 "x = sqrt((L^2 - b^2)/3),  b = L - a",
                 "y = P b x (L^2 - b^2 - x^2) / (6 L EI) for x <= a", 'P',
                 [](const Ref& r) { return mk(r, r.L, {{PIN, 0.0}, {ROL, r.L}}, {pointLoad(r.P, 0.7 * r.L)}); },
                 [](const Ref& r, double x) { return ySSPoint(r, 0.7 * r.L, x); },
                 [S3](const Ref& r) {
                     const double L = r.L, b = 0.3 * L;
                     return r.P * b * std::pow(L * L - b * b, 1.5) / (9 * S3 * L * r.EI()); },
                 [](const Ref& r) { const double b = 0.3 * r.L; return std::sqrt((r.L * r.L - b * b) / 3); }});

    c.push_back({"Simply supported: uniform w", "5 w L^4 / (384EI)", "x = L/2",
                 "y = w x (L^3 - 2L x^2 + x^3) / (24EI)", 'w',
                 [](const Ref& r) { return mk(r, r.L, {{PIN, 0.0}, {ROL, r.L}}, {distLoad(r.w, r.w, 0.0, r.L)}); },
                 [](const Ref& r, double x) {
                     return r.w * x * (std::pow(r.L, 3) - 2 * r.L * x * x + x * x * x) / (24 * r.EI()); },
                 [](const Ref& r) { return 5 * r.w * std::pow(r.L, 4) / (384 * r.EI()); },
                 [](const Ref& r) { return r.L / 2; }});

    c.push_back({"Simply supported: triangle 0 -> w0", "0.00652 w0 L^4 / EI", "x = 0.5193 L",
                 "y = w0 x (7L^4 - 10L^2 x^2 + 3x^4) / (360 L EI)", 'w',
                 [](const Ref& r) { return mk(r, r.L, {{PIN, 0.0}, {ROL, r.L}}, {distLoad(0.0, r.w, 0.0, r.L)}); },
                 [](const Ref& r, double x) { return ySSTriangle(r, x); },
                 [](const Ref& r) { return ySSTriangle(r, r.L * std::sqrt(1 - std::sqrt(8.0 / 15.0))); },
                 [](const Ref& r) { return r.L * std::sqrt(1 - std::sqrt(8.0 / 15.0)); }});

    c.push_back({"Simply supported: couple M0 at end", "M0 L^2 / (9 sqrt3 EI)", "x = 0.4226 L (from the loaded end)",
                 "y = M0 x (2L^2 - 3Lx + x^2) / (6 L EI)", 'M',
                 [](const Ref& r) { return mk(r, r.L, {{PIN, 0.0}, {ROL, r.L}}, {coupleLoad(r.M0, 0.0)}); },
                 [](const Ref& r, double x) { return ySSCouple(r, x); },
                 [S3](const Ref& r) { return r.M0 * r.L * r.L / (9 * S3 * r.EI()); },
                 [S3](const Ref& r) { return r.L * (1 - 1 / S3); }});

    // ---------------- Fixed at both ends ----------------
    c.push_back({"Fixed-fixed: P at midspan", "P L^3 / (192EI)", "x = L/2",
                 "y = P x^2 (3L - 4x) / (48EI) for x <= L/2 (mirror image beyond)", 'P',
                 [](const Ref& r) { return mk(r, r.L, {{FIX, 0.0}, {FIX, r.L}}, {pointLoad(r.P, r.L / 2)}); },
                 [](const Ref& r, double x) {
                     const double s = std::min(x, r.L - x);
                     return r.P * s * s * (3 * r.L - 4 * s) / (48 * r.EI()); },
                 [](const Ref& r) { return r.P * std::pow(r.L, 3) / (192 * r.EI()); },
                 [](const Ref& r) { return r.L / 2; }});

    c.push_back({"Fixed-fixed: uniform w", "w L^4 / (384EI)", "x = L/2",
                 "y = w x^2 (L - x)^2 / (24EI)", 'w',
                 [](const Ref& r) { return mk(r, r.L, {{FIX, 0.0}, {FIX, r.L}}, {distLoad(r.w, r.w, 0.0, r.L)}); },
                 [](const Ref& r, double x) { return r.w * x * x * (r.L - x) * (r.L - x) / (24 * r.EI()); },
                 [](const Ref& r) { return r.w * std::pow(r.L, 4) / (384 * r.EI()); },
                 [](const Ref& r) { return r.L / 2; }});

    // ---------------- Propped cantilever (fixed at 0, roller at L) ----------------
    c.push_back({"Propped cantilever: P at midspan", "P L^3 / (48 sqrt5 EI)",
                 "x = 0.5528 L from the wall (L/sqrt5 from the roller)",
                 "cantilever with P at L/2, minus a cantilever pushed up at L by the roller's 5P/16", 'P',
                 [](const Ref& r) { return mk(r, r.L, {{FIX, 0.0}, {ROL, r.L}}, {pointLoad(r.P, r.L / 2)}); },
                 [](const Ref& r, double x) { return yProppedP(r, x); },
                 [S5](const Ref& r) { return r.P * std::pow(r.L, 3) / (48 * S5 * r.EI()); },
                 [S5](const Ref& r) { return r.L * (1 - 1 / S5); }});

    c.push_back({"Propped cantilever: uniform w", "w L^4 / (185EI)", "x = 0.5785 L from the wall",
                 "y = w x^2 (3L^2 - 5Lx + 2x^2) / (48EI)   (roller carries 3wL/8)", 'w',
                 [](const Ref& r) { return mk(r, r.L, {{FIX, 0.0}, {ROL, r.L}}, {distLoad(r.w, r.w, 0.0, r.L)}); },
                 [](const Ref& r, double x) { return yProppedW(r, x); },
                 [](const Ref& r) { return yProppedW(r, r.L * (15 - std::sqrt(33.0)) / 16); },
                 [](const Ref& r) { return r.L * (15 - std::sqrt(33.0)) / 16; }});

    // ---------------- Overhang (span L between supports, overhang a = L/4) ----------------
    c.push_back({"Overhang: P at tip (a = L/4)", "P a^2 (L + a) / (3EI)", "x = L + a (tip of the overhang)",
                 "span: y = -P a x (L^2 - x^2)/(6 L EI) (it LIFTS); overhang: y = P s (2aL + 3as - s^2)/(6EI), s = x - L", 'P',
                 [](const Ref& r) { return mk(r, 1.25 * r.L, {{PIN, 0.0}, {ROL, r.L}}, {pointLoad(r.P, 1.25 * r.L)}); },
                 [](const Ref& r, double x) { return yOverhang(r, x); },
                 [](const Ref& r) { const double a = r.L / 4; return r.P * a * a * (r.L + a) / (3 * r.EI()); },
                 [](const Ref& r) { return 1.25 * r.L; }});
    return c;
}

double loadOf(char kind, const Ref& r) { return kind == 'P' ? r.P : kind == 'w' ? r.w : r.M0; }
int powerOf(char kind) { return kind == 'P' ? 3 : kind == 'w' ? 4 : 2; }
std::string loadSymbol(char kind) { return kind == 'P' ? "P L^3" : kind == 'w' ? "w L^4" : "M0 L^2"; }

// ============================================================================
//  9. Program modes
// ============================================================================
void tour(const Units& u, const Ref& r) {
    const auto cases = tableCases();
    std::cout << "\n  THE BEAM DEFLECTION TABLE  --  every row, table formula vs. simulation\n"
              << "  " << std::string(72, '=') << "\n"
              << "  Reference beam:  L = " << fmt(r.L / u.kLen) << " " << u.len << ",  E = " << fmt(r.E / u.kModulus)
              << " " << u.modulus << ",  I = " << fmt(r.I / u.kInertia, 6) << " " << u.inertia << "\n"
              << "  Loads:           P = " << fmt(r.P / u.kForce) << " " << u.force << ",  w (or peak w0) = "
              << fmt(r.w / u.kDist) << " " << u.dist << ",  M0 = " << fmt(r.M0 / u.kMoment) << " " << u.moment << "\n\n";

    std::cout << "  " << padL("#", 2) << "  " << padR("Beam and loading", 36) << padR("Table says dmax =", 30)
              << padL("Table", 10) << padL("Simulated", 11) << padL("Diff %", 10) << "\n"
              << "  " << padR("", 68) << padL("[" + u.defl + "]", 10) << padL("[" + u.defl + "]", 11) << "\n"
              << "  " << std::string(99, '-') << "\n";

    double worstPeak = 0.0, worstCurve = 0.0;
    std::vector<double> C(cases.size(), 0.0);
    for (size_t i = 0; i < cases.size(); ++i) {
        const auto& tc = cases[i];
        const Beam bm = tc.build(r);
        const Solution sol = solveBeam(bm);
        if (!sol.ok) { std::cout << "  " << i + 1 << "  " << tc.name << ": " << sol.error << "\n"; continue; }
        const Curves cv = sampleBeam(bm, sol);
        const Peak pk = maxDeflection(sol, cv);
        const double tab = tc.dmax(r), sim = std::fabs(pk.y);
        const double diff = std::fabs(sim - tab) / tab * 100.0;
        double gap = 0.0;
        for (size_t j = 0; j < cv.x.size(); ++j) gap = std::max(gap, std::fabs(cv.y[j] - tc.y(r, cv.x[j])));
        worstPeak = std::max(worstPeak, diff);
        worstCurve = std::max(worstCurve, gap / tab * 100.0);
        C[i] = tab * r.EI() / (loadOf(tc.kind, r) * std::pow(r.L, powerOf(tc.kind)));

        std::cout << "  " << padL(std::to_string(i + 1), 2) << "  " << padR(tc.name, 36) << padR(tc.formula, 30)
                  << padL(num(tab / u.kDefl), 10) << padL(num(sim / u.kDefl), 11) << padL(sci(diff), 10) << "\n";
    }
    std::cout << "  " << std::string(99, '-') << "\n"
              << "  Worst difference in max deflection: " << sci(worstPeak) << " %\n"
              << "  Worst gap between the table's curve y(x) and the simulation, anywhere on any beam: "
              << sci(worstCurve) << " % of dmax\n"
              << "  -> Every row is the same equation, E I y'''' = w(x), solved with different supports and loads.\n";

    std::cout << "\n  WHY THE TABLE IS SMALLER THAN IT LOOKS\n"
              << "  " << std::string(72, '=') << "\n"
              << "  Every answer above has the same shape:     dmax = C x (load) x L^n / (E I)\n"
              << "  The load type fixes the power of L (P -> L^3, w -> L^4, M0 -> L^2) so the answer\n"
              << "  is a length. Only the pure number C changes, and C is a stiffness score set by\n"
              << "  the supports: smaller C (bigger denominator) = stiffer beam.\n";
    for (char kind : {'P', 'w', 'M'}) {
        std::vector<std::pair<double, std::string>> rows;
        for (size_t i = 0; i < cases.size(); ++i)
            if (cases[i].kind == kind && C[i] > 0) rows.push_back({C[i], cases[i].name});
        std::sort(rows.begin(), rows.end(), [](const auto& a, const auto& b) { return a.first > b.first; });
        const std::string head = kind == 'P' ? "Point load P" : kind == 'w' ? "Distributed load w" : "Couple M0";
        std::cout << "\n  " << padR(head, 22) << "dmax = C x " << loadSymbol(kind) << " / (E I)     (floppiest first)\n";
        for (const auto& row : rows)
            std::cout << "      C = 1/" << padR(fmt(1.0 / row.first, 4), 8) << " = " << padR(fmt(row.first, 4), 10)
                      << row.second << "\n";
    }
    if (C[5] > 0 && C[10] > 0 && C[7] > 0 && C[11] > 0 && C[0] > 0)
        std::cout << "\n  Same span, same load:\n"
                  << "    * fixing both ends instead of pinning them: " << fmt(C[5] / C[10], 3)
                  << "x stiffer (point load), " << fmt(C[7] / C[11], 3) << "x stiffer (uniform load)\n"
                  << "    * a cantilever loaded at its tip sags " << fmt(C[0] / C[5], 3)
                  << "x more than a simply supported beam loaded at midspan\n"
                  << "  (Rows 2, 7 and 15 depend on where the load sits, so their C changes with a/L.)\n";
}

void caseDetail(int k, const Units& u, const Ref& r) {
    const auto cases = tableCases();
    const TableCase& tc = cases[k - 1];
    const Beam bm = tc.build(r);
    std::cout << "\n  TABLE CASE " << k << ":  " << tc.name << "\n  " << std::string(66, '=') << "\n";
    drawBeam(bm, u);
    std::cout << "\n  Table formula   dmax = " << tc.formula << "\n"
              << "  Occurs at       " << tc.where << "\n"
              << "  Curve           " << tc.curve << "\n";

    const Solution sol = solveBeam(bm);
    if (!sol.ok) { std::cout << "\n  Can't solve: " << sol.error << "\n"; return; }
    const Curves cv = sampleBeam(bm, sol);
    const Peak pk = maxDeflection(sol, cv);
    const double tab = tc.dmax(r);
    const double C = tab * r.EI() / (loadOf(tc.kind, r) * std::pow(r.L, powerOf(tc.kind)));

    std::cout << "\n  " << padR("", 20) << padL("Table", 16) << padL("Simulation", 16) << "\n"
              << "  " << padR("Max deflection", 20) << padL(num(tab / u.kDefl) + " " + u.defl, 16)
              << padL(num(std::fabs(pk.y) / u.kDefl) + " " + u.defl, 16) << "\n"
              << "  " << padR("Location", 20) << padL("x = " + fix(tc.xmax(r) / u.kLen) + " " + u.len, 16)
              << padL("x = " + fix(pk.x / u.kLen) + " " + u.len, 16) << "\n"
              << "  As C x " << loadSymbol(tc.kind) << " / EI:   C = 1/" << fmt(1.0 / C, 5) << "\n";

    report(bm, sol, cv, u, 0.0, false);
    plots(bm, cv, u);
    writeCsv("table_case_" + std::to_string(k) + ".csv", cv, u, [&](double x) { return tc.y(r, x); });
}

void superposition(const Units& u, const Ref& r) {
    const auto cases = tableCases();
    const TableCase& rowP = cases[5];   // simply supported, P at midspan
    const TableCase& rowPa = cases[6];  // simply supported, P at 0.7L
    const TableCase& rowW = cases[7];   // simply supported, uniform w
    auto simMax = [](const Beam& bm) {
        const Solution sol = solveBeam(bm);
        return maxDeflection(sol, sampleBeam(bm, sol));
    };
    auto D = [&](double y) { return num(y / u.kDefl) + " " + u.defl; };
    auto X = [&](double x) { return "x = " + fix(x / u.kLen) + " " + u.len; };

    std::cout << "\n  SUPERPOSITION: how to combine rows of the table\n  " << std::string(66, '=') << "\n"
              << "  The beam equation is linear, so deflections from separate loads ADD.\n"
              << "  Add the deflection CURVES y1(x) + y2(x), then find the max of the sum.\n"
              << "  Adding the two maxima only works if both maxima happen at the same x.\n";

    Beam b1 = rowW.build(r);
    b1.loads.push_back(rowP.build(r).loads[0]);
    const Peak p1 = simMax(b1);
    std::cout << "\n  EXAMPLE 1: simply supported, uniform w + P at midspan (both peak at L/2)\n";
    drawBeam(b1, u);
    std::cout << "\n    row 8 alone (uniform w)            " << padL(D(rowW.dmax(r)), 14) << "  at " << X(rowW.xmax(r)) << "\n"
              << "    row 6 alone (P at midspan)         " << padL(D(rowP.dmax(r)), 14) << "  at " << X(rowP.xmax(r)) << "\n"
              << "    table: add them                    " << padL(D(rowW.dmax(r) + rowP.dmax(r)), 14) << "\n"
              << "    simulation, both loads at once     " << padL(D(std::fabs(p1.y)), 14) << "  at " << X(p1.x) << "\n"
              << "    -> match, because the peaks line up.\n";

    Beam b2 = rowW.build(r);
    b2.loads.push_back(rowPa.build(r).loads[0]);
    const Peak p2 = simMax(b2);
    double best = 0.0, xb = 0.0;
    for (int i = 0; i <= 20000; ++i) {
        const double x = r.L * i / 20000.0, y = rowW.y(r, x) + rowPa.y(r, x);
        if (y > best) { best = y; xb = x; }
    }
    const double naive = rowW.dmax(r) + rowPa.dmax(r);
    std::cout << "\n  EXAMPLE 2: simply supported, uniform w + P at x = 0.7L (peaks at different x)\n";
    drawBeam(b2, u);
    std::cout << "\n    row 8 alone (uniform w)            " << padL(D(rowW.dmax(r)), 14) << "  at " << X(rowW.xmax(r)) << "\n"
              << "    row 7 alone (P at 0.7L)            " << padL(D(rowPa.dmax(r)), 14) << "  at " << X(rowPa.xmax(r)) << "\n"
              << "    WRONG: add the two maxima          " << padL(D(naive), 14) << "  (overestimates by "
              << fix((naive - best) / best * 100.0, 2) << " %)\n"
              << "    RIGHT: max of y8(x) + y7(x)        " << padL(D(best), 14) << "  at " << X(xb) << "\n"
              << "    simulation, both loads at once     " << padL(D(std::fabs(p2.y)), 14) << "  at " << X(p2.x) << "\n"
              << "    -> adding the curves matches the simulation; adding the peaks doesn't.\n"
              << "       (On an exam, adding peaks is conservative but not exact.)\n";
}

void theory() {
    std::cout << R"TXT(
  THE ONE EQUATION BEHIND THE WHOLE TABLE
  =======================================================================
  Bend a slender beam and its curvature is proportional to the bending
  moment (y measured DOWNWARD, M > 0 sagging):

          E I y''(x) = -M(x)

  Differentiate twice using dM/dx = V and dV/dx = -w:

          E I y''''(x) = w(x)

  Every row of the deflection table is this same recipe:
    1. Write the load w(x) for that case.
    2. Integrate four times. Each integration adds one constant:
          E I y'''  = -V                 (+ C1)
          E I y''   = -M                 (+ C2)
          E I y'    =  E I x slope       (+ C3)
          E I y     =  E I x deflection  (+ C4)
    3. Use the supports to pin down C1..C4 (two conditions per end):
          fixed end      y = 0   and  y' = 0      no deflection, no rotation
          pin / roller   y = 0   and  M  = 0      (y'' = 0 at an end)
          free end       M = 0   and  V  = 0      (y'' = 0 and y''' = 0)
    4. The max is where y' = 0 (or at a free end).

  WORKED EXAMPLE: cantilever with uniform load w (row 3), fixed at x = 0
    E I y'''' = w
    E I y'''  = w x + C1                          free end V = 0:   y'''(L) = 0 -> C1 = -wL
    E I y''   = w x^2/2 - wL x + C2               free end M = 0:   y''(L)  = 0 -> C2 = wL^2/2
    E I y'    = w x^3/6 - wL x^2/2 + wL^2 x/2 + C3     fixed:  y'(0) = 0 -> C3 = 0
    E I y     = w x^4/24 - wL x^3/6 + wL^2 x^2/4 + C4  fixed:  y(0)  = 0 -> C4 = 0

    y(x) = w x^2 (6L^2 - 4L x + x^2) / (24 E I)   ->   y(L) = w L^4 / (8 E I)

    That's row 3. Every other row is the same four steps with a different
    w(x) and different end conditions.

  INDETERMINATE BEAMS (fixed-fixed, propped cantilever)
    Statics alone can't find the reactions, but the recipe doesn't care:
    there are still four constants and four boundary conditions. The extra
    support condition (y = 0 at the roller) is what gives you the redundant
    reaction, e.g. 5P/16 or 3wL/8 for a propped cantilever.

  HOW TO READ THE TABLE WITHOUT FEAR
    * Pick the row by SUPPORTS first, then by LOAD type.
    * The load type sets the power of L:  P -> L^3,  w -> L^4,  M0 -> L^2.
      Units check: P L^3/(E I) and w L^4/(E I) both come out as a length.
    * The number in the denominator is a stiffness score: bigger = stiffer.
    * Several loads? Add the deflection CURVES, then find the max of the sum
      (menu option 4 shows why adding the maxima can be wrong).
    * Assumptions: constant E I, small deflections, linear elastic material.

  HOW THIS PROGRAM SOLVES A BEAM
    It solves the same equation numerically with the finite element method.
    The beam is cut into ~120 short elements. Inside each one the deflection
    is a cubic (the exact solution of E I y'''' = 0), described by the
    deflection and slope at its two ends. Gluing the elements together and
    applying the supports gives a linear system K u = F -- the same Gaussian
    elimination you do by hand, just with ~250 unknowns. For a uniform beam
    this gives the exact nodal deflections, so it matches the table to
    round-off, and it keeps working for beams the table doesn't list.
)TXT";
}

// ---------------------------------------------------------------------------
// Build-your-own-beam mode
// ---------------------------------------------------------------------------
double askPosition(const std::string& prompt, double def, double Ld) {
    for (;;) {
        const double v = askDouble(prompt, def);
        if (v >= 0 && v <= Ld * (1 + 1e-12)) return std::min(v, Ld);
        std::cout << "    Position must be between 0 and " << fmt(Ld) << ".\n";
    }
}

Beam askBeam(const Units& u, double& cDepth) {
    Beam bm;
    std::cout << "\n  BUILD YOUR OWN BEAM   (" << unitsName(u) << ")\n"
              << "  Press Enter to accept the value in [brackets]. x is measured from the left end.\n\n";
    const double Ld = askPositive("Beam length L (" + u.len + ")", u.si ? 4.0 : 12.0);
    const double Ed = askPositive("Elastic modulus E (" + u.modulus + ")", u.si ? 200.0 : 29000.0);
    const double Id = askPositive("Second moment of area I (" + u.inertia + ")", u.si ? 50e6 : 120.0);
    bm.L = Ld * u.kLen;
    bm.E = Ed * u.kModulus;
    bm.I = Id * u.kInertia;

    std::cout << "\n  Supports\n"
                 "    1  Cantilever, fixed at the left end\n"
                 "    2  Cantilever, fixed at the right end\n"
                 "    3  Simply supported (pin left, roller right)\n"
                 "    4  Fixed at both ends\n"
                 "    5  Propped cantilever (fixed left, roller right)\n"
                 "    6  Place supports yourself (overhangs, continuous beams, ...)\n";
    switch (askInt("Choice", 3, 1, 6)) {
        case 1: bm.supports = {{FIX, 0.0}}; break;
        case 2: bm.supports = {{FIX, bm.L}}; break;
        case 3: bm.supports = {{PIN, 0.0}, {ROL, bm.L}}; break;
        case 4: bm.supports = {{FIX, 0.0}, {FIX, bm.L}}; break;
        case 5: bm.supports = {{FIX, 0.0}, {ROL, bm.L}}; break;
        default: {
            const int n = askInt("How many supports", 2, 1, 6);
            for (int i = 0; i < n; ++i) {
                const std::string tag = "Support " + std::to_string(i + 1);
                const int t = askInt(tag + " type (1 pin, 2 roller, 3 fixed)", i == 0 ? 1 : 2, 1, 3);
                const double x = askPosition(tag + " position x (" + u.len + ")", i == 0 ? 0.0 : 0.75 * Ld, Ld);
                bm.supports.push_back({t == 1 ? PIN : t == 2 ? ROL : FIX, x * u.kLen});
            }
        }
    }

    const double dP = u.si ? 20.0 : 5.0, dw = u.si ? 10.0 : 0.8, dM = u.si ? 30.0 : 10.0;
    std::cout << "\n  Loads  (forces and intensities positive DOWN, couples positive CLOCKWISE)\n";
    for (;;) {
        std::cout << "\n    1 point load   2 uniform load   3 linearly varying load   4 couple   0 done\n";
        const int t = askInt("Add a load", bm.loads.empty() ? 1 : 0, 0, 4);
        if (t == 0) {
            if (bm.loads.empty()) { std::cout << "    Add at least one load first.\n"; continue; }
            break;
        }
        if (bm.loads.size() >= 35) { std::cout << "    That's plenty of loads.\n"; break; }
        if (t == 1) {
            const double P = askDouble("P (" + u.force + ", down +)", dP);
            const double x = askPosition("at x (" + u.len + ")", Ld / 2, Ld);
            bm.loads.push_back(pointLoad(P * u.kForce, x * u.kLen));
        } else if (t == 2 || t == 3) {
            double w1, w2;
            if (t == 2) { w1 = w2 = askDouble("w (" + u.dist + ", down +)", dw); }
            else {
                w1 = askDouble("w at the start (" + u.dist + ")", 0.0);
                w2 = askDouble("w at the end (" + u.dist + ")", dw);
            }
            const double a = askPosition("starts at x (" + u.len + ")", 0.0, Ld);
            double b = askPosition("ends at x (" + u.len + ")", Ld, Ld);
            while (b <= a) {
                std::cout << "    The end has to be to the right of the start.\n";
                b = askPosition("ends at x (" + u.len + ")", Ld, Ld);
            }
            bm.loads.push_back(distLoad(w1 * u.kDist, w2 * u.kDist, a * u.kLen, b * u.kLen));
        } else {
            const double C = askDouble("M0 (" + u.moment + ", clockwise +)", dM);
            const double x = askPosition("at x (" + u.len + ")", Ld, Ld);
            bm.loads.push_back(coupleLoad(C * u.kMoment, x * u.kLen));
        }
    }
    cDepth = askDouble("\n  Distance c from neutral axis to outer fiber, for bending stress (" + u.depth +
                           "), 0 = skip", 0.0) * u.kDepth;
    return bm;
}

void customMode(const Units& u) {
    double c = 0.0;
    const Beam bm = askBeam(u, c);
    std::cout << "\n";
    drawBeam(bm, u);
    const Solution sol = solveBeam(bm);
    if (!sol.ok) { std::cout << "\n  Can't solve this beam: " << sol.error << "\n"; return; }
    const Curves cv = sampleBeam(bm, sol);
    report(bm, sol, cv, u, c, true);
    plots(bm, cv, u);
    writeCsv("my_beam.csv", cv, u);
}

Ref askRef(const Units& u, Ref r, char kind) {
    std::cout << "\n  Press Enter to keep each reference value.\n";
    r.L = askPositive("Span L (" + u.len + ")", r.L / u.kLen) * u.kLen;
    r.E = askPositive("E (" + u.modulus + ")", r.E / u.kModulus) * u.kModulus;
    r.I = askPositive("I (" + u.inertia + ")", r.I / u.kInertia) * u.kInertia;
    if (kind == 'P') r.P = askDouble("P (" + u.force + ")", r.P / u.kForce) * u.kForce;
    if (kind == 'w') r.w = askDouble("w or peak w0 (" + u.dist + ")", r.w / u.kDist) * u.kDist;
    if (kind == 'M') r.M0 = askDouble("M0 (" + u.moment + ")", r.M0 / u.kMoment) * u.kMoment;
    return r;
}

void usage() {
    std::cout << "Usage: beam [--tour | --case N | --superpose | --theory] [--us]\n"
                 "  (no arguments)  interactive menu\n"
                 "  --tour          every table row: formula vs simulation\n"
                 "  --case N        one table case in detail (N = 1..15)\n"
                 "  --superpose     superposition demo\n"
                 "  --theory        the one equation behind the table\n"
                 "  --us            US customary units (kip, ft, ksi, in^4)\n";
}

}  // namespace

// The graphical version (beam_gui.cpp) #includes this whole file to reuse the
// solver, and defines BEAM_NO_MAIN first so this terminal main() is skipped.
#ifndef BEAM_NO_MAIN
int main(int argc, char** argv) {
    Units u = siUnits();
    const std::vector<std::string> args(argv + 1, argv + argc);
    for (const auto& a : args)
        if (a == "--us") u = usUnits();
    Ref ref = defaultRef(u);
    const int nCases = static_cast<int>(tableCases().size());

    for (size_t i = 0; i < args.size(); ++i) {
        const std::string& a = args[i];
        if (a == "--tour") { tour(u, ref); return 0; }
        if (a == "--theory") { theory(); return 0; }
        if (a == "--superpose") { superposition(u, ref); return 0; }
        if (a == "--help" || a == "-h") { usage(); return 0; }
        if (a == "--case") {
            const int n = (i + 1 < args.size()) ? std::atoi(args[i + 1].c_str()) : 0;
            if (n < 1 || n > nCases) { std::cerr << "Use --case 1 to --case " << nCases << "\n"; return 1; }
            caseDetail(n, u, ref);
            return 0;
        }
        if (a != "--us") { usage(); return 1; }
    }

    for (;;) {
        std::cout << "\n  ==============================================================\n"
                  << "   BEAM DEFLECTION EXPLORER        units: " << unitsName(u) << "\n"
                  << "  ==============================================================\n"
                  << "   1  Tour the deflection table   (every row: formula vs simulation)\n"
                  << "   2  One table case up close     (sketch, V, M, slope, deflection)\n"
                  << "   3  Build your own beam         (any supports, any mix of loads)\n"
                  << "   4  Superposition demo          (combining rows correctly)\n"
                  << "   5  The one equation behind the table\n"
                  << "   6  Switch to " << (u.si ? "US units (kip, ft, ksi, in^4)" : "SI units (kN, m, GPa, mm^4)") << "\n"
                  << "   0  Quit\n";
        const int choice = askInt("Choose", 1, 0, 6);
        if (choice == 0) break;
        if (choice == 1) tour(u, ref);
        if (choice == 2) {
            const auto cases = tableCases();
            std::cout << "\n";
            for (size_t i = 0; i < cases.size(); ++i)
                std::cout << "   " << padL(std::to_string(i + 1), 2) << "  " << cases[i].name << "\n";
            const int n = askInt("Which case", 8, 1, nCases);
            caseDetail(n, u, askRef(u, ref, cases[n - 1].kind));
        }
        if (choice == 3) customMode(u);
        if (choice == 4) superposition(u, ref);
        if (choice == 5) theory();
        if (choice == 6) { u = u.si ? usUnits() : siUnits(); ref = defaultRef(u); }
    }
    return 0;
}
#endif  // BEAM_NO_MAIN
