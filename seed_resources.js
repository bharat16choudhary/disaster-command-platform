/**
 * seed_resources.js
 * Run this ONCE in your browser console (on the dashboard page, while logged in)
 * OR paste into a Firebase Cloud Function.
 *
 * It populates the "resources" Firestore collection with sample
 * ambulances, fire trucks, and police cars so the smart-allocation
 * logic has data to work with.
 *
 * Usage (browser console on dashboard.html):
 *   Copy the code below, open dashboard.html, open DevTools → Console, paste & run.
 */

import { initializeApp }  from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getFirestore, collection, addDoc } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const firebaseConfig = {
  apiKey:            "YOUR_API_KEY",
  authDomain:        "YOUR_AUTH_DOMAIN",
  projectId:         "YOUR_PROJECT_ID",
  storageBucket:     "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId:             "YOUR_APP_ID"
};

const app = initializeApp(firebaseConfig);
const db  = getFirestore(app);

const sampleResources = [
  { type: "fire truck",  latitude: 19.0820, longitude: 72.8820, available: true },
  { type: "ambulance",   latitude: 19.0700, longitude: 72.8700, available: true },
  { type: "police car",  latitude: 19.0760, longitude: 72.8600, available: true },
  { type: "ambulance",   latitude: 19.0900, longitude: 72.8900, available: true },
  { type: "fire truck",  latitude: 19.0600, longitude: 72.8500, available: true },
  { type: "police car",  latitude: 19.0550, longitude: 72.8750, available: true },
];

(async () => {
  for (const r of sampleResources) {
    const ref = await addDoc(collection(db, "resources"), r);
    console.log("Added resource:", ref.id, r.type);
  }
  console.log("✅ All resources seeded!");
})();
