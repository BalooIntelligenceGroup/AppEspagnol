# Ahla bik — appli de tunisien (derja) pour adultes débutants (branche `tounsi`)

Branche ORPHELINE du dépôt AppEspagnol, sans rapport avec `main` (espagnol) ni `italiano`.
Ne jamais fusionner les branches entre elles.

Hébergement : Netlify, déploiement de branche (branch deploy) du projet cozy-ganache-5c4ae8.
Adresse : https://tounsi--cozy-ganache-5c4ae8.netlify.app — chaque push sur `tounsi` y est déployé.

## Particularités
- Tunisien en lettres latines : 3 = ع, 7 = ح, 9 = ق, kh = خ, gh = غ, ch = ش (écran « Les sons », tableau `SOUNDS`).
- Voix, par ordre de priorité : 1) enregistrements du Studio sur l'appareil, 2) vraie voix en ligne (`audio/<hash>.webm`, liste `audio/index.json`),
  3) voix de synthèse Microsoft « arabe de Tunisie » (`audio/tts/<hash>.mp3`, liste `audio/tts/index.json`).
- Voix de synthèse : `tts/phrases.json` associe chaque phrase latine (`t`) à son écriture arabe (`ar`, c'est ce que la voix lit).
  Le workflow `.github/workflows/voix.yml` (GitHub Actions, edge-tts, voix ar-TN-ReemNeural) régénère les fichiers à chaque push
  qui touche `tts/`, puis les commit sur `tounsi`. Toute nouvelle phrase de l'appli doit être ajoutée à `tts/phrases.json` avec son arabe.
- Vraies voix : ENREGISTREMENTS d'une personne tunisienne.
  - Studio (Réglages → Studio d'enregistrement) : enregistre chaque phrase, stockage IndexedDB `ahla-studio`.
  - Export : un .zip contenant `<hash>.webm` + `index.json` ([{h, t}]).
  - Mise en ligne : copier les `.webm` dans `audio/` et fusionner la liste dans `audio/index.json` (garder les entrées existantes, dédoublonner par `h`).
  - `hash` = FNV-1a 32 bits du texte exact de la phrase (`hashOf` dans index.html). Si on corrige le texte d'une phrase, son hash change : il faudra la réenregistrer.
  - Les phrases contenant `{name}` ne sont pas enregistrées (restent écrites).
- Micro : auto-évaluation (s'enregistrer, réécouter le modèle et soi, se noter). « À retravailler » = non validé, reproposé en fin de leçon.

## Règle absolue : ne jamais perdre la progression
- Progression dans `localStorage`, clé `ahla-v1` (+ `ahla-v1-secours`). Ne jamais renommer.
- Ne jamais changer l'`id` d'un niveau existant, ni le nom de la branche `tounsi`.
- Nouveaux niveaux : `insAfter` / `UNITS.push` ; `S.opened` empêche tout reverrouillage.

## Publier une nouvelle version
1. Modifier `index.html` ; incrémenter `APP_VERSION` + texte dans `NEW_IN`.
2. Dans `sw.js`, changer le nom du cache (`ahla-vN`).
3. Vérifier la syntaxe et tester toutes les leçons dans Playwright (Chromium avec faux micro : --use-fake-device-for-media-stream).
4. Commit + push sur `tounsi`.
