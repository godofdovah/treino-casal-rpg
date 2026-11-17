// Guarda uma cópia do app para abrir sem internet. Sempre tenta a internet primeiro.
const CACHE = 'duo-v2';
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let u; try { u = new URL(req.url); } catch (err) { return; }
  const nosso = u.origin === self.location.origin && !u.pathname.endsWith('versao.json');
  const firebase = u.hostname === 'www.gstatic.com' && u.pathname.startsWith('/firebasejs/');
  const fonte = u.hostname === 'fonts.googleapis.com' || u.hostname === 'fonts.gstatic.com';
  if (!nosso && !firebase && !fonte) return;
  e.respondWith(
    fetch(req, nosso ? { cache: 'no-cache' } : undefined).then(res => {
      if (res && (res.ok || res.type === 'opaque')) { const copia = res.clone(); caches.open(CACHE).then(c => c.put(req, copia)).catch(() => {}); }
      return res;
    }).catch(() => caches.match(req, { ignoreSearch: req.mode === 'navigate' }).then(r => r || Promise.reject(new Error('offline'))))
  );
});
