"""Small helpers shared by the Python verification scripts of every lab."""
from pathlib import Path


class Checks:
    def __init__(self, title):
        self.title, self.rows = title, []

    def rel(self, name, val, ref, tol, note=""):
        r = abs(val - ref) / max(abs(ref), 1e-300)
        self.rows.append((name + (f" — {note}" if note else ""), val, ref, r, tol, r <= tol))
        return r <= tol

    def abs(self, name, val, ref, tol, note=""):
        r = abs(val - ref)
        self.rows.append((name + (f" — {note}" if note else "") + " (absolute)", val, ref, r, tol, r <= tol))
        return r <= tol

    def true(self, name, cond, note=""):
        self.rows.append((name + (f" — {note}" if note else ""), bool(cond), True, 0.0 if cond else 1.0, 0.0, bool(cond)))
        return cond

    def write(self, path, verb="passed"):
        f = lambda v: (str(v) if isinstance(v, bool) else f"{v:.8g}")  # noqa: E731
        lines = [f"## {self.title}", "", "| Test | Value | Reference | Rel. difference | Tolerance | Result |",
                 "|---|---:|---:|---:|---:|---|"]
        for name, v, ref, r, tol, okk in self.rows:
            lines.append(f"| {name.replace('|', chr(92) + '|')} | {f(v)} | {f(ref)} | {r:.2e} | {tol:.1e} | {'PASS' if okk else '**FAIL**'} |")
        nf = sum(not r[-1] for r in self.rows)
        lines += ["", f"{len(self.rows) - nf} of {len(self.rows)} {verb}."]
        Path(path).write_text("\n".join(lines) + "\n")
        print("\n".join(lines))
        return 1 if nf else 0
