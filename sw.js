/* Ahla bik – version 2. Page et liste des voix prises sur Internet quand c'est possible (mises à jour immédiates), sinon depuis le cache (hors ligne). Les voix se gardent en cache dès la première écoute. */
const C='ahla-v2';
const CORE=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','icon-maskable-512.png','audio/index.json'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE.map(u=>new Request(u,{cache:'reload'})))));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
const fresh=(r,key)=>fetch(r,{cache:'no-store'}).then(res=>{if(res.ok){const cp=res.clone();caches.open(C).then(c=>c.put(key||r,cp))}return res}).catch(()=>caches.match(key||r));
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;
  if(r.mode==='navigate'){e.respondWith(fresh(r,'index.html').then(x=>x||caches.match('./')));return}
  if(new URL(r.url).pathname.endsWith('/audio/index.json')){e.respondWith(fresh(r,'audio/index.json'));return}
  e.respondWith(caches.match(r).then(hit=>{const net=fetch(r).then(res=>{if(res&&(res.ok||res.type==='opaque')){const cp=res.clone();caches.open(C).then(c=>c.put(r,cp))}return res}).catch(()=>hit);return hit||net}));
});
