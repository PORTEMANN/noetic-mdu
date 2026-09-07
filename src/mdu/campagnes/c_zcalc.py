"""C-ZCALC — la simulation aveugle corrigée (verdict local CONFORME après correction).

Formule brute (atomes_3, 11/12/2025) : Z_calc = A / (2(1 + 0,006·A^0,6)).
Correction fine formalisée (07/09/2026) : vallée de stabilité SEMF —
    Z = A / (2 + (a_C/2a_sym)·A^(2/3)),  a_C = 0,72 MeV, a_sym = 23,2 MeV.

Domaine déclaré : A ≥ 4 (l'hydrogène, sans neutron, est hors vallée).

Usage : python -m mdu.campagnes.c_zcalc [--csv path/vers/anu_table_2.csv]
"""

from __future__ import annotations
import argparse
import numpy as np
from ..donnees import DATA_DEFAUT, charger_anu, masses_dominantes

A_C, A_SYM = 0.72, 23.2  # MeV (constantes SEMF typiques)


def z_calc_brut(A: np.ndarray) -> np.ndarray:
    return A / (2 * (1 + 0.006 * A ** 0.6))


def z_calc_corrige(A: np.ndarray) -> np.ndarray:
    return A / (2 + (A_C / (2 * A_SYM)) * A ** (2 / 3))


def rejouer(csv_path: str) -> dict:
    Z, _, sym = charger_anu(csv_path)
    A, _ = masses_dominantes(Z)
    Zf, Af = Z.astype(float), A.astype(float)
    eb, ec = (z_calc_brut(Af) - Zf) / Zf, (z_calc_corrige(Af) - Zf) / Zf
    return {
        "brut": {"mediane_pct": float(np.median(np.abs(eb)) * 100),
                 "rms_pct": float(np.sqrt(np.mean(eb**2)) * 100),
                 "sous_5pct": int(np.sum(np.abs(eb) < 0.05))},
        "corrige": {"mediane_pct": float(np.median(np.abs(ec)) * 100),
                    "rms_pct": float(np.sqrt(np.mean(ec**2)) * 100),
                    "sous_5pct": int(np.sum(np.abs(ec) < 0.05)),
                    "sous_10pct": int(np.sum(np.abs(ec) < 0.10))},
        "controle_U": float(z_calc_corrige(np.array([238.0]))[0]),
        "n": len(Z),
        "verdict": "CONFORME après correction"
                   if np.median(np.abs(ec)) < 0.05 else "DIVERGENT",
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(DATA_DEFAUT))
    a = ap.parse_args()
    r = rejouer(a.csv)
    print("C-ZCALC — simulation aveugle (brute vs corrigée SEMF) :")
    for cle, v in r.items():
        print(f"  {cle} : {v}")
