# ¡Hola Lola! — appli d'espagnol pour une enfant de 8 ans

Appli web installable (PWA) hébergée sur Netlify : https://cozy-ganache-5c4ae8.netlify.app
Chaque push sur `main` est déployé automatiquement par Netlify.

## Fichiers
- `index.html` : toute l'appli (contenu des niveaux, exercices, styles, script).
- `sw.js` : service worker (hors ligne + mises à jour). Page en « réseau d'abord ».
- `manifest.webmanifest`, `icon-*.png` : installation sur Android.
- `fx/` : images 3D Fluent Emoji (Microsoft, licence MIT dans `fx/LICENSE`), une par émoji, nommées par code (`1f436.webp`). Un MutationObserver (`fxify`) remplace à l'affichage chaque émoji qui a son image ; `FX` (index.html) et `FXL` (sw.js) listent les images. Nouvel émoji → ajouter son image et sa clé dans les deux listes, sinon l'émoji du téléphone reste.
- `netlify.toml` : publication de la racine, pas de cache sur index.html et sw.js.

## Règle absolue : ne jamais perdre la progression
- La progression est dans `localStorage`, clé `hola-lola-v1` (+ copie `hola-lola-v1-secours`). Ne jamais renommer ces clés.
- Ne jamais changer l'`id` d'un niveau existant (les étoiles sont rangées par id).
- Ne jamais changer l'adresse du site Netlify (l'origine porte les données).
- Nouveaux niveaux : on peut les insérer n'importe où ; `S.opened` et `LEGACY` garantissent qu'un niveau déjà ouvert ne se reverrouille pas.

## Organisation (depuis la version 12)
- **Niveaux** : seuls les 15 niveaux de `ACTIVE` sont affichés ; l'étape = la place dans `ACTIVE` (5 par étape). `DROP` retire un mot par niveau (5 mots par leçon). Les autres niveaux et mots restent dans le code.
- **Évaluation de fin d'étape** : 12 questions, 80 % pour ouvrir le 1er niveau de l'étape suivante (`S.evals[étape]`). Un niveau déjà ouvert ou réussi ne se reverrouille jamais (`S.opened`).
- **Profils** : liste dans `hola-lola-profiles` ; le profil `p1` garde la clé d'origine `hola-lola-v1`, les autres `hola-lola-v1-<id>` (+ `-secours`). Ne jamais renommer ces clés.
- **Univers** (`THEMES`) : 6 univers (3 proposés aux filles, 3 aux garçons, tous accessibles), couleurs + compagnon. « Lola » dans les dialogues est remplacée par le nom du compagnon ; accords fille/garçon via `gx()`.
- **Révision espacée** : `S.words[mot] = {b, d, ok, ko}` ; la Séance du jour prend les mots dus (`dueList`). Temps passé : `S.days`.
- **Espace parent** : protégé par le **code parent** à 4 chiffres (v22, un par téléphone, clé `hola-lola-pin`, empreinte `pinHash`), créé sur l'écran `tsetup` ou au premier accès ; sans code ou « Code oublié ? » : multiplication à 2 chiffres × 2 chiffres puis nouveau code. `openGate(next)` / `gatePass()` ; protège aussi « Recommencer à zéro » et le choix du joueur quand le temps est écoulé.

