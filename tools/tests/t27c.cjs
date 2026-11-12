const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:400,height:820},deviceScaleFactor:2,locale:'it-IT'});
await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#warn{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st))});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));const log=(...a)=>console.log(...a);
await p.goto('http://localhost:8765/index.html');
await p.evaluate(()=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:'fr',stars:{saludos:3,colores:2},ver:26,mig12:1,mig13:1,mig22:1,mig23:1,tuto:1,tsetup:1,limit:0,coins:50,days:{},opened:[],evals:{1:{pct:90}},words:{hola:{b:2,d:'2026-01-01',ok:1,ko:0}}}));setPin('1234');setQ(0,'paris')});
await p.reload();await p.waitForTimeout(500);
// 1. new profile on Italian phone learning English: no lang step, UI = it
await p.evaluate(()=>{view='who';render()});await p.click('[data-act="addp"]');await p.click('[data-act="settarget"][data-t="en"]');
log('after target',await p.evaluate(()=>({step:wStep,lang:S.lang,hasName:!!document.querySelector('#nm')})));
await p.evaluate(()=>{view='who';render()});await p.click('[data-act="addp"]');await p.click('[data-act="settarget"][data-t="it"]');
log('it on it phone',await p.evaluate(()=>({lang:S.lang})));
// 2. Lola adds English
await p.evaluate(()=>{loadProfile('p1');view='home';render()});await p.click('[data-act="langs"]');await p.screenshot({path:S+'v27c-langs.png'});
await p.click('[data-act="addlang"][data-t="en"]');log('gate',await p.evaluate(()=>({view,title:document.querySelector('.head h2')?.textContent})));
await p.evaluate(()=>{gateMode='pin';render();$('#pg').value='1234'});await p.click('[data-act="pgok"]');await p.waitForTimeout(200);
log('switched',await p.evaluate(()=>({view,TGT,target:S.target,stars:S.stars,words:Object.keys(S.words),coins:S.coins,L:Object.keys(S.L),Les:S.L.es&&Object.keys(S.L.es.stars),u0:UNITS[0].es})));
// play/finish lesson in English
await p.evaluate(()=>{startUnit(0);L.mistakes=0;finish()});log('en stars',await p.evaluate(()=>S.stars));
// switch back to es
await p.evaluate(()=>{view='langs';render()});await p.click('[data-act="golang"][data-t="es"]');
log('back es',await p.evaluate(()=>({TGT,stars:S.stars,words:Object.keys(S.words),evals:S.evals,Len:S.L.en&&S.L.en.stars,u0:UNITS[0].es})));
// persistence after reload
await p.reload();await p.waitForTimeout(500);log('reload',await p.evaluate(()=>({TGT,stars:S.stars,langs:langsOf(S)})));
// who flags, parent subscription area
await p.evaluate(()=>{view='who';render()});log('who',await p.evaluate(()=>[...document.querySelectorAll('.pcard b')].map(x=>x.textContent)));
await p.evaluate(()=>{localStorage.setItem('hola-lola-subs',JSON.stringify([{lang:'en',offer:'solo',pid:'p1',start:'2026-11-01',period:'month'}]));loadProfile('p1');view='parent';gatePass&&0;render()});
await p.evaluate(()=>{openGate(null);gateMode='pin';render();$('#pg').value='1234'});await p.click('[data-act="pgok"]');await p.waitForTimeout(200);
log('parent',await p.evaluate(()=>[...document.querySelectorAll('.limit')].map(x=>x.innerText).filter(t=>/Langues|languages|Lingue/.test(t))));
await p.evaluate(()=>document.querySelector('.famset').scrollIntoView());await p.screenshot({path:S+'v27c-parent.png'});
// subscription entitlement: solo en for p1 → famActive in en, not es
log('ent',await p.evaluate(()=>{const r={};switchTarget('en');r.en=famActive();switchTarget('es');r.es=famActive();return r}));
log('ERR',errs);await b.close()})();
