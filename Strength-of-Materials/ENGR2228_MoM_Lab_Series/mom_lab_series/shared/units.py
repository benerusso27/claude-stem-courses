"""Unit constants shared by every lab's Python tools (style_guide.md section 1).
Internal calculations are in SI base units (N, m, Pa)."""
IN = 0.0254            # m per inch (exact)
MM = 1e-3              # m per mm
LBF = 4.4482216152605  # N per pound-force (exact definition)
KIP = 1e3 * LBF
KSI = 6.894757293168e6  # Pa per ksi
PSI = KSI / 1e3
MPA = 1e6
GPA = 1e9
KN = 1e3


def mpa_to_ksi(x):
    return x * MPA / KSI


def ksi_to_mpa(x):
    return x * KSI / MPA
