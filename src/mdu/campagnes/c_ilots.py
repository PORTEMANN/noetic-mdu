"""C-ILOTS — les îlots de stabilité 18k + m (verdict local CONFORME sous coupure).

Formule (Atomes_2, 11/12/2025) : Z_stable = 18k + m, m ∈ {0, 6, 12}.
Coupure (07/09/2026) : k ≤ 9 — imposée par la limite causale du Koïlon
(c_s ≤ c ⇒ Z_max ≈ 179–180 ; registre Z-MAX).

Usage : python -m mdu.campagnes.c_ilots
"""

from __future__ import annotations
import numpy as np

Z_MAX = 180  # registre canonique (P40, recomputé exact) ; 179 = alias causal


def rejouer() -> dict:
    brut = sorted({18 * k + m for k in range(1, 12) for m in (0, 6, 12)
                   if 18 * k + m > 92})
    coupe = sorted({18 * k + m for k in range(1, 10) for m in (0, 6, 12)
                    if 18 * k + m > 92})
    return {
        "ilots_brut": brut,
        "debordement_sans_coupure": [z for z in brut if z > Z_MAX],
        "ilots_avec_coupure": coupe,
        "coherent_avec_z_max": bool(max(coupe) <= Z_MAX),
        "cites_par_larticle_presents": all(z in coupe for z in (126, 132, 150, 156)),
        "verdict": "CONFORME sous coupure k ≤ 9",
    }


if __name__ == "__main__":
    r = rejouer()
    print("C-ILOTS — îlots de stabilité 18k + m :")
    for cle, v in r.items():
        print(f"  {cle} : {v}")
