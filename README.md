# noetic-mdu

**MDU — Machine Dynamique Unifiée** : l'entrée *préfiltre / classifieur* de la Machine Noétique, en amont de l'[ASH](https://github.com/PORTEMANN/noetic-ash-corpus) (banque de signaux) et des campagnes ([noetic-machine-complete](https://github.com/PORTEMANN/noetic-machine-complete), banc de verdicts).

> De l'atome au cosmos : une même ossature spectrale (7 plans), des adaptateurs par échelle, des invariants certifiables, et une fiche pré-enregistrée pour chaque verdict.

## Ce qu'est une MDU

Une **Machine Dynamique Unifiée** est un système computationnel défini par sept propriétés (définition de janvier 2026, art. « Systèmes Complexes II », histoire-des-sciences.eu) :

1. une **équation maîtresse géométrique** à dynamique unifiée : D**v**/Dt = −∇P_c + **v**×**T** + ν(S_ent)Δ**v** ;
2. une **incarnation computationnelle directe** (automate spectral) : X_{t+1} = X_t + η(LX_t + MF(X_t) + D(S_ent)) ;
3. une décomposition **multi-échelle** en sept plans spectraux (E1–E7) ;
4. l'information encodée dans la **géométrie interne** des opérateurs ;
5. une **mémoire lente** (rétroaction entropique D(S_ent) ; mémoire fractionnaire d'Atangana–Baleanu) ;
6. la **stabilité énergétique** : Ė = −∫ η(S_ent)|∇v|² dx ≤ 0 (théorème d'énergie, sous hypothèses H1–H5 déclarées) ;
7. la simulation de phénomènes physiques, informationnels et cognitifs dans **un cadre unique**.

## Le contrat d'entrée (préfiltre / classification)

```
objet structuré (atome, composé, caryotype, état cognitif, galaxie)
        │  MDU : échelle (MICRO/MÉSO/MACRO via Re_N) · domaine · plans dominants · adaptateur
        ▼
fiche pré-enregistrée (objet / protocole / falsifieur / prédiction datée)
        ▼
├─ ASH (signaux)  ├─ campagnes P (calculs)  └─ registre canonique (valeurs)
```

L'ASH identifie l'inconnu *parmi les signaux* ; la MDU identifie l'échelle et le domaine *du problème* — et produit la fiche qui rend le verdict possible.

## Premiers verdicts locaux (07/09/2026)

Calculs rejoués sur la table officielle `anu_table_2.csv` ([koilon-scale-e8](https://github.com/PORTEMANN/koilon-scale-e8)) et les masses IUPAC/AME2020 :

| Fiche | Verdict | Chiffre |
|---|---|---|
| C-GAMME | **CONFORME** | moyenne géométrique des k(i) = 1,06193 vs 2^(1/12) : écart **0,23 %** (IC 95 % bootstrap : [1,0357 ; 1,1026]) |
| C-ZCALC | **CONFORME après correction** | la « correction fine » écrite : vallée de stabilité SEMF Z = A/(2+0,0155·A^{2/3}) ; médiane **1,15 %** (brute : 7,3 %) |
| C-DELTA | **DIVERGENT** | deltaANU : tendance réelle (r = 0,90), loi publiée fausse (exposant mesuré −0,31 ≠ −1,5 ; R² = 1 non soutenu) |
| C-ILOTS | **CONFORME sous coupure** | îlots 18k+m ≤ 180 avec la règle k ≤ 9 |

Détail : [`docs/verdicts_locaux_2026-09-07.md`](docs/verdicts_locaux_2026-09-07.md). Les divergences sont publiées avec le même rang que les conformités (discipline B3-FAIL).

## État des preuves (honnêteté de la charte ◆◇◈✗)

| Propriété MDU | État |
|---|---|
| 2 Incarnation · 3 Multi-échelle · 4 Encodage | **démontrées** (pipeline en œuvre : atomes, matériaux, cerveau) |
| 6 Stabilité énergétique | **écrite** (théorème d'énergie, sous H1–H5 déclarées) |
| 1 Équation maîtresse (limites) · 5 Mémoire lente mesurée | ◈ — dérivations/mesures publiques à produire |
| 7 Unification | partielle (cognitif validé ; physique : Noeticon-1, 4,7 %) |

## Documents

- [`docs/mdu_formalisation.tex`](docs/mdu_formalisation.tex) — la formalisation LaTeX (compile avec pdfLaTeX, ex. Overleaf) ;
- [`docs/verdicts_locaux_2026-09-07.md`](docs/verdicts_locaux_2026-09-07.md) — les quatre premières fiches et leurs verdicts ;
- [`docs/evolution.md`](docs/evolution.md) — la chronologie documentée de la machine (24/11/2025 → V4.1, 06/05/2026).

## Liens de l'écosystème

- [noetic-ash-corpus](https://github.com/PORTEMANN/noetic-ash-corpus) — la banque de signaux (entrée niveau signal) ;
- [noetic-machine-complete](https://github.com/PORTEMANN/noetic-machine-complete) — les campagnes P0–P48, CAMPAIGNS.md, CONVENTIONS.md ;
- [koilon-scale-e8](https://github.com/PORTEMANN/koilon-scale-e8) — la gamme du Koïlon, E8, Z_max ;
- registre canonique : index.portemann.eu — une valeur = une source unique.

## Licence

MIT — © 2026 Patrice Portemann.
