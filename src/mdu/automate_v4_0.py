"""L'automate cellulaire spectral — V4.0 (Systèmes complexes II, 12/01/2026).

Discrétisation de l'équation maîtresse  Dv/Dt = −∇P_c + v×T + ν(S_ent)Δv :
    X_{t+1} = X_t + η (L X_t + M F(X_t) + D(S_ent))
avec la correspondance continu ↔ discret du document d'origine :
    −∇P_c  → couplage dissipatif L (diffusion/viscosité)
    v×T    → matrice M antisymétrique (torsion/rotation)
    νΔv    → terme νΔx_i
    S_ent  → rétroaction D_i(S) (mémoire lente)

Stabilité (condition du document) : ρ(I + ηA_lin) < 1.
"""

from __future__ import annotations
import numpy as np
from .plans import N_PLANS


class AutomateSpectral:
    """L'automate cellulaire spectral V4.0."""

    def __init__(self, n: int = 64, eta: float = 0.05, nu: float = 0.05,
                 graine: int = 20260907):
        self.n, self.eta, self.nu = n, eta, nu
        rng = np.random.default_rng(graine)
        # L : diffusion (laplacien de ligne, stable)
        L = np.zeros((n, n))
        for i in range(n):
            L[i, i] = -2.0
            L[i, (i - 1) % n] = 1.0
            L[i, (i + 1) % n] = 1.0
        self.L = nu * L
        # M : torsion — antisymétrique pure (conserve l'énergie)
        A = rng.standard_normal((n, n))
        self.M = (A - A.T) / (2 * np.sqrt(n))
        # mémoire lente : S_ent évolue lentement vers l'entropie observée
        self.S_ent = 0.0
        self.tau_memoire = 50.0  # τ ≫ 1 (Mémoire_spectrale)

    def F(self, X: np.ndarray) -> np.ndarray:
        return np.tanh(X)

    def D(self, S_cible: float) -> float:
        """Rétroaction de la mémoire lente : D = (S_cible − S_ent)/τ."""
        return (S_cible - self.S_ent) / self.tau_memoire

    def etape(self, X: np.ndarray, S_cible: float = 0.0) -> np.ndarray:
        dS = self.D(S_cible)
        self.S_ent += dS
        return X + self.eta * (self.L @ X + self.M @ self.F(X) + dS)

    def run(self, X0: np.ndarray, pas: int = 200, S_cible: float = 0.0) -> dict:
        X = X0.copy()
        energie = []
        for _ in range(pas):
            X = self.etape(X, S_cible)
            energie.append(0.5 * float(X @ X))
        return {"X": X, "energie": np.array(energie), "S_ent": self.S_ent}

    def stabilite(self) -> dict:
        """ρ(I + ηA_lin) avec A_lin = L + M·diag(sech²(X)) évalué à X = 0."""
        A_lin = self.L + self.M  # F′(0) = 1
        rho = max(abs(np.linalg.eigvals(np.eye(self.n) + self.eta * A_lin)))
        return {"rho": float(rho), "stable": bool(rho < 1)}
