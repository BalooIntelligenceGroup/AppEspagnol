"""Ajoute la possibilité de passer la répétition vocale + nouvelle version. Usage : python3 patch_skip.py <branche>"""
import re, sys
branch = sys.argv[1]
cfg = {
    'main':     dict(ver_from=9,  ver_to=10, cache='hola-lola'),
    'italiano': dict(ver_from=1,  ver_to=2,  cache='parliamo'),
    'tounsi':   dict(ver_from=1,  ver_to=2,  cache='ahla'),
}[branch]
p = open('index.html').read()

def rep(old, new, count=1):
    global p
    n = p.count(old)
    if n != count:
        sys.exit(f'{branch}: expected {count}, found {n}: {old[:90]}')
    p = p.replace(old, new)

# 1. Pied de page des exercices de répétition : toujours un bouton pour continuer
learn_re = re.compile(r"if\(s\.t==='learn'\)foot=(?:\(micOK&&!L\.learnDone\)\?`[^`]*`:)?`<button class=\"btn\" data-act=\"next\">Suivant</button>`;")
assert len(learn_re.findall(p)) == 1, branch + ' learn footer'
if branch != 'tounsi':  # en tunisien, l'enregistrement sur « Nouveau mot » est déjà facultatif
  p = learn_re.sub("if(s.t==='learn')foot=(micOK&&!L.learnDone)?`<button class=\"btn ghost\" data-act=\"next\">Passer la répétition →</button>`:`<button class=\"btn\" data-act=\"next\">Suivant</button>`;", p)
rep("else if(s.t==='speak'&&!micOK&&!L.answered)foot=`<button class=\"btn\" data-act=\"next\">Continuer</button>`;",
    "else if(s.t==='speak'&&!L.answered)foot=micOK?`<button class=\"btn ghost\" data-act=\"next\">Passer cet exercice →</button>`:`<button class=\"btn\" data-act=\"next\">Continuer</button>`;")

# 2. Espagnol / italien : si l'élève passe pendant que le micro écoute, le résultat qui arrive ensuite est ignoré
if branch in ('main', 'italiano'):
    rep("  let alts;\n  try{alts=await listen()}\n  catch(err){\n    btn.classList.remove('on');\n",
        "  const LL=L,at=L.i;let alts;\n  try{alts=await listen()}\n  catch(err){\n    btn.classList.remove('on');if(L!==LL||L.i!==at||view!=='lesson')return;\n")
    rep("  btn.classList.remove('on');\n  if(!alts.length)",
        "  btn.classList.remove('on');if(L!==LL||L.i!==at||view!=='lesson')return;\n  if(!alts.length)")

# 3. Nouvelle version + bandeau de nouveauté
txt = 'Tu peux maintenant passer un exercice de répétition au micro et continuer la leçon.'
if branch == 'main':
    rep("const APP_VERSION=9,NEW_IN={", "const APP_VERSION=10,NEW_IN={")
    rep("  9:'5 nouveaux niveaux : la musique, sous la mer, aider à la maison, partir en vacances et se faire une amie.'};",
        "  9:'5 nouveaux niveaux : la musique, sous la mer, aider à la maison, partir en vacances et se faire une amie.',\n  10:'" + txt + "'};")
else:
    rep("const APP_VERSION=1,NEW_IN={};", "const APP_VERSION=2,NEW_IN={2:'" + txt + "'};")
open('index.html', 'w').write(p)

sw = open('sw.js').read()
sw2 = re.sub(r"const C='%s-v\d+';" % cfg['cache'], "const C='%s-v%d';" % (cfg['cache'], cfg['ver_to']), sw)
sw2 = re.sub(r"version \d+", "version %d" % cfg['ver_to'], sw2, count=1)
assert sw2 != sw, branch + ' sw'
open('sw.js', 'w').write(sw2)
print(branch, 'patched → version', cfg['ver_to'])
