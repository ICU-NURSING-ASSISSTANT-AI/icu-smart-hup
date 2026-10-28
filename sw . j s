/* ICU Smart Hub offline support — version 3 */
const SHELL='icu-shell-v3',DOCS='icu-docs-v3',VIDEOS='icu-videos-v3';
const SHELL_FILES=['./','./index.html','./manifest.json','./icon-192.png','./icon-512.png'];
self.addEventListener('install',event=>{event.waitUntil((async()=>{const c=await caches.open(SHELL);await Promise.allSettled(SHELL_FILES.map(async path=>{const r=await fetch(path,{cache:'reload'});if(r.ok)await c.put(path,r);}));await self.skipWaiting();})());});
self.addEventListener('activate',event=>{event.waitUntil((async()=>{const keys=await caches.keys();await Promise.all(keys.filter(k=>k.startsWith('icu-shell-')&&k!==SHELL).map(k=>caches.delete(k)));await self.clients.claim();})());});
self.addEventListener('fetch',event=>{const req=event.request;if(req.method!=='GET')return;const url=new URL(req.url);if(url.origin!==self.location.origin)return;
if(req.mode==='navigate'){event.respondWith((async()=>{try{const r=await fetch(req);if(r.ok){const c=await caches.open(SHELL);await c.put('./index.html',r.clone());}return r;}catch{return await caches.match('./index.html')||await caches.match('./')||Response.error();}})());return;}
if(/\.(mp4|webm|mov|m4v|ogg)$/i.test(url.pathname)){event.respondWith((async()=>{const cached=await caches.match(req.url);if(cached){const range=req.headers.get('range');if(range){const bytes=await cached.arrayBuffer();const match=/bytes=(\d+)-(\d*)/.exec(range);if(match){const start=Number(match[1]),end=match[2]?Math.min(Number(match[2]),bytes.byteLength-1):bytes.byteLength-1;if(start<bytes.byteLength&&end>=start)return new Response(bytes.slice(start,end+1),{status:206,headers:{'Content-Type':cached.headers.get('Content-Type')||'video/mp4','Content-Range':`bytes ${start}-${end}/${bytes.byteLength}`,'Accept-Ranges':'bytes','Content-Length':String(end-start+1)}});}}return cached;}return fetch(req);})());return;}
if(url.pathname.endsWith('.pdf')||url.pathname.endsWith('/policy_index.json')){event.respondWith((async()=>{try{const r=await fetch(req);if(r.ok){const c=await caches.open(DOCS);await c.put(req,r.clone());}return r;}catch{return await caches.match(req)||Response.error();}})());return;}
if(['.html','.css','.js','.png','.json'].some(ext=>url.pathname.endsWith(ext))){event.respondWith((async()=>{try{const r=await fetch(req);if(r.ok&& !url.pathname.endsWith('videos.json')){const c=await caches.open(SHELL);await c.put(req,r.clone());}return r;}catch{return await caches.match(req)||Response.error();}})());}
});

// Reviewer web push notifications. Existing offline caching remains unchanged.
self.addEventListener('push', event => {
  let payload = {};
  try { payload = event.data ? event.data.json() : {}; }
  catch { payload = {body: event.data ? event.data.text() : ''}; }
  const title = typeof payload.title === 'string' ? payload.title : 'ICU Smart Hub';
  const body = typeof payload.body === 'string' ? payload.body : 'New Nursing Question awaiting review.';
  const target = new URL('./#reviewerPanel', self.registration.scope).href;
  event.waitUntil(self.registration.showNotification(title, {
    body, icon: './icon-192.png', badge: './icon-192.png',
    tag: 'icu-nursing-question', renotify: true,
    data: {url: target}
  }));
});
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil((async () => {
    const target = new URL('./#reviewerPanel', self.registration.scope).href;
    const windows = await clients.matchAll({type: 'window', includeUncontrolled: true});
    for (const client of windows) {
      if (new URL(client.url).origin === self.location.origin) {
        await client.navigate(target);
        return client.focus();
      }
    }
    return clients.openWindow(target);
  })());
});
