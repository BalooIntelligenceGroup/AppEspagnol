const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();
for(const [tg,lang] of [['es','fr'],['en','it'],['it','en']]){const ctx=await b.newContext({viewport:{width:400,height:860},locale:lang});
await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#warn{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st))});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));const log=(...a)=>console.log(tg,lang,...a);
await p.goto('http://localhost:8765/index.html');
const st={};['saludos','colores','numeros','mascotas','familia','frutas','comida','ropa','casa','escuela'].forEach(i=>st[i]=3);
await p.evaluate(([tg,l,st])=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'m',theme:'jungla',lang:l,target:tg,stars:st,ver:30,seen:30,mig12:1,mig13:1,mig22:1,mig23:1,mig29:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{1:1,2:1},days:{},coins:20,words:{}}));localStorage.setItem('hola-lola-subs',JSON.stringify([{lang:tg,offer:'famille',start:'2026-09-01',period:'month'}]))},[tg,lang,st]);
await p.reload();await p.waitForTimeout(500);
await p.click('[data-act="trad"]');await p.waitForTimeout(200);
log('atelier',await p.evaluate(()=>document.querySelector('#app').innerText.replace(/\n+/g,' / ').slice(0,330)));
for(const k of ['oral','ecrit']){
 await p.click(`[data-act="tradgo"][data-k="${k}"]`);await p.waitForTimeout(200);
 const info=await p.evaluate(()=>L.steps.map(s=>s.mode||(s.fr?'fr':'dict')).join(','));
 // jouer le 1er exercice correctement
 await p.evaluate(()=>{const s=L.steps[L.i];s.target.forEach(w=>{const k=s.tiles.findIndex((t,x)=>t===w&&!s.used.includes(x));document.querySelector(`.bank [data-k="${k}"]`).click()})});
 await p.waitForTimeout(400);
 log(k,info,await p.evaluate(()=>({ok:L.answered&&L.answered.ok,ask:document.querySelector('.ask').innerText.replace(/\n/g,' | '),target:L.steps[L.i].target.join(' ')})));
 if(tg==='es')await p.screenshot({path:S+`v31-${k}.png`});
 await p.evaluate(()=>{view='home';render()});await p.click('[data-act="trad"]');
}
// leçon Famille : les nouveaux modes sont là
log('famille',await p.evaluate(()=>{const i=UNITS.findIndex(u=>u.id==='f_cafe');startUnit(i);return L.steps.filter(s=>s.t==='build').map(s=>s.mode||(s.fr?'fr':'dict')).join(',')}));
log('lecon N2',await p.evaluate(()=>{const i=UNITS.findIndex(u=>u.id==='ropa');startUnit(i);return L.steps.filter(s=>s.t==='build').map(s=>s.mode||(s.fr?'fr':'dict')).join(',')}));
log('ERR',errs);await ctx.close()}
await b.close()})();
