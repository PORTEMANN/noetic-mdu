"""Chargeurs de données publiques pour les campagnes rejouables.

Sources (toutes libres) :
- anu_table_2.csv : la table n°2 de la Chimie Occulte (dépôt koilon-scale-e8) —
  Z, symbole, N_ANU pour les 92 éléments H→U ;
- masses standard IUPAC (table embarquée minimale ci-dessous) ;
- AME2020 (IAEA, https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt) —
  parseur à colonnes fixes (format mas20).
"""

from __future__ import annotations
import io
from pathlib import Path
import numpy as np

DATA_DEFAUT = Path(__file__).resolve().parents[2] / "data" / "anu_table_2.csv"

# Poids atomiques standards IUPAC et isotope dominant (Z = 1..92) — table embarquée.
STD = {1:(1,1.008),2:(4,4.003),3:(7,6.94),4:(9,9.012),5:(11,10.81),6:(12,12.011),
7:(14,14.007),8:(16,15.999),9:(19,18.998),10:(20,20.180),11:(23,22.990),
12:(24,24.305),13:(27,26.982),14:(28,28.085),15:(31,30.974),16:(32,32.06),
17:(35,35.45),18:(40,39.948),19:(39,39.098),20:(40,40.078),21:(45,44.956),
22:(48,47.867),23:(51,50.942),24:(52,51.996),25:(55,54.938),26:(56,55.845),
27:(59,58.933),28:(58,58.693),29:(63,63.546),30:(64,65.38),31:(69,69.723),
32:(74,72.630),33:(75,74.922),34:(80,78.971),35:(80,79.904),36:(84,83.798),
37:(85,85.468),38:(88,87.62),39:(89,88.906),40:(90,91.224),41:(93,92.906),
42:(98,95.95),43:(98,98.0),44:(102,101.07),45:(103,102.91),46:(106,106.42),
47:(107,107.87),48:(114,112.41),49:(115,114.82),50:(120,118.71),51:(121,121.76),
52:(130,127.60),53:(127,126.90),54:(132,131.29),55:(133,132.91),56:(138,137.33),
57:(139,138.91),58:(140,140.12),59:(141,140.91),60:(144,144.24),61:(145,145.0),
62:(152,150.36),63:(153,151.96),64:(158,157.25),65:(159,158.93),66:(164,162.50),
67:(165,164.93),68:(166,167.26),69:(169,168.93),70:(174,173.05),71:(175,174.97),
72:(180,178.49),73:(181,180.95),74:(184,183.84),75:(187,186.21),76:(192,190.23),
77:(193,192.22),78:(195,195.08),79:(197,196.97),80:(202,200.59),81:(205,204.38),
82:(208,207.2),83:(209,208.98),84:(209,209.0),85:(210,210.0),86:(222,222.0),
87:(223,223.0),88:(226,226.0),89:(227,227.0),90:(232,232.04),91:(231,231.04),
92:(238,238.03)}


def charger_anu(path: str) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Lit anu_table_2.csv → (Z, N_ANU, symboles)."""
    Z, N, sym = [], [], []
    with io.open(path, encoding='utf-8') as fh:
        lignes = [l.strip() for l in fh if l.strip()]
    for l in lignes[1:]:
        z, s, n = l.split(',')
        Z.append(int(z)); sym.append(s); N.append(int(n))
    return np.array(Z), np.array(N), sym


def masses_dominantes(Z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(A dominant, poids standard) pour chaque Z."""
    return (np.array([STD[z][0] for z in Z], float),
            np.array([STD[z][1] for z in Z], float))


def parser_ame2020(path: str) -> list[tuple[int, int, int, str, float, float]]:
    """Parse le format mas20 (colonnes fixes) → [(N, Z, A, el, mass_excess_keV, BE/A_keV)]."""
    out = []
    with io.open(path, encoding='latin-1') as fh:
        for line in fh:
            try:
                N = int(line[5:9]); Z = int(line[10:14]); A = int(line[15:19])
                el = line[20:23].strip()
                me = float(line[29:40]); beA = float(line[57:67])
                out.append((N, Z, A, el, me, beA))
            except (ValueError, IndexError):
                continue
    return out
