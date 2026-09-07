# Campagnes locales MDU — procès-verbal du 07/09/2026

## Premiers verdicts locaux — contenu fondateur de l'entrée noetic-mdu

**Cadre :** calculs exécutés localement le 07/09/2026 sur la table officielle de l'écosystème (`anu_table_2.csv`, dépôt koilon-scale-e8, 92 éléments H→U) et les masses standard IUPAC/AME2020, puis publiés ici comme contenu fondateur du dépôt. Format des fiches : objet / protocole / prédiction pré-enregistrée / falsifieur / verdict daté — le modèle CAMPAIGNS.md.

---

## Fiche C-GAMME — la gamme du Koilon

**Objet.** La moyenne des rapports k(i) = N_ANU(Z)/N_ANU(Z−1) sur la table officielle (92 éléments) face à 2^(1/12).
**Protocole.** Moyenne géométrique des 91 rapports ; intervalle de confiance bootstrap (20 000 réplicats, graine figée 20260907).
**Prédiction pré-enregistrée.** La moyenne géométrique tombe à moins de 0,5 % de 2^(1/12).
**Falsifieur.** Écart ≥ 0,5 %, ou cible hors de l'IC 95 %.
**Verdict (07/09/2026) : CONFORME.** Estimation 1,061933 ; cible 1,059463 ; **écart 0,23 %** ; IC 95 % bootstrap [1,0357 ; 1,1026] — la cible est dedans. Précision de convention : il s'agit de la moyenne **géométrique** (l'arithmétique dérive à 2,1 %) ; dans la plage Z = 11–30 (affirmation de l'article 12327) : 0,2 %.
**Conséquence.** La gamme est réintégrable dans la MDU comme fait calculé ◆, avec la convention « moyenne géométrique » écrite.

## Fiche C-ZCALC — la simulation aveugle, corrigée

**Objet.** La formule Z_calc = A/[2(1+0,006·A^0,6)] d'atomes_3, et sa « correction fine » appliquée à la main dans l'article (U : 102,6 → 91,7).
**Protocole.** (a) Formule brute sur les 92 éléments ; (b) correction fine **formalisée** : la vallée de stabilité standard du modèle semi-empirique, Z = A/(2 + (a_C/2a_sym)·A^(2/3)) avec a_C = 0,72 MeV, a_sym = 23,2 MeV (coefficient 0,0155) ; distribution complète des erreurs dans les deux cas.
**Prédiction pré-enregistrée.** La version corrigée atteint une erreur médiane < 5 % sur les 92 éléments.
**Falsifieur.** Médiane ≥ 5 %, ou correction impossible à écrire.
**Verdict (07/09/2026) : CONFORME après correction.** Formule brute : médiane **7,3 %** (casse H/He et les actinides — l'affirmation « < 5 % » de l'article ne tient pas). Version corrigée SEMF : **médiane 1,15 %**, 80/92 sous 5 %, 90/92 sous 10 % ; **U : 91,7 — exactement la valeur que l'article obtenait à la main**. Domaine : A ≥ 4 (l'hydrogène, sans neutron, est hors vallée — à exclure explicitement).
**Conséquence.** La « correction fine » existe et s'écrit : c'est la vallée de stabilité du SEMF. La simulation aveugle devient rejouable et réintégrable — avec la table complète des résidus publiée et le domaine déclaré.

## Fiche C-DELTA — deltaANU

**Objet.** deltaANU = 137·Z^(−3/2), présenté (5677/4014) comme l'écart relatif à 2^(1/12) avec R² = 1.
**Protocole.** Écart réel |k − 2^(1/12)|/2^(1/12) calculé sur les 91 rapports ; ré-ajustement en loi de puissance libre ; corrélation avec le modèle publié.
**Prédiction pré-enregistrée.** Si la loi est juste : pente ≈ −1,5, amplitude ≈ 137, R² élevé.
**Falsifieur.** Pente, amplitude ou R² hors de ces bornes.
**Verdict (07/09/2026) : DIVERGENT — la tendance survit, la loi tombe.** Mesuré : pente **−0,31** (pas −1,5), amplitude 0,100 (pas 137 — surestimation ×14), R² log-log 0,05 (pas 1). Mais la **corrélation monotone est forte : r = 0,90** — l'écart relatif décroît bien avec Z. Formulation honnête : deltaANU est une **tendance**, pas une loi ajustée ; l'affichage R² = 1 est à retirer des futures versions (addendum daté, le jour où des modifications publiques seront décidées).

## Fiche C-ILOTS — les îlots de stabilité 18k + m

**Objet.** La formule Z_stable = 18k + m (m ∈ {0, 6, 12}) d'Atomes_2 (îlots cités : 126, 132, 150, 156) face à la limite causale Z_max ≈ 179–180.
**Protocole.** Énumération complète, sans et avec coupure k ≤ 9 (imposée par c_s ≤ c) ; confrontation qualitative à la littérature des superlourds.
**Prédiction pré-enregistrée.** Les îlots cités sont < Z_max ; la formule avec coupure ne produit rien au-delà de 180.
**Falsifieur.** Un îlot prédit > 180, ou incohérence avec Z_max.
**Verdict (07/09/2026) : CONFORME sous coupure.** Sans coupure, la formule déborde (186, 192, 198, 204, 210 ✗). Avec k ≤ 9 : îlots 96, 102, 108, **114, 120, 126**, 132, 138, 144, 150, 156, 162, 168, 174 — tous ≤ 180 ✓. 114 (région du flérovium) et 164 (îlot historique discuté) figurent dans la liste ; 132/138/150/156 sont des prédictions propres au modèle (non magiques standard) — à marquer ◈.
**Conséquence.** Réintégrable dans la MDU **avec la coupure k ≤ 9 écrite** — la cohérence avec Z_max est alors structurelle.

---

## Synthèse locale

| Fiche | Verdict | Statut produit |
|---|---|---|
| C-GAMME | **CONFORME** (0,23 % ; IC 95 % couvre la cible) | fait calculé ◆ (avec convention « moyenne géométrique ») |
| C-ZCALC | **CONFORME après correction** (7,3 % → 1,15 % ; U = 91,7) | méthode rejouable ◇ (résidus complets à publier le jour venu) |
| C-DELTA | **DIVERGENT** — tendance vraie (r = 0,90), loi publiée fausse | correction à dater ; deltaANU devient « tendance » |
| C-ILOTS | **CONFORME sous coupure k ≤ 9** | modèle ◇ avec règle de coupure |

Deux verdicts conformes, un conforme après correction, un divergent — **publiés avec la même rigueur, conformément à la discipline de l'écosystème (B3-FAIL : les divergences ont le même rang que les conformités)**.

*Procès-verbal établi le 07/09/2026. Calculs rejoués sur `anu_table_2.csv` (92 éléments) et masses IUPAC/AME2020 ; bootstrap à graine figée.*
