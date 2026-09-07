"""compare.py — les trois versions de la MDU sur le même signal.

Rejoue la partie : la boucle de novembre 2025, l'automate V4.0 et le solveur V4.1
reçoivent le même signal d'entrée ; les invariants/résidus sont tabulés côte à côte.

Usage : python src/compare.py
"""

from __future__ import annotations
import numpy as np

from mdu.boucle_v2025_11_24 import BoucleNoetique
from mdu.automate_v4_0 import AutomateSpectral
from mdu.solveur_v4_1 import SolveurInvariants


def main() -> None:
    rng = np.random.default_rng(20260907)
    n = 64
    # signal 7 plans : le plan k oscille à la fréquence 2^(k/12) (la gamme, dans l'entrée)
    t = np.linspace(0, 4 * np.pi, 256)
    signal = np.stack([np.sin(2.0 ** (k / 12) * t) + 0.05 * rng.standard_normal(256)
                       for k in range(7)], axis=1)
    x0 = rng.standard_normal(n) * 0.1

    # V.24/11/2025 — la boucle itérative
    boucle = BoucleNoetique(n=n)  # η auto-conservatif (document, extension « boucle adaptative »)
    r1 = boucle.run(x0, max_iter=2000, tol=1e-6)
    rho1 = boucle.rayon_spectral_jacobienne(r1["x"])

    # V4.0 — l'automate spectral
    auto = AutomateSpectral(n=n)
    r2 = auto.run(x0, pas=200)
    st2 = auto.stabilite()

    # V4.1 — le solveur d'invariants
    sol = SolveurInvariants()
    r3 = sol.run(signal)

    print("=== Trois versions de la MDU, même entrée ===\n")
    print(f"[24/11/2025] boucle itérative   : converge en {r1['iterations']} it. "
          f"(converge : {r1['converge']}) ; ρ(J) = {rho1:.4f}")
    print(f"[V4.0  01/2026] automate spectral : énergie {r2['energie'][0]:.4f} → "
          f"{r2['energie'][-1]:.4f} ; ρ(I+ηA) = {st2['rho']:.4f} (stable : {st2['stable']})")
    fin = r3["final"]
    print(f"[V4.1  05/2026] solveur invariants : I₁ = {fin['I1']:.4f} ; Re_N = {fin['Re_N']:.4f} ; "
          f"régime nominal {r3['pct_nominal']:.0f} % du run ; résidus R_c/R_top/R_dyn = "
          f"{fin['residus']['R_c']:.3f}/{fin['residus']['R_top']:.2f}/{fin['residus']['R_dyn']:.4f}")
    print("\nCohabitation : les trois versions partagent l'ossature (7 plans, invariants) ;")
    print("V4.1 est la plus aboutie (bornes prouvées sur I₃ et Re_N — 4-Math_Simple, 06/05/2026).")


if __name__ == "__main__":
    main()
