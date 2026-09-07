"""demo_table.py — la machine sur la table périodique (données publiques embarquées).

Rejoue la structure du rapport « Analyse Noétique de la Table Périodique » (11/12/2025)
sur les grandeurs publiques vérifiées : Z, N_ANU (table officielle koilon-scale-e8),
A dominant et poids standard (IUPAC). Features réduites et déclarées — l'analyse
d'origine utilisait une base étendue (ionisation, rayons, électronégativité…) non
publiée ; voir la note F10 dans src/noetic/__init__.py.

Usage : PYTHONPATH=src python src/noetic/demo_table.py
"""

from __future__ import annotations
import numpy as np

from noetic import NoeticMachine
from mdu.donnees import DATA_DEFAUT, charger_anu, masses_dominantes


def main() -> None:
    Z, N_ANU, sym = charger_anu(str(DATA_DEFAUT))
    A, M = masses_dominantes(Z)
    # Features normalisées (déclarées) : Z, N_ANU/18, A, M — échelles log pour la portée
    feats = np.stack([np.log(Z), N_ANU / 18.0 / 100.0, np.log(A), np.log(M)], axis=1)
    nm = NoeticMachine()
    P = [nm.project_to_planes(feats[i]) for i in range(len(Z))]
    anomalies = nm.detect_anomalies(P)
    noms = [sym[i - 1] for i in anomalies]
    print("=== NoeticMachine (référence reconstruite) — table périodique ===")
    print(f"éléments : {len(Z)} | projections : {P[0].size} composantes "
          f"({len(nm.rangs_locaux)} plans)")
    print(f"anomalies détectées (seuil μ + 3σ) : {len(anomalies)} → {noms}")
    clusters = nm.noetic_clustering(P)
    print(f"clusters (k=9) : tailles {np.bincount(clusters)}")
    print("\nContrôle de cohérence : H est-il anomal ?",
          "OUI" if 1 in anomalies else "non",
          "| les lourds (Z ≥ 84) :", [s for s in noms if Z[list(sym).index(s)] >= 84])


if __name__ == "__main__":
    main()
