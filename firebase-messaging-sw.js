// firebase-messaging-sw.js
// Must live at the ROOT of your GitHub Pages site (same folder as notify.html)
// so it can register with scope "/" and receive background push messages.

importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js');

// ⚠️ Replace with YOUR Firebase project's config
firebase.initializeApp({
  apiKey: "AIzaSyDhd9b-GT3gIA_5t8_mdtptVhmFnjFxf8g",
  authDomain: "site-visit-web.firebaseapp.com",
  projectId: "site-visit-web",
  storageBucket: "site-visit-web.firebasestorage.app",
  messagingSenderId: "385253553737",
  appId: "1:385253553737:web:9f08602c89614eaa9e3198"
});

const messaging = firebase.messaging();

// Shows a notification when a push arrives while the site is NOT in the foreground tab
messaging.onBackgroundMessage(function (payload) {
  console.log('[firebase-messaging-sw.js] Background message received:', payload);

  const title = (payload.notification && payload.notification.title) || 'Site Visit Reminder';
  const options = {
    body: (payload.notification && payload.notification.body) || "Don't forget to submit today's site visit form.",
    data: { url: 'https://karan2233-cmd.github.io/site-visit-notify/notify.html' }
  };

  self.registration.showNotification(title, options);
});

// Clicking the notification opens (or focuses) the notify page
self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  const targetUrl = (event.notification.data && event.notification.data.url) || '/';
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (clientList) {
      for (const client of clientList) {
        if (client.url === targetUrl && 'focus' in client) return client.focus();
      }
      if (clients.openWindow) return clients.openWindow(targetUrl);
    })
  );
});
