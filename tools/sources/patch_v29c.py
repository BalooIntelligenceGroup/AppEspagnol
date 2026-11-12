P='/home/claude/appespagnol/index.html'
s=open(P,encoding='utf8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)>=1 and (n==0 or s.count(a)==n),(s.count(a),a[:90]);s=s.replace(a,b,1)
# 1. offre gratuite = Niveaux 1 et 2 (10 leçons) ; le Niveau 3 passe dans l'offre Famille.
#    Règle absolue : un enfant qui avait déjà ouvert le Niveau 3 (évaluation du Niveau 2 réussie, ou une leçon du Niveau 3 commencée) le garde (S.g3[langue]).
rep("""  for(let k=UNITS.length-1;k>=0;k--)if(UNITS[k].tier>=4)UNITS.splice(k,1);
  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famUltimate()?FAM_UNITS.length:famOpen(famStart())));   /* même offre Famille dans les 3 langues (v29) */""",
"""  FREE3=FREE3||UNITS.filter(u=>u.tier===3);
  for(let k=UNITS.length-1;k>=0;k--)if(UNITS[k].tier>=3)UNITS.splice(k,1);
  if(free3())UNITS.push(...FREE3);   /* Niveau 3 déjà ouvert avant la v29 : il reste gratuit pour cet enfant */
  const fl=famList();if(famActive())UNITS.push(...fl.slice(0,famUltimate()?fl.length:famOpen(famStart())));   /* même offre Famille dans les 3 langues (v29) */""")
rep("function famSync(){","""/* v29 : offre gratuite = Niveaux 1 et 2 (10 leçons). Le Niveau 3 (FREE3) ouvre l'offre Famille, sauf pour un enfant qui l'avait déjà ouvert (S.g3). */
let FREE3=null;
const free3=()=>!!(S.g3&&S.g3[TGT]);
const famList=()=>free3()?FAM_UNITS:[...(FREE3||[]),...FAM_UNITS];
function famSync(){""")
rep("const on=famActive(),us=on?FAM_UNITS.filter(u=>!UNITS.includes(u)):FAM_PREVIEW.map(id=>ALL_UNITS.find(u=>u.id===id)).filter(Boolean);",
    "const on=famActive(),us=on?famList().filter(u=>!UNITS.includes(u)):famList().slice(0,5);")
rep("  if(!S.mig22){","""  if(!S.mig29){S.g3=S.g3||{};if(S.name){const n3=['presentarse','estas','gustos','preguntas','ayuda'],had=o=>!!o&&(!!(o.evals&&o.evals[2])||n3.some(i=>(o.stars||{})[i]||(o.opened||[]).includes(i)));
    if(had(S))S.g3[S.target||'es']=1;Object.entries(S.L||{}).forEach(([l,o])=>{if(had(o))S.g3[l]=1})}S.mig29=1;if(S.name)save()}
  if(!S.mig22){""")
# textes de l'offre
rep("'Gratuit (15 leçons)'","'Gratuit (10 leçons)'")
rep("Les 15 premières leçons (Niveaux 1 à 3) sont gratuites, pour toujours, dans chaque langue.","Les 10 premières leçons (Niveaux 1 et 2) sont gratuites, pour toujours, dans chaque langue.")
rep('"Les {0} premières leçons (Niveaux {1} à {2}) sont gratuites, pour toujours, dans chaque langue.":','"Les {0} premières leçons (Niveaux {1} et {2}) sont gratuites, pour toujours, dans chaque langue.":["The first {0} lessons (Levels {1} and {2}) are free, forever, in every language.", "Le prime {0} lezioni (Livelli {1} e {2}) sono gratuite, per sempre, in ogni lingua."],"Les {0} premières leçons (Niveaux {1} à {2}) sont gratuites, pour toujours, dans chaque langue.":')
rep("profite de tes 15 leçons gratuites !","profite de tes 10 leçons gratuites !")
old="🎁 Chaque mois, une leçon Bonus sur la culture d'Espagne et d'Amérique latine, ouverte aux abonnés, quelle que soit la progression de l'enfant."
new="🎁 Chaque mois, un Niveau Bonus de 5 leçons sur une grande fête du pays de la langue apprise, ouvert aux abonnés, quelle que soit la progression de l'enfant."
rep(old+"</p>",new+"</p>")
rep('"'+old+'":','"'+new+'":["🎁 Every month, a 5-lesson Bonus Level about a big festival in a country of the language being learnt, open to subscribers whatever the child\'s progress.", "🎁 Ogni mese, un Livello Bonus di 5 lezioni su una grande festa del paese della lingua studiata, aperto agli abbonati, qualunque sia il percorso del bambino."],"'+old+'":',n=0)
rep("L'appli et les traductions des mots et des phrases s'affichent dans cette langue. L'espagnol reste en espagnol.</p>","L'appli et les traductions des mots et des phrases s'affichent dans cette langue. La langue apprise reste dans sa langue.</p>")
rep('"L\'appli et les traductions des mots et des phrases s\'affichent dans cette langue. L\'espagnol reste en espagnol.":','"L\'appli et les traductions des mots et des phrases s\'affichent dans cette langue. La langue apprise reste dans sa langue.":["The app and the translations of words and sentences are shown in this language. The language being learnt stays as it is.","L\'app e le traduzioni di parole e frasi sono in questa lingua. La lingua studiata resta com\'è."],"L\'appli et les traductions des mots et des phrases s\'affichent dans cette langue. L\'espagnol reste en espagnol.":')
# 2. premier écran : la question dans la langue du téléphone
rep('<h1 style="font-size:30px">Quelle langue veux-tu apprendre ?</h1>',
    '<h1 style="font-size:30px">${{fr:\'Quelle langue veux-tu apprendre ?\',en:\'Which language do you want to learn?\',it:\'Quale lingua vuoi imparare?\'}[S.lang||sysLang()]||\'Quelle langue veux-tu apprendre ?\'}</h1>')
rep('<p class="note">Which language? · ¿Qué idioma? · Quale lingua?</p>','<p class="note">Quelle langue ? · Which language? · Quale lingua?</p>')
open(P,'w',encoding='utf8').write(s);print('ok')