## Côté ludique (depuis la version 13)
- **Pièces** `S.coins` (leçons, séance, évaluations, jeux, comptines, défis) et **points de la semaine** `S.wk={k,pts}` via `addPts()` (classement familial, remis à zéro le lundi).
- **Histoire** `STORY[id du niveau]` : un épisode de 3 cases s'ouvre quand le niveau est réussi.
- **Album** : un autocollant par mot réussi 3 fois (`S.words[mot].ok>=3`).
- **Garde-robe** `ACC` : accessoires achetés (`S.owned`) et portés (`S.acc`), dessinés par `avatar()`.
- **Jeux** (catch, memory, chrono) sur les mots déjà vus ; **Défi famille** (duel) contre un autre profil ou un parent, gains écrits dans l'autre profil par `editProfile()`.
- **Comptines** `SONGS` (karaoké), chacune ouverte par un niveau.
- **Limite par jour** `S.limit` (minutes, réglée dans l'espace parent), `S.unlockDay` pour débloquer ; `guard()` avant chaque activité.
- **Boutons retour** : chaque écran a un ←/✕ ; l'accueil d'un joueur suit `wStep` (prénom → fille/garçon → univers) avec retour à chaque étape.
- **Traductions** (v15) : `tr(es)` cherche la phrase dans les dialogues (`d.f`, `o[1]`) puis dans `FR_EXTRA` (phrases à trou et dialogues sans français). Toute nouvelle phrase à trou ou réplique doit y avoir sa traduction. L'encadré « Continuer » affiche `trBox()` ; le bouton « Traduire » sur les questions dépend de `S.trQ` (réglé par profil dans l'espace parent), jamais en évaluation.
- **Mots abstraits** (v16) : `ABSTRACT` (gracias, hola, ¿qué es?…) affiche le mot français à la place de l'image (`txt:` dans `w.e`, rendu par `pic()`).
- **Langue de l'appli** (v18) : `S.lang` = fr (défaut), en ou it, choisie au tout premier écran d'un nouveau profil (`wStep='lang'`) et modifiable dans l'espace parent. L'interface est écrite en français et traduite à l'affichage : `uiT()` cherche le texte dans `UI` (clé française où nombres, prénoms, noms des compagnons et texte entre « » deviennent {0}, {1}…) puis dans les motifs `UIP`. **Tout nouveau texte français affiché doit avoir son entrée dans `UI`**, sinon il reste en français. Traductions des contenus : `tx(es, fr)` cherche dans `TRX[espagnol] = [anglais, italien]` (les 15 leçons actives), sinon garde le français. Toute nouvelle phrase ou mot doit avoir son entrée dans `TRX`.
- **Noms** (v17) : à l'écran, une « étape » s'appelle **Niveau** (`TIERS`) et un niveau s'appelle **Leçon** ; les comptines sont des **Récitations**. Le code garde ses noms (UNITS, tier, SONGS).
- **Temps d'écran** (v17, corrigé v20) : compté en direct par `timeTick()` (toutes les 10 s, hors écrans `FREE` et réglages), comparé en secondes. Choisir une limite annule le déblocage du jour et les minutes ajoutées. L'écran `stop` n'offre que « Je suis un parent ». Si un profil a fini son temps (`anyOver()`), choisir ou créer un joueur sur « ¿Quién juega? » passe par la multiplication (`gateNext`). Limite atteinte → écran `stop` partout (« Demande à tes parents »), le parent ajoute 15 min (`S.extra`) ou débloque la journée (`S.unlockDay`).
- **Rythme quotidien** (v22) : `newGate(i)` bloque une leçon jamais réussie si une nouvelle leçon a déjà été réussie aujourd'hui (`S.newDay`) ou si des mots sont à revoir et que la Séance du jour n'est pas faite (`S.seanceDay`). Les leçons déjà réussies restent libres. Limite par défaut : 15 min/jour (`def()`, migration `mig22` si aucun réglage). Au-delà de 15 min (ou sans limite), `limitBox()` affiche un avertissement : appli conçue pour limiter le temps d'écran de façon préventive, le parent reste seul décideur.
- **Didacticiel** `tuto()` : montré une fois par profil (`S.tuto`), revisible dans les réglages. À la fin du premier didacticiel, écran `tsetup` : le parent choisit le temps d'écran (`S.tsetup`).
- **10 mots par leçon** (v22) : les mots retirés par `DROP` reviennent et `MORE` ajoute 4 mots par leçon active. Une leçon déjà réussie fait découvrir les mots jamais vus. Mot sans bonne image → `💬` + entrée dans `ABSTRACT`.
- **Voix** (v22) : `S.voice` (voiceURI d'une voix espagnole du téléphone, liste `esVoices()`) et `S.pitch` (n/h/l, table `PITCH`), dans les réglages.
- **Espace parent** (v22) : un `<details class="acc">` par enfant (Progrès / Réglages), `popen` garde les accordéons ouverts ; `limitBox()` sert aussi à `tsetup` ; `PROMISE` = message « notre engagement ».
- **Boutique** (v23) : `ACC` (head, face, neck, hand, fx), `SKINS` (classe `sk-…` sur `.ava`, `S.skin`/`S.skins`), univers : `freeThemes()` = 2 premiers de `THEME_FOR[sexe]`, les autres à `THEME_PRICE` pièces (`S.ownT`, l'univers déjà choisi reste acquis). `spend(prix)` débite ou prépare le message « il te manque… ». Onglets `shopTab`. « Changer d'univers » des réglages ouvre l'onglet Univers.
- **Jeux** (v23) : `GAMES` (catch, memory, chrono offerts ; letters et tfx à acheter, `S.gOwned`), `DECORS` (`S.decor`, classe `deco-…` sur `.stage`), `BONUS` consommables (`S.bonus` : time, shield, hint) qui n'ajoutent jamais de temps d'écran.
- **Voix** (v23) : « Qui parle ? » = `S.pitch` n/h/m/g (femme, fille, homme, homme grave) via `PITCH` et `RATEK` ; langue par défaut = langue du système (`sysLang()`).
- **Ordre des exercices** : `mix()` mélange les exercices après la découverte des mots et évite de rejouer le même enchaînement (`S.seq`).
- **Carte** : à l'arrivée sur l'accueil, défilement automatique vers la leçon en cours ; bouton `#totop` pour remonter.
- Révision espacée : un mot n'avance d'une boîte que s'il était dû (`r.d<=aujourd'hui`) ; `f` = date de première rencontre (rapport hebdo).

## Rythme de publication (demande du 7 novembre 2026 : économiser les crédits Netlify)
Formule gratuite Netlify : 300 crédits/mois, **chaque mise en ligne sur `main` coûte 15 crédits** ; les branches ne coûtent rien.
- Chaque nouvelle demande d'évolution est développée et testée sur la branche **`prochaine-version`** (push autorisé, pas de mise en ligne).
  L'artefact Claude est mis à jour à chaque demande : il sert d'aperçu.
- On fusionne `prochaine-version` dans `main` (= 1 seule mise en ligne) **toutes les 3 demandes d'évolution**.
  Compteur ci-dessous, à mettre à jour sur la branche à chaque demande, remis à 0 à la fusion.
- Exception : un bug qui empêche d'utiliser l'appli → proposer à l'utilisateur de publier tout de suite.
- Un commit sur `main` qui ne touche pas l'appli (documentation) porte `[skip ci]` dans son message pour ne pas déclencher de mise en ligne.
- Une seule version (`APP_VERSION`, cache `hola-lola-vN`) par mise en ligne, avec un texte `NEW_IN` qui résume les 3 demandes.

**Demandes en attente sur `prochaine-version` : 1 / 3** (version 23 en préparation ; la 22 est en ligne depuis le 8 novembre 2026)
1. Bouton « + » pour un temps d'écran personnalisé ; boutique (accessoires sur 5 emplacements, skins, univers à débloquer, 2 univers offerts par sexe), 2 nouveaux jeux, décors et bonus de jeux ; voix d'homme ; langue du système par défaut. Slogan : 5 propositions faites, en attente du choix.

**À venir (décidé le 8 novembre 2026)** : comptes pour retrouver sa progression, créés par le **parent** (e-mail + mot de passe du parent, un profil par enfant), à faire quand l'utilisateur aura son propre hébergement ; ils remplaceront le code de sauvegarde.

## Publier une nouvelle version
1. Modifier `index.html` (ajouter des niveaux dans un tableau `V8_…` puis `insAfter(...)`, comme V7).
2. Incrémenter `APP_VERSION` et ajouter le texte de nouveauté dans `NEW_IN` (bandeau affiché une fois).
3. Dans `sw.js`, changer le nom du cache (`hola-lola-vN`).
4. Vérifier la syntaxe du script et tester toutes les leçons (startUnit sur chaque niveau) dans Playwright.
5. Commit + push sur `prochaine-version` ; à la 3e demande, fusion dans `main` → Netlify déploie, le téléphone se met à jour à la prochaine ouverture.

Le même contenu est aussi publié comme artefact Claude : c'est `index.html` sans l'en-tête PWA
ni le script d'enregistrement du service worker. Les images `fx/*.webp` sont publiées avec l'artefact (deux publications : 255 fichiers maximum par envoi). Dans l'artefact, le micro est bloqué (mode « répéter à voix haute »).
