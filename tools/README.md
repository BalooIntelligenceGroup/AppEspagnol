# Outils de Petit Polyglotte

- `audit_tr.cjs` : contrôle des traductions (fr, en, it) — **à lancer à chaque demande** :
  `python3 -m http.server 8765` à la racine du dépôt, puis `node tools/audit_tr.cjs` (aucun ❌ attendu).
- `tests/` : tests Playwright (`npm i playwright` ou Playwright déjà installé), serveur local sur le port 8765.
  - `tfix.cjs` : ouvre chaque leçon et vérifie chaque exercice (les « Construis la phrase » doivent afficher leurs mots).
  - `t29d.cjs` : les 60 leçons en anglais, italien et espagnol avec un code bêta.
  - `t29c.cjs` : offre gratuite (Niveaux 1 et 2), Niveau 3 gardé pour les anciens joueurs, abonnés.
  - `t29b.cjs`, `t28.cjs`, `t27c.cjs`, `trand.cjs`, `tbeta.cjs`, `tnew.cjs`, `tstart.cjs` : Famille, bonus, langues, ordre aléatoire, bandeau de version, premier écran.
  - Les tests qui saisissent un code bêta le lisent dans la variable `BETA_CODE` (les codes ne sont jamais écrits dans le dépôt) :
    `BETA_CODE=XXXXXX node tools/tests/t29d.cjs`
- `sources/` : sources du contenu (Python) et scripts de modification qui ont servi à écrire chaque version
  (`content_v*.py` = textes des leçons, traductions, récitations ; `patch_v*.py` = modifications appliquées à `index.html`).
  Le contenu fait foi dans `index.html` ; ces fichiers servent de référence pour écrire la suite.
- `icon.svg`, `icon-maskable.svg` : sources de l'icône (police Baloo 2).
