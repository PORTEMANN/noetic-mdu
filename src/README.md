# src/ — les versions de la MDU, cohabitant et rejouables

## Structure

```
src/mdu/
  plans.py               — socle commun : 7 plans, S_ent = ln N, Q_ent = e^(−S_ent)
  boucle_v2025_11_24.py  — la boucle itérative d'origine (24/11/2025)
  automate_v4_0.py       — l'automate spectral V4.0 (01/2026)
  solveur_v4_1.py        — le solveur d'invariants V4.1 (06/05/2026)
  donnees.py             — chargeurs : anu_table_2, masses IUPAC, parseur AME2020
  campagnes/
    c_gamme.py           — gamme du Koilon (verdict CONFORME, 0,23 %)
    c_zcalc.py           — simulation aveugle corrigée (CONFORME après correction)
    c_delta.py           — deltaANU (DIVERGENT : tendance vraie, loi fausse)
    c_ilots.py           — îlots 18k+m (CONFORME sous coupure k ≤ 9)
src/compare.py           — les trois versions sur le même signal
data/anu_table_2.csv     — la table officielle (copie de koilon-scale-e8)
```

## Rejouer

```bash
pip install numpy
python src/compare.py                          # les trois versions, même entrée
python -m mdu.campagnes.c_gamme                # depuis src/
python -m mdu.campagnes.c_zcalc
python -m mdu.campagnes.c_delta
python -m mdu.campagnes.c_ilots
```

Graine figée partout : 20260907. Les verdicts reproduisent le procès-verbal du 07/09/2026
(`docs/verdicts_locaux_2026-09-07.md`).

## Versions : laquelle pour quoi ?

| Version | Rôle | Quand l'utiliser |
|---|---|---|
| boucle (24/11/2025) | la plus simple | pédagogie, prototype rapide |
| automate V4.0 | l'équation maîtresse discrétisée | dynamiques physiques (fluide/torsion) |
| solveur V4.1 | invariants bornés, preuves formelles | embarqué, certification (DO-178C) — **la plus aboutie** |
