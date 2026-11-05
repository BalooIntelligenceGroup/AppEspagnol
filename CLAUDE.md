# Parliamo! — appli d'italien pour adultes débutants (branche `italiano`)

Branche ORPHELINE du dépôt AppEspagnol, sans rapport avec `main` (appli d'espagnol pour enfant).
Ne jamais fusionner `italiano` dans `main` ni l'inverse.

Hébergement : Netlify, déploiement de branche (branch deploy) du projet cozy-ganache-5c4ae8.
Adresse : https://italiano--cozy-ganache-5c4ae8.netlify.app
Chaque push sur `italiano` est déployé automatiquement à cette adresse.

## Fichiers
- `index.html` : toute l'appli (niveaux dans `UNITS`, exercices, styles clair/sombre, script).
- `sw.js` : service worker (hors ligne + mises à jour), page en « réseau d'abord ».
- `manifest.webmanifest`, `icon-*.png` : installation sur Android.
- `netlify.toml` : publication de la racine, pas de cache sur index.html et sw.js.

## Règle absolue : ne jamais perdre la progression
- Progression dans `localStorage`, clé `parliamo-v1` (+ copie `parliamo-v1-secours`). Ne jamais renommer.
- Ne jamais changer l'`id` d'un niveau existant.
- Ne jamais changer l'adresse (nom de la branche `italiano` et du projet Netlify).
- Nouveaux niveaux : insérer où l'on veut (`insAfter`) ; `S.opened` empêche tout reverrouillage.

## Publier une nouvelle version
1. Ajouter des niveaux dans un tableau `V2_…` puis `insAfter(...)` / `UNITS.push(...)`.
2. Incrémenter `APP_VERSION`, ajouter le texte dans `NEW_IN` (bandeau affiché une fois).
3. Dans `sw.js`, changer le nom du cache (`parliamo-vN`).
4. Vérifier la syntaxe et tester toutes les leçons (startUnit sur chaque niveau) dans Playwright.
5. Commit + push sur `italiano`.

Voix et micro : `it-IT`. Conseils de prononciation italiens dans `TIPS`. Guide : Giulia (monogramme « G »).
