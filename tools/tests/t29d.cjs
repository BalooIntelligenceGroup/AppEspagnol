const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();
for(const tg of ['en','it','es']){const ctx=await b.newContext({viewport:{width:400,height:820},locale:'fr-FR'});await ctx.clock.setFixedTime(new Date('2026-12-03T10:00:00'));
await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#warn{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st))});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));const log=(...a)=>console.log(tg,...a);
await p.goto('http://localhost:8765/index.html');
await p.evaluate(tg=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'m',theme:'jungla',lang:'fr',target:tg,stars:{},ver:29,seen:29,mig12:1,mig13:1,mig22:1,mig23:1,mig29:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{},days:{},coins:20,words:{}}))},tg);
await p.reload();await p.waitForTimeout(500);
await p.evaluate(()=>{setPin('1234');setQ(0,'paris');view='parent';render()});await p.fill('#promo',process.env.BETA_CODE||'');await p.click('[data-act="promo"]');await p.waitForTimeout(400);
log('ultimate',await p.evaluate(()=>{famSync();const t={};UNITS.forEach(u=>t[u.tier]=(t[u.tier]||0)+1);return {n:UNITS.length,tiers:t,spanishLeft:UNITS.filter(u=>u.tier>=6).flatMap(u=>u.words.map(w=>w[0])).filter(x=>/[ñ¿¡]/.test(x)).slice(0,5),songs:SONGS.filter(s=>stageUnits(s.tier).length).length}}));
log('audit',await p.evaluate(()=>{const bad=[];UNITS.forEach((u,i)=>{startUnit(i);L.steps.forEach((s,k)=>{L.i=k;L.answered=null;render();const n=document.querySelectorAll('[data-act]:not([data-act="quit"]):not([data-act="hear"]):not([data-act="home"]):not([data-act="trq"])').length;if(s.t==='build'&&!document.querySelectorAll('.bank .tile').length)bad.push(u.id+':'+k+':build');if(n<1)bad.push(u.id+':'+k+':'+s.t)})});return bad}));
// joue une phrase à trou d'une ancienne leçon
await p.evaluate(()=>{const i=UNITS.findIndex(u=>u.id==='emociones');startUnit(i);L.i=L.steps.findIndex(s=>s.t==='gap');L.answered=null;render()});
log('gap',await p.evaluate(()=>document.querySelector('.stage, main, #app').innerText.replace(/\n+/g,' | ').slice(0,200)));
await p.screenshot({path:S+`v29d-${tg}-gap.png`});
await p.evaluate(()=>{const i=UNITS.findIndex(u=>u.id==='nueva');startUnit(i);L.i=L.steps.findIndex(s=>s.t==='talk');L.answered=null;render()});
log('talk nueva',await p.evaluate(()=>document.querySelector('#app').innerText.replace(/\n+/g,' | ').slice(0,260)));
log('ERR',errs);await ctx.close()}
await b.close()})();
