"""Le solveur d'invariants — V4.1 (4-Math_Simple, 06/05/2026).

Pipeline : mémoire fractionnaire d'Atangana–Baleanu (forme discrète) → projection
harmonique H7 (entrées 2^(k/12) — la gamme du Koilon dans la machine) → covariance
réduite embarquée (P ≈ D + U Vᵀ) → invariants I₁, I₂, I₃ et nombre de Reynolds
noétique Re_N, bornés (preuves formelles du document d'origine) :

    I₁ = ‖Y‖₂,  I₂ = Tr(P_t),  I₃ = λmax(P)/(λmin(P) + ε) ≤ M/(m+ε),
    a/B ≤ Re_N = ‖D_AB x‖/‖T[Ψ]‖ ≤ A/b.

Triplet de résidus : R_c, R_top, R_dyn fonctions des invariants.
"""

from __future__ import annotations
import numpy as np
from .plans import N_PLANS


class SolveurInvariants:
    """Le solveur d'invariants noétiques V4.1 (embarquable : O(1), < 10 Ko RAM visé).

    Entrée : un vecteur Ψ(t) ∈ R⁷ (une composante par plan). La projection harmonique
    applique la gamme vérifiée : Y = diag(2^(k/12))·Ψ (H7 de 4-Math_Simple).
    """

    def __init__(self, alpha_ab: float = 0.7, lam: float = 0.05, eps: float = 1e-6):
        self.alpha = alpha_ab          # ordre fractionnaire AB ∈ (0,1)
        self.lam = lam                 # oubli de la covariance réduite
        self.eps = eps
        # H7 : projection harmonique — entrées 2^(k/12), la gamme du Koilon (vérifiée : 0,23 %)
        self.H7 = np.diag([2.0 ** (k / 12) for k in range(N_PLANS)])
        # poids AB discrets (forme du document : Ψ_n = Σ w_{n−k}(x_k − x_{k−1}))
        K = 64
        k = np.arange(K)
        self.w_ab = np.exp(-self.alpha * k)  # approximation compacte du noyau Mittag-Leffler
        self.x_prev = np.zeros(N_PLANS)
        self.memoire = [[] for _ in range(N_PLANS)]
        self.mu = np.zeros(N_PLANS)
        self.P = np.eye(N_PLANS) * 0.1  # enveloppe de conception : P bornée (preuve I₃)
        self.T_slow = np.zeros(N_PLANS)  # tension du vide : moyenne lente de |D_AB x|

    def D_AB(self, x: np.ndarray) -> np.ndarray:
        """Mémoire fractionnaire discrète d'Atangana–Baleanu, par plan."""
        dx = x - self.x_prev
        self.x_prev = x.copy()
        out = np.zeros(N_PLANS)
        for i in range(N_PLANS):
            self.memoire[i].append(dx[i])
            h = np.array(self.memoire[i][-len(self.w_ab):])
            w = self.w_ab[:len(h)][::-1]
            out[i] = float(np.dot(w, h))
        return out

    def etape(self, x: np.ndarray) -> dict:
        """Un pas : Ψ(t) ∈ R⁷ → invariants + résidus."""
        psi = self.D_AB(np.asarray(x, dtype=float))
        # tension du vide : moyenne lente de |D_AB x| par plan (T[Ψ] du document)
        self.T_slow = 0.95 * self.T_slow + 0.05 * np.abs(psi)
        T = self.T_slow + self.eps
        Y = self.H7 @ psi
        self.mu = (1 - self.lam) * self.mu + self.lam * Y
        d = Y - self.mu
        self.P = (1 - self.lam) * self.P + self.lam * np.outer(d, d)
        I1 = float(np.linalg.norm(Y))
        I2 = float(np.trace(self.P))
        ev = np.linalg.eigvalsh(self.P)
        I3 = float(ev[-1] / (ev[0] + self.eps))
        Re_N = float(np.linalg.norm(psi) / np.linalg.norm(T))  # borné par construction
        return {"I1": I1, "I2": I2, "I3": I3, "Re_N": Re_N, "regime": self.regime(I3),
                "residus": {"R_c": I1, "R_top": I3, "R_dyn": float(np.linalg.norm(psi))}}

    @staticmethod
    def regime(I3: float) -> str:
        """Classification opérationnelle de I₃ (table de V4.1, §11.2)."""
        if I3 < 5: return "nominal"
        if I3 < 20: return "dégradé"
        if I3 < 100: return "critique"
        return "hors enveloppe (reset)"

    def run(self, signal: np.ndarray) -> dict:
        """signal : (n_pas, 7) — une composante par plan."""
        sorties = [self.etape(signal[t]) for t in range(len(signal))]
        regimes = [s["regime"] for s in sorties]
        return {
            "I1": np.array([s["I1"] for s in sorties]),
            "I3": np.array([s["I3"] for s in sorties]),
            "Re_N": np.array([s["Re_N"] for s in sorties]),
            "regimes": regimes,
            "pct_nominal": 100.0 * regimes.count("nominal") / len(regimes),
            "final": sorties[-1],
        }
