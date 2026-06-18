importScripts(
'https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js'
);

importScripts(
'https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js'
);

firebase.initializeApp({

apiKey:"AIzaSyDhd9b-GT3gIA_5t8_mdtptVhmFnjFxf8g",

authDomain:"site-visit-web.firebaseapp.com",

projectId:"site-visit-web",

messagingSenderId:"385253553737",

appId:"1:385253553737:web:9f08602c89614eaa9e3198"

});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload)=>{

self.registration.showNotification(
payload.notification.title,
{
body:payload.notification.body,
icon:'/icon.png'
});

});
