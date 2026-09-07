"""La décomposition spectrale en sept plans — socle commun des versions MDU.

Références : Plans_Noétiques (24/11/2025) ; PFPN V (22/10/2025) ; Systèmes complexes I/II (01/2026).
"""

from __future__ import annotations
import numpy as np

N_PLANS = 7


def entropie_spectrale(n_classe: float) -> float:
    """S_ent = ln(N_classe) — entropie spectrale d'un plan (PFPN V)."""
    return float(np.log(n_classe))


def charge_entropique(n_classe: float) -> float:
    """Q_ent = e^(−S_ent) = 1/N_classe — charge entropique (PFPN V)."""
    return float(np.exp(-entropie_spectrale(n_classe)))


def poids_entropiques(rangs: np.ndarray, beta: float = 0.5) -> np.ndarray:
    """w_i ← w_i · exp(−β·ln r_i) — amortissement entropique (Plans_Noétiques__computation_)."""
    rangs = np.asarray(rangs, dtype=float)
    return np.exp(-beta * np.log(rangs))


def projecteurs(n: int, rangs: list[int], graine: int = 20260907) -> list[np.ndarray]:
    """Bases réduites U_i ∈ R^{n×r_i} orthonormales et **disjointes** (Σr_i ≤ n — condition
    du document d'origine ; « bases identitaires » du cas d'étude 1).

    En production : PCA locale / vecteurs propres du Laplacien / vecteurs propres de D —
    cf. Plans_Noétiques__computation_.pdf §8. Ici : partition identité reproductible (graine figée).
    """
    assert sum(rangs) <= n, "Σr_i ≤ n requis (document d'origine)"
    rng = np.random.default_rng(graine)
    perm = rng.permutation(n)
    bases, pos = [], 0
    for r in rangs:
        U = np.zeros((n, r))
        idx = perm[pos:pos + r]
        U[idx, np.arange(r)] = 1.0
        bases.append(U)
        pos += r
    return bases


def decomposition(x: np.ndarray, bases: list[np.ndarray]) -> list[np.ndarray]:
    """p_i = U_i^T x — projection modale sur les 7 plans."""
    return [U.T @ x for U in bases]


def reconstruction(p: list[np.ndarray], bases: list[np.ndarray]) -> np.ndarray:
    """x = Σ_i U_i p_i — reconstruction modale."""
    return sum(U @ pi for U, pi in zip(bases, p))
