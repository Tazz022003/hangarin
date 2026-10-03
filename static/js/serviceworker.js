const CACHE_NAME = "hangarin-cache-v1";

const STATIC_ASSETS = [
    "/static/tasks/style.css",
    "/static/img/icon-192.png",
    "/static/img/icon-512.png",
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS);
        })
    );

    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => {
                        return (
                            name.startsWith("hangarin-cache-") &&
                            name !== CACHE_NAME
                        );
                    })
                    .map((name) => caches.delete(name))
            );
        })
    );

    self.clients.claim();
});

self.addEventListener("fetch", (event) => {
    const request = event.request;

    if (request.method !== "GET") {
        return;
    }

    const url = new URL(request.url);

    if (url.origin !== self.location.origin) {
        return;
    }

    // Dynamic pages: try the network first.
    // Do not cache authenticated pages containing user data.
    if (request.mode === "navigate") {
        event.respondWith(
            fetch(request).catch(() => {
                return new Response(
                    `<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport"
                              content="width=device-width, initial-scale=1">
                        <title>Hangarin Offline</title>
                    </head>
                    <body style="font-family: sans-serif; padding: 2rem;">
                        <h1>You're offline</h1>
                        <p>
                            Hindi ma-load ang Hangarin ngayon.
                            Pakikonekta muli sa internet at subukan ulit.
                        </p>
                    </body>
                    </html>`,
                    {
                        headers: {
                            "Content-Type": "text/html; charset=utf-8",
                        },
                    }
                );
            })
        );

        return;
    }

    // Static assets: use cache when available.
    if (url.pathname.startsWith("/static/")) {
        event.respondWith(
            caches.match(request).then((cachedResponse) => {
                if (cachedResponse) {
                    return cachedResponse;
                }

                return fetch(request).then((response) => {
                    if (response.ok) {
                        const responseToCache = response.clone();

                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(request, responseToCache);
                        });
                    }

                    return response;
                });
            })
        );
    }
});