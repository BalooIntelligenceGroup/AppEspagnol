# ¡Hola Lola! — appli d'espagnol pour une enfant de 8 ans

Appli web installable (PWA) hébergée sur Netlify : https://cozy-ganache-5c4ae8.netlify.app
Chaque push sur `main` est déployé automatiquement par Netlify.

## Fichiers
- `index.html` : toute l'appli (contenu des niveaux, exercices, styles, script).
- `sw.js` : service worker (hors ligne + mises à jour). Page en « réseau d'abord ».
- `manifest.webmanifest`, `icon-*.png` : installation sur Android.
- `netlify.toml` : publication de la racine, pas de cache sur index.html et sw.js.

## Règle absolue : ne jamais perdre la progression
- La progression est dans `localStorage`, clé `hola-lola-v1` (+ copie `hola-lola-v1-secours`). Ne jamais renommer ces clés.
- Ne jamais changer l'`id` d'un niveau existant (les étoiles sont rangées par id).
- Ne jamais changer l'adresse du site Netlify (l'origine porte les données).
- Nouveaux niveaux : on peut les insérer n'importe où ; `S.opened` et `LEGACY` garantissent qu'un niveau déjà ouvert ne se reverrouille pas.

## Niveaux affichés (depuis la version 11)
- Seuls les 15 niveaux listés dans `ACTIVE` sont affichés (5 par étape). Les autres restent dans le code, et leurs étoiles dans la sauvegarde.
- Pour réafficher ou changer un niveau : modifier la liste `ACTIVE` (l'ordre de la liste = l'ordre sur la carte).

## Publier une nouvelle version
1. Modifier `index.html` (ajouter des niveaux dans un tableau `V8_…` puis `insAfter(...)`, comme V7).
2. Incrémenter `APP_VERSION` et ajouter le texte de nouveauté dans `NEW_IN` (bandeau affiché une fois).
3. Dans `sw.js`, changer le nom du cache (`hola-lola-vN`).
4. Vérifier la syntaxe du script et tester toutes les leçons (startUnit sur chaque niveau) dans Playwright.
5. Commit + push sur `main` → Netlify déploie, le téléphone se met à jour à la prochaine ouverture.

Le même contenu est aussi publié comme artefact Claude : c'est `index.html` sans l'en-tête PWA
ni le script d'enregistrement du service worker. Dans l'artefact, le micro est bloqué (mode « répéter à voix haute »).
