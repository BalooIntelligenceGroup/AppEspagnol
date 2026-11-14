const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const lang of ['fr','en']){const ctx=await b.newContext({viewport:{width:400,height:860},locale:lang});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
const cdp=await ctx.newCDPSession(p);await cdp.send('WebAuthn.enable');const {authenticatorId}=await cdp.send('WebAuthn.addVirtualAuthenticator',{options:{protocol:'ctap2',transport:'internal',hasResidentKey:true,hasUserVerification:true,isUserVerified:true,automaticPresenceSimulation:true}});
await p.goto('http://localhost:8765/index.html');
await p.evaluate(l=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:l,target:'es',stars:{},ver:30,seen:30,mig12:1,mig13:1,mig22:1,mig23:1,mig29:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{},days:{},coins:20,words:{}}))},lang);
await p.reload();await p.waitForTimeout(500);
await p.evaluate(()=>{setPin('1234');setQ(0,'paris');view='parent';render()});await p.waitForTimeout(300);
console.log(lang,'parent bloc:',await p.evaluate(()=>{const t=document.body.innerText;const i=t.indexOf('👆');return t.slice(i,i+120).replace(/\n/g,' / ')}));
await p.click('[data-act="bioon"]');await p.waitForTimeout(800);
console.log(lang,'activation:',await p.evaluate(()=>({saved:!!localStorage.getItem('hola-lola-bio'),msg:(document.querySelector('[role=status]')||{}).innerText})));
await p.evaluate(()=>{view='settings';render();openGate()});await p.waitForTimeout(300);
console.log(lang,'bouton gate:',await p.evaluate(()=>!!document.querySelector('[data-act="biogo"]')));
await p.click('[data-act="biogo"]');await p.waitForTimeout(800);
console.log(lang,'apres empreinte, vue =',await p.evaluate(()=>view));
// refus (UV non vérifiée)
await cdp.send('WebAuthn.setUserVerified',{authenticatorId,isUserVerified:false});
await p.evaluate(()=>{view='settings';render();openGate()});await p.click('[data-act="biogo"]');await p.waitForTimeout(800);
console.log(lang,'refus, vue =',await p.evaluate(()=>view+' / '+(document.querySelector('#gmsg')||{}).innerText));
console.log(lang,'ERR',errs);await ctx.close()}
await b.close()})();
