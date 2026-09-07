"""La boucle itérative d'origine — 24/11/2025 (Plans_Noétiques__computation_.pdf).

La plus ancienne incarnation de la MDU : projection sur 7 plans → opérateurs locaux
F_i = U_i(L̃_i p_i + N_i(p_i)) → agrégation pondérée → mise à jour x ← x + η·y.

Critères du document d'origine : stabilité locale ρ(J) < 1 au point fixe ; condition
suffisante de contraction ; régularisation Tikhonov sur L̃_i ; amortissement entropique
des poids.
"""

from __future__ import annotations
import numpy as np
from .plans import N_PLANS, projecteurs, poids_entropiques


class BoucleNoetique:
    """La boucle à plans noétiques de novembre 2025."""

    def __init__(self, n: int = 64, rangs: list[int] | None = None, eta: float | None = None,
                 beta: float = 0.5, lam: float = 1e-4, gamma: float = 0.4,
                 graine: int = 20260907):
        self.n = n
        self.rangs = rangs or [8, 8, 8, 10, 12, 10, 8]  # Σr_i = 64 = n (condition du document)
        self.beta, self.lam = beta, lam
        # gamma : dissipation −Γx (Documentation technique du 17/01/2026, annexe A.1) —
        # elle doit dominer le gain local : γ > max_i w_i(1 + λ_max(L̃_i)) (γ = 0,4 par défaut)
        self.gamma = gamma
        self.rng = np.random.default_rng(graine)
        self.U = projecteurs(n, self.rangs, graine)
        # L̃_i : diagonales stables (document d'origine, §8 : « matrices diagonales stables »)
        self.L = [np.diag(self.rng.uniform(-0.10, -0.01, r)) for r in self.rangs]
        # M : inter-plans (E4→E5 fort, E5→E6 moyen — cas d'étude 1)
        self.M = np.zeros((N_PLANS, N_PLANS))
        self.M[4, 3], self.M[5, 4] = 0.8, 0.6
        self.w = poids_entropiques(np.array(self.rangs, float), beta)
        # η auto-conservatif (extension « boucle adaptative » du document) : η·λ_max(G) ≈ 0,4
        G = self._gain_lineaire()
        self.eta = float(eta) if eta is not None else 0.4 / max(abs(np.linalg.eigvals(G)).max(), 1e-9)

    def _gain_lineaire(self) -> np.ndarray:
        """Gain linéarisé G = Σ_i w_i U_i(L_i + I)U_iᵀ − γI (tanh′(0) = 1)."""
        G = -self.gamma * np.eye(self.n)
        for i in range(N_PLANS):
            G = G + self.w[i] * self.U[i] @ (self.L[i] + np.eye(self.rangs[i])) @ self.U[i].T
        return G

    def F_local(self, i: int, p: np.ndarray) -> np.ndarray:
        """F_i = L̃_i p_i + N_i(p_i) ; N_i = tanh (non-linéarité saturante, cf. Cognition_2)."""
        return self.L[i] @ p + np.tanh(p)

    def etape(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Une itération : retourne (x_new, contributions par plan c_i)."""
        p = [self.U[i].T @ x for i in range(N_PLANS)]
        y_r = [self.F_local(i, p[i]) for i in range(N_PLANS)]
        y = sum(self.w[i] * (self.U[i] @ y_r[i]) for i in range(N_PLANS))
        c = np.array([np.linalg.norm(self.U[i] @ y_r[i]) for i in range(N_PLANS)])
        return x + self.eta * (y - self.gamma * x), c

    def run(self, x0: np.ndarray, max_iter: int = 500, tol: float = 1e-8) -> dict:
        """Boucle jusqu'à convergence (‖Δx‖ < tol) — diagnostics inclus."""
        x = x0.copy()
        histoire_c, normes = [], []
        for t in range(max_iter):
            x_new, c = self.etape(x)
            d = np.linalg.norm(x_new - x)
            histoire_c.append(c)
            normes.append(d)
            x = x_new
            if d < tol:
                break
        return {"x": x, "iterations": t + 1, "converge": bool(d < tol),
                "contributions": np.array(histoire_c), "normes": np.array(normes)}

    def rayon_spectral_jacobienne(self, x: np.ndarray) -> float:
        """ρ(J) estimé par itérations de puissance sur la jacobienne réduite (diagnostic §7.2)."""
        eps = 1e-6
        v = self.rng.standard_normal(self.n)
        for _ in range(50):
            Jv = ((self.etape(x + eps * v)[0] - self.etape(x)[0]) / eps)
            nrm = np.linalg.norm(Jv)
            if nrm == 0:
                return 0.0
            v = Jv / nrm
        lam = np.linalg.norm((self.etape(x + eps * v)[0] - self.etape(x)[0]) / eps)
        return float(lam)
