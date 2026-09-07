"""NoeticMachine — le pipeline d'analyse de la Machine Noétique.

Référence reconstruite (07/09/2026) d'après l'extrait de code publié dans
« Analyse Noétique de la Table Périodique Complète » (11/12/2025) :

    from noetic import NoeticMachine
    nm = NoeticMachine(n_dims=1_000_000,
                       spectral_ranks=[150000, 150000, 150000, 200000, 150000,
                                       100000, 100000],
                       beta=0.0434)
    p = nm.project_to_planes(x)          # projection spectrale sur les 7 plans
    d = nm.noetic_distance(p1, p2)       # distance noétique (poids entropiques)
    clusters = nm.noetic_clustering(P)   # groupement par similarité
    anomalies = nm.detect_anomalies(P)   # seuil μ + 3σ

Les signatures publiées sont respectées ; les rangs sont réduits à l'exécution
(locale) : la structure du pipeline ne dépend pas de la taille.
"""

from __future__ import annotations
import numpy as np

RANGS_PUBLIES = [150000, 150000, 150000, 200000, 150000, 100000, 100000]


class NoeticMachine:
    """Pipeline : vecteur d'entrée → projection 7 plans → distance/clustering/anomalies."""

    def __init__(self, n_dims: int = 1_000_000,
                 spectral_ranks: list[int] | None = None,
                 beta: float = 0.0434, graine: int = 20260907,
                 n_local: int = 64, rangs_locaux: list[int] | None = None):
        # Les paramètres publiés sont conservés pour référence ; l'exécution locale
        # utilise des rangs réduits (la structure est indépendante de la taille).
        self.n_dims = n_dims
        self.spectral_ranks = spectral_ranks or RANGS_PUBLIES
        self.beta = beta
        self.n_local = n_local
        self.rangs_locaux = rangs_locaux or [8, 8, 8, 10, 12, 10, 8]  # Σr = n_local
        rng = np.random.default_rng(graine)
        perm = rng.permutation(n_local)
        self.U, pos = [], 0
        for r in self.rangs_locaux:
            U = np.zeros((n_local, r))
            idx = perm[pos:pos + r]
            U[idx, np.arange(r)] = 1.0
            self.U.append(U)
            pos += r
        # poids entropiques (Atomes_2) : w_i = exp(−β ln r_i)
        self.w = np.exp(-beta * np.log(np.array(self.rangs_locaux, float)))

    def encode_element(self, features: np.ndarray) -> np.ndarray:
        """Vecteur d'entrée normalisé x(Z) ∈ R^{n_local} (propriétés normalisées)."""
        x = np.asarray(features, dtype=float)
        if x.size < self.n_local:
            x = np.pad(x, (0, self.n_local - x.size))
        return x[: self.n_local]

    def project_to_planes(self, x: np.ndarray) -> np.ndarray:
        """p_i = U_iᵀ x — la projection spectrale (plans E1–E7)."""
        x = self.encode_element(x)
        return np.concatenate([U.T @ x for U in self.U])

    def noetic_distance(self, p1: np.ndarray, p2: np.ndarray) -> float:
        """D_N(Z1, Z2) = √(Σ_i w_i ‖p_i^(Z1) − p_i^(Z2)‖²) — Atomes_2, §4.1."""
        d2, pos = 0.0, 0
        for i, r in enumerate(self.rangs_locaux):
            a, b = p1[pos:pos + r], p2[pos:pos + r]
            d2 += self.w[i] * float(np.sum((a - b) ** 2))
            pos += r
        return float(np.sqrt(d2))

    def noetic_clustering(self, projections: list[np.ndarray], k: int = 9) -> np.ndarray:
        """Groupement par similarité dans l'espace des plans (k-means, graine figée)."""
        P = np.array(projections)
        rng = np.random.default_rng(20260907)
        centres = P[rng.choice(len(P), k, replace=False)]
        for _ in range(100):
            d = np.linalg.norm(P[:, None, :] - centres[None, :, :], axis=2)
            lab = d.argmin(axis=1)
            nouveaux = np.array([P[lab == j].mean(axis=0) if np.any(lab == j)
                                 else centres[j] for j in range(k)])
            if np.allclose(nouveaux, centres):
                break
            centres = nouveaux
        return lab

    def detect_anomalies(self, projections: list[np.ndarray]) -> np.ndarray:
        """Anomalie si distance noétique moyenne > μ + 3σ (Atomes_2, §4.1)."""
        n = len(projections)
        dist = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    dist[i, j] = self.noetic_distance(projections[i], projections[j])
        moy = dist.sum(axis=1) / (n - 1)
        seuil = moy.mean() + 3 * moy.std()
        return np.where(moy > seuil)[0] + 1  # Z = index + 1
