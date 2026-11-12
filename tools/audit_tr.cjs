/* Contrôle des traductions (règle v28) : à lancer à CHAQUE demande, avant tout commit.
   Usage : dans le dossier du dépôt, `python3 -m http.server 8765` puis `node tools/audit_tr.cjs`.
   Vérifie, pour chaque langue apprise (es, en, it), que tout texte de contenu a son sens anglais/italien dans TRX
   (le français vient de words/talk/FR_EXTRA) : leçons gratuites, Famille, anciennes leçons (Ultimate), bonus, histoires,
   titres des niveaux bonus, récitations (SONG_TR : [français, anglais, italien]). Code de sortie 1 s'il manque quelque chose. */
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(600);
const r=await p.evaluate(()=>{const out={};
 const groups={free:()=>ACTIVE.map(id=>ALL_UNITS.find(u=>u.id===id)),famille:()=>FAM_UNITS,extra:()=>EXTRA_UNITS,bonus:()=>Object.values(BONUS_LV[TGT]||{}).flatMap(l=>l.ids.map(bonUnit)).filter(Boolean)};
 for(const t of ['es','en','it']){setTarget(t);
  for(const [g,f] of Object.entries(groups)){if(t!=='es'&&(g==='famille'||g==='extra'))continue;   /* Famille et Ultimate : espagnol seulement pour l'instant */
   const miss=new Set();let n=0;const chk=s=>{if(!s)return;n++;const k=TA[s]||s;if(!TRX[k])miss.add(s)};
   f().forEach(u=>{chk(u.es);u.words.forEach(w=>chk(w[0]));(u.talk||[]).forEach(d=>{chk(d.l);d.o.forEach(o=>chk(o[0]))});(u.gaps||[]).forEach(g=>chk(g[0].replace('_',g[1])));
     const st=STORY[u.id];if(st&&g==='free')st.p.forEach(pp=>chk(pp[1]))});
   if(g==='bonus')Object.values(BONUS_LV[t]||{}).forEach(l=>chk(l.t));
   out[t+'/'+g]={n,miss:miss.size,ex:[...miss].slice(0,6)}}
  /* récitations affichées pour cette langue (en/it : Niveaux 1 à 3) : sens fr/en/it dans SONG_TR */
  const sm=new Set();let sn=0;SONGS.filter(x=>t==='es'||x.tier<=3).forEach(x=>[x.t,...x.l].forEach(l=>{sn++;const v=SONG_TR[l];if(!v||v.length!==3||v.some(y=>!y))sm.add(l)}));
  out[t+'/recit']={n:sn,miss:sm.size,ex:[...sm].slice(0,6)}}
 setTarget('es');
 return out});
let bad=0;for(const [k,v] of Object.entries(r)){if(v&&v.miss!==undefined){bad+=v.miss;console.log((v.miss?'❌ ':'✅ ')+k.padEnd(12)+' '+v.n+' textes, '+v.miss+' manquants'+(v.miss?' : '+JSON.stringify(v.ex):''))}}
if(errs.length){console.log('Erreurs JS :',errs);bad++}
await b.close();process.exit(bad?1:0)})();
