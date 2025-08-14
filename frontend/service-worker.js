self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open("bloodlink-cache").then((cache) => {
      return cache.addAll([
        "/",
        "/index.html",
        "/css/style.css",
        "/js/app.js",
        "/js/auth.js",
        "/js/socket.js"
      ]);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((resp) => {
      return resp || fetch(event.request);
    })
  );
});
