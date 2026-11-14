const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();
for(const lang of ['fr','en','it']){const ctx=await b.newContext({viewport:{width:400,height:860},locale:lang});
await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#warn{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st))});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));const log=(...a)=>console.log(lang,...a);
await p.goto('http://localhost:8765/index.html');
const t=new Date();const d=n=>{const x=new Date(t);x.setDate(x.getDate()+n);return x.toISOString().slice(0,10)};
await p.evaluate(([l,d0,dm])=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:l,target:'es',stars:{saludos:3,colores:2},ver:30,seen:30,mig12:1,mig13:1,mig22:1,mig23:1,mig29:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{},days:{},coins:20,
 words:{'hola':{b:4,d:d0,ok:5,ko:0,f:dm},'gracias':{b:3,d:d0,ok:3,ko:0,f:dm},'adiós':{b:1,d:d0,ok:1,ko:1,f:dm},'buenos días':{b:5,d:d0,ok:6,ko:0,f:dm}}}))},[lang,d(0),d(-10)]);
await p.reload();await p.waitForTimeout(500);
log('chip',await p.evaluate(()=>[...document.querySelectorAll('.chip')].map(c=>c.innerText).join(' | ')));
if(lang==='fr')await p.screenshot({path:S+'v30-home.png'});
await p.click('[data-act="dico"]');await p.waitForTimeout(300);
log('dico',await p.evaluate(()=>document.querySelector('#app').innerText.split('\n').filter(Boolean).slice(0,9).join(' / ')));
await p.evaluate(()=>document.querySelectorAll('details.lacc').forEach(d=>d.open=true));
log('badges',await p.evaluate(()=>[...document.querySelectorAll('.dw')].slice(0,6).map(b=>(b.querySelector('.wst')||{}).textContent||'-').join('')));
if(lang==='fr')await p.screenshot({path:S+'v30-dico.png',fullPage:false});
// fin de séance : simule une séance qui fait passer « Gracias » à retenu
await p.evaluate(()=>{startSeance();S.words['gracias'].b=4;finish()});await p.waitForTimeout(300);
log('seance',await p.evaluate(()=>[...document.querySelectorAll('.say')].map(x=>x.innerText).join(' || ')));
if(lang==='fr')await p.screenshot({path:S+'v30-seance.png'});
await p.evaluate(()=>{setPin('1234');setQ(0,'paris');view='parent';render()});await p.waitForTimeout(200);
await p.evaluate(()=>{document.querySelectorAll('details').forEach(d=>d.open=true)});
log('parent',await p.evaluate(()=>{const t=document.body.innerText;const i=t.indexOf('ℹ️');return t.slice(i,i+300).replace(/\n/g,' / ')}));
log('ERR',errs);await ctx.close()}
await b.close()})();
