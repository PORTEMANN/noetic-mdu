"""C-GAMME — la gamme du Koilon (verdict local CONFORME, 07/09/2026).

Moyenne géométrique des k(i) = N_ANU(Z)/N_ANU(Z−1) contre 2^(1/12),
intervalle de confiance bootstrap (graine figée).

Usage : python -m mdu.campagnes.c_gamme [--csv path/vers/anu_table_2.csv]
"""

from __future__ import annotations
import argparse
import numpy as np
from ..donnees import DATA_DEFAUT, charger_anu

GRAINE = 20260907
CIBLE = 2.0 ** (1 / 12)


def rejouer(csv_path: str, n_boot: int = 20000) -> dict:
    Z, N, _ = charger_anu(csv_path)
    k = N[1:] / N[:-1].astype(float)
    gm = float(np.exp(np.mean(np.log(k))))
    rng = np.random.default_rng(GRAINE)
    boots = np.array([np.exp(np.mean(np.log(k[rng.integers(0, len(k), len(k))])))
                      for _ in range(n_boot)])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    m = (Z[1:] >= 11) & (Z[1:] <= 30)
    return {
        "moyenne_geometrique": gm,
        "cible": CIBLE,
        "ecart_pct": abs(gm - CIBLE) / CIBLE * 100,
        "ic95": (float(lo), float(hi)),
        "cible_dans_ic95": bool(lo <= CIBLE <= hi),
        "moyenne_plage_11_30": float(k[m].mean()),
        "verdict": "CONFORME" if (abs(gm - CIBLE) / CIBLE < 0.005 and lo <= CIBLE <= hi)
                   else "DIVERGENT",
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(DATA_DEFAUT))
    a = ap.parse_args()
    r = rejouer(a.csv)
    print("C-GAMME — gamme du Koilon :")
    for cle, v in r.items():
        print(f"  {cle} : {v}")
