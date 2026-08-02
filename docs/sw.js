/* LAZARUS v8 — service worker : l'appli fonctionne même sans internet.
   Stratégie : réseau d'abord (toujours la dernière version quand on est
   connecté), cache en secours (hors-ligne = la dernière version connue). */
const CACHE = 'lazarus-v8';
const FICHIERS = ['./', './index.html', './manifest.json', './icone-192.png', './icone-512.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FICHIERS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((noms) =>
    Promise.all(noms.filter((n) => n !== CACHE).map((n) => caches.delete(n)))
  ).then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request).then((rep) => {
      const copie = rep.clone();
      caches.open(CACHE).then((c) => c.put(e.request, copie)).catch(() => {});
      return rep;
    }).catch(() => caches.match(e.request, { ignoreSearch: false })
      .then((r) => r || caches.match('./index.html')))
  );
});
