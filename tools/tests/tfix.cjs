const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:400,height:820},deviceScaleFactor:2,locale:'fr-FR'});
await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#warn{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st))});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));const log=(...a)=>console.log(...a);
await p.goto('http://localhost:8765/index.html');
await p.evaluate(()=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:'fr',stars:{},ver:25,mig12:1,mig13:1,mig22:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{},days:{},coins:20,words:{}}))});
await p.reload();await p.waitForTimeout(500);
await p.evaluate(()=>{setPin('1234');setQ(0,'paris');view='parent';render()});await p.fill('#promo',process.env.BETA_CODE||'');await p.click('[data-act="promo"]');await p.waitForTimeout(400);
// every step of every lesson + bonus: interactive elements present
log('audit',await p.evaluate(()=>{const bad=[];const chk=(id)=>{L.steps.forEach((s,k)=>{L.i=k;L.answered=null;render();const n=document.querySelectorAll('[data-act]:not([data-act="quit"]):not([data-act="hear"]):not([data-act="home"]):not([data-act="trq"])').length;if(s.t==='build'&&!document.querySelectorAll('.bank .tile').length)bad.push(id+':'+k+':build'+(s.fr?'-fr':''));if(n<1)bad.push(id+':'+k+':'+s.t)})};
 UNITS.forEach((u,i)=>{startUnit(i);chk(u.id)});MONTHLY.forEach(m=>{startUnit(-1,m.u);chk(m.u.id)});return {n:UNITS.length+MONTHLY.length,bad:bad.slice(0,10),nbad:bad.length}}));
// play a translate step to the end
await p.evaluate(()=>{const i=UNITS.findIndex(u=>u.id==='f_cafe');startUnit(i);L.i=L.steps.findIndex(s=>s.t==='build'&&s.fr);L.answered=null;render()});
await p.screenshot({path:S+'fix-before.png'});
await p.evaluate(()=>{const s=L.steps[L.i];s.target.forEach(w=>{const k=s.tiles.findIndex((t,x)=>t===w&&!s.used.includes(x));document.querySelector(`.bank [data-k="${k}"]`).click()})});
await p.waitForTimeout(300);
const chk=await p.$('[data-act="check"]');if(chk)await chk.click();await p.waitForTimeout(300);
log('answered',await p.evaluate(()=>({ok:L.answered&&L.answered.ok,cont:!!document.querySelector('[data-act="next"]')})));
await p.screenshot({path:S+'fix-after.png'});
log('ERR',errs);await b.close()})();
