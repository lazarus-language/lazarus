/* L'ancien service worker se retire : le site a déménagé sur larkhre.github.io. */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((noms) => Promise.all(noms.map((n) => caches.delete(n))))
    .then(() => self.registration.unregister()));
});
