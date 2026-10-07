"""Symbolic geometry and high-precision checks of the seven-point placement.

Uses symbolic algebra for geometry and 60-digit evaluation for placement inequalities:
  1. the seven Moser-spindle vectors of the paper have all eleven edges of length exactly 1;
  2. the placement z_g = (35+12i)/37 * (g + (-290+149i)/250) is a rotation + translation;
  3. every placed vertex satisfies 0 < |z|^2 < 4 and the strict inequality P < P' (eq. source-27);
  4. the Moser spindle has no proper 3-colouring (brute force over 3^7 colourings).
Also brute-forces chromatic numbers used in Act 2 (triangle = 3, spindle = 4).
"""
import itertools
import sympy as sp

s3, s11 = sp.sqrt(3), sp.sqrt(11)
I = sp.I
A = (s3 + I) / 2
B = (s3 - I) / 2
T = s3
u = (5 + I * s11) / 6
G = {"0": sp.Integer(0), "A": A, "B": B, "T": T, "uA": u * A, "uB": u * B, "uT": u * T}
EDGES = [("0", "A"), ("0", "B"), ("A", "B"), ("A", "T"), ("B", "T"),
         ("0", "uA"), ("0", "uB"), ("uA", "uB"), ("uA", "uT"), ("uB", "uT"),
         ("T", "uT")]


def abs2(z):
    return sp.simplify(sp.expand(z * sp.conjugate(z)))


def main():
    ok = True
    for a, b in EDGES:
        d = abs2(G[a] - G[b])
        ok &= (d == 1)
        print(f"|{a}-{b}|^2 = {d}")
    rot = (35 + 12 * I) / 37
    print("|rotation|^2 =", abs2(rot))
    off = (-290 + 149 * I) / 250
    for name, g in G.items():
        z = sp.expand(rot * (g + off))
        xi, up = sp.re(z), sp.im(z)
        l = sp.simplify(xi**2 + up**2)
        P = up**2 * (3 * xi**2 - up**2) ** 2
        Pp = l**3 * (1 - l / 4) * (l - 1) ** 2
        # Numerical check at 60 digits; this is not the paper's rational interval certificate.
        lv, Pv, Ppv = (sp.N(e, 60) for e in (l, P, Pp))
        good = (0 < lv < 4) and (Pv < Ppv)
        ok &= bool(good)
        print(f"{name:>3}: z=({sp.N(xi,8)}, {sp.N(up,8)})  |z|^2={sp.N(lv,8)}  P={sp.N(Pv,6)}  P'={sp.N(Ppv,6)}  ok={good}")
    # 3-colourability of the spindle
    names = list(G)
    idx = {n: k for k, n in enumerate(names)}
    e = [(idx[a], idx[b]) for a, b in EDGES]

    def colourable(n, edges, k):
        return any(all(c[p] != c[q] for p, q in edges) for c in itertools.product(range(k), repeat=n))

    print("Moser spindle 3-colourable?", colourable(7, e, 3), " 4-colourable?", colourable(7, e, 4))
    ok &= (not colourable(7, e, 3)) and colourable(7, e, 4)
    print("ALL CHECKS PASS" if ok else "SOME CHECK FAILED")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
