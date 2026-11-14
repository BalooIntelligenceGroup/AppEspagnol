const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();
for(const [tg,lang] of [['en','fr'],['it','fr'],['es','fr']]){const ctx=await b.newContext({viewport:{width:400,height:820},locale:lang});
await ctx.clock.setFixedTime(new Date('2026-12-03T10:00:00'));
await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#warn{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st))});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));const log=(...a)=>console.log(tg,...a);
await p.goto('http://localhost:8765/index.html');
const st={};['saludos','colores','numeros','mascotas','familia','frutas','comida','ropa','casa','escuela','presentarse','estas','gustos','preguntas','ayuda'].forEach(i=>st[i]=3);
await p.evaluate(([tg,l,st])=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:l,target:tg,stars:st,ver:29,seen:29,mig12:1,mig13:1,mig22:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{1:1,2:1,3:1},days:{},coins:20,words:{}}))},[tg,lang,st]);
// sans abonnement : aperçu verrouillé + bonus verrouillé
await p.reload();await p.waitForTimeout(500);
log('sans abo',await p.evaluate(()=>({fam:[...document.querySelectorAll('.famn b')].map(x=>x.textContent),bonusLocked:document.querySelectorAll('.bonusn.locked').length,head:[...document.querySelectorAll('.tier.fam b')].map(x=>x.textContent)})));
// abonnement Famille dans cette langue depuis 40 jours
await p.evaluate(tg=>{localStorage.setItem('hola-lola-subs',JSON.stringify([{lang:tg,offer:'famille',start:'2026-10-20',period:'month'}]))},tg);
await p.reload();await p.waitForTimeout(500);
log('abo',await p.evaluate(()=>{famSync();return {units:UNITS.slice(15).map(u=>u.es),bonusOpen:document.querySelectorAll('.bonusn:not(.locked)').length,songs:SONGS.filter(s=>stageUnits(s.tier).length).map(s=>s.t)}}));
log('audit',await p.evaluate(()=>{const bad=[];UNITS.forEach((u,i)=>{if(u.tier<4)return;startUnit(i);L.steps.forEach((s,k)=>{L.i=k;L.answered=null;render();if(s.t==='build'&&!document.querySelectorAll('.bank .tile').length)bad.push(u.id+':'+k);if(s.t==='gap'&&document.querySelectorAll('[data-act]').length<3)bad.push(u.id+':gap'+k)})});return bad}));
// joue une phrase à construire de f_medico
await p.evaluate(()=>{const i=UNITS.findIndex(u=>u.id==='f_medico');startUnit(i);L.i=L.steps.findIndex(s=>s.t==='build');L.answered=null;render()});
await p.evaluate(()=>{const s=L.steps[L.i];s.target.forEach(w=>{const k=s.tiles.findIndex((t,x)=>t===w&&!s.used.includes(x));document.querySelector(`.bank [data-k="${k}"]`).click()})});
await p.waitForTimeout(200);const c=await p.$('[data-act="check"]');if(c)await c.click();await p.waitForTimeout(300);
log('build',await p.evaluate(()=>({ok:L.answered&&L.answered.ok,target:L.steps[L.i].target.join(' '),voice:TLC[TGT]})));
await p.screenshot({path:S+`v29b-${tg}.png`});
await p.evaluate(()=>{const i=UNITS.findIndex(u=>u.id==='f_perdido');startUnit(i);L.i=L.steps.findIndex(s=>s.t==='gap');L.answered=null;render()});
await p.screenshot({path:S+`v29b-${tg}-gap.png`});
log('ERR',errs);await ctx.close()}
await b.close()})();
