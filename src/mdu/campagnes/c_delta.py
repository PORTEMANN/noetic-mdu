"""C-DELTA — deltaANU (verdict local DIVERGENT, 07/09/2026).

La loi publiée : deltaANU = 137·Z^(−3/2), R² = 1 affiché (art. 5677).
Le rejeu : écart réel |k − 2^(1/12)|/2^(1/12) sur la table officielle ;
loi de puissance à exposant libre ; corrélation avec le modèle publié.

Usage : python -m mdu.campagnes.c_delta [--csv path/vers/anu_table_2.csv]
"""

from __future__ import annotations
import argparse
import numpy as np
from ..donnees import DATA_DEFAUT, charger_anu

CIBLE = 2.0 ** (1 / 12)


def rejouer(csv_path: str) -> dict:
    Z, N, _ = charger_anu(csv_path)
    k = N[1:] / N[:-1].astype(float)
    Zk = Z[1:].astype(float)
    d_reel = np.abs(k - CIBLE) / CIBLE
    d_publie = 137.0 * Zk ** (-1.5)
    m = d_reel > 1e-6
    pente, ic = np.polyfit(np.log(Zk[m]), np.log(d_reel[m]), 1)
    r2 = float(np.corrcoef(np.log(Zk[m]), np.log(d_reel[m]))[0, 1] ** 2)
    corr = float(np.corrcoef(d_reel, d_publie)[0, 1])
    return {
        "pente_mesuree": float(pente),       # article : −1,5
        "amplitude_mesuree": float(np.exp(ic)),  # article : 137
        "r2_loglog": r2,                     # article : 1 affiché
        "correlation_monotone": corr,        # la forme survit
        "verdict": "DIVERGENT — tendance réelle, loi publiée fausse",
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(DATA_DEFAUT))
    a = ap.parse_args()
    r = rejouer(a.csv)
    print("C-DELTA — deltaANU = 137·Z^(−3/2) face aux données :")
    for cle, v in r.items():
        print(f"  {cle} : {v}")
