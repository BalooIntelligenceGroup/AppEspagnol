# v30 (3e demande) : personnages animés qui réagissent aux réponses, choisis au hasard
import json
P='/home/claude/appespagnol/index.html'
s=open(P,encoding='utf8').read()
J=lambda x:json.dumps(x,ensure_ascii=False)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]);s=s.replace(a,b,1)
CAST=['🦊','🐸','🐰','🐻','🐙','🦁','🐱','🐢']
# phrases : [es, en, it, fr]
OK=[['¡Muy bien!','Well done!','Bravissimo!','Très bien !'],['¡Genial!','Great!','Fantastico!','Génial !'],['¡Perfecto!','Perfect!','Perfetto!','Parfait !'],['¡Eso es!','That\'s it!','Esatto!','C\'est ça !'],['¡Fantástico!','Brilliant!','Ottimo!','Fantastique !'],['¡Bravo!','Hooray!','Evviva!','Bravo !']]
KO=[['¡Casi!','Almost!','Quasi!','Presque !'],['¡Ánimo!','Keep going!','Forza!','Courage !'],['¡Tú puedes!','You can do it!','Ce la fai!','Tu peux y arriver !'],['¡Otra vez!','One more time!','Ancora una volta!','Encore une fois !']]
rep("const pick=a=>a[Math.random()*a.length|0];","""const pick=a=>a[Math.random()*a.length|0];
/* v30 : troupe de personnages qui réagissent à chaque réponse (choisis au hasard, le compagnon de l'univers en fait partie) */
const CAST="""+J(CAST)+""";
const CHEER={ok:"""+J(OK)+""",ko:"""+J(KO)+"""};
function castFor(a){if(!a.cast){a.cast=Math.random()<.25?G().e:pick(CAST);a.ph=pick(CHEER[a.ok?'ok':'ko'])}
  const ti={es:0,en:1,it:2}[TGT]??0,li={en:1,it:2,fr:3}[S.lang||'fr']??3,said=a.ph[ti],mean=li!==ti?a.ph[li]:'';
  return `<div class="cast-row"><span class="cast ${a.ok?'joy':'sad'}" aria-hidden="true">${a.cast}</span><div class="cbub"><b>${esc(said)}</b>${mean?`<small>${esc(mean)}</small>`:''}</div></div>`}""")
rep("""foot=`<div class="fb ${g?'good':'bad'}" role="status"><h3>${g?pick(['¡Muy bien!','¡Genial!','¡Bravo!','¡Perfecto!']):'¡Casi! Presque !'}</h3>""",
    """foot=`<div class="fb ${g?'good':'bad'}" role="status">${castFor(L.answered)}""")
css=""".cast-row{display:flex;align-items:center;gap:12px}
.cast{font-size:54px;line-height:1;display:inline-block;flex:none;transform-origin:50% 90%}
.cast img.fx{width:60px;height:60px}
.cast.joy{animation:chJoy .9s ease-out both}
.cast.sad{animation:chSad .8s ease-out both}
.cbub{position:relative;background:var(--card);border-radius:18px;padding:8px 14px;box-shadow:0 3px 0 var(--line);animation:chPop .35s .15s ease-out both}
.cbub::before{content:"";position:absolute;left:-8px;top:50%;margin-top:-8px;border:8px solid transparent;border-left:0;border-right-color:var(--card)}
.cbub b{display:block;font-size:22px;line-height:1.2}
.cbub small{display:block;font-size:13px;font-weight:700;color:var(--muted)}
@keyframes chJoy{0%{transform:translateY(30px) scale(.4);opacity:0}35%{transform:translateY(-14px) scale(1.12) rotate(-6deg);opacity:1}55%{transform:translateY(0) scale(.95) rotate(4deg)}75%{transform:translateY(-6px) rotate(-2deg)}100%{transform:none}}
@keyframes chSad{0%{transform:translateY(20px) scale(.5);opacity:0}30%{transform:none;opacity:1}45%{transform:rotate(-10deg)}60%{transform:rotate(8deg)}75%{transform:rotate(-5deg)}100%{transform:rotate(0)}}
@keyframes chPop{0%{transform:scale(.6);opacity:0}100%{transform:none;opacity:1}}
@media (prefers-reduced-motion:reduce){.cast,.cbub{animation:none!important}}
.fb{"""
rep(".fb{",css)
open(P,'w',encoding='utf8').write(s);print('ok')
