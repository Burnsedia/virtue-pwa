const CACHE_NAME = 'virtue-pwa-cache-v2';
const urlsToCache = [
  '/',
  '/styles/global.css',
  '/favicon.svg',
  '/manifest.json',
  '/projects',
  '/crud',
  '/matrix',
  '/pomodoro',
  '/settings',
  '/signin',
  '/signup',
  '/forgot-password',
  // Add other critical assets like images, fonts, etc.
  // '/images/logo.png',
  // '/fonts/myfont.woff2',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
