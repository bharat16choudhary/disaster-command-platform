# 🚨 AI-Powered Unified Disaster Command Platform — Setup Guide

## 📁 Project Structure

```
disaster-command-platform/
├── index.html          ← Login page
├── register.html       ← Register page
├── report.html         ← Incident reporting page
├── dashboard.html      ← Main dashboard (map + live list)
├── style.css           ← All styles (light/dark theme)
├── server.py           ← Python AI backend (no pip needed)
├── seed_resources.js   ← One-time Firestore resource seeder
└── SETUP.md            ← This file
```

---

## 🔥 Step 1 — Create a Firebase Project

1. Go to **https://console.firebase.google.com**
2. Click **"Add project"** → name it `disaster-command`
3. Disable Google Analytics (optional) → **Create Project**

### Enable Authentication
1. Left menu → **Authentication** → **Get started**
2. **Sign-in method** → Enable **Email/Password** → Save

### Enable Firestore Database
1. Left menu → **Firestore Database** → **Create database**
2. Choose **"Start in test mode"** (for development)
3. Select a region closest to you → **Enable**

### Get Firebase Config
1. Project Settings (gear icon) → **Your apps** → Click `</>` (Web)
2. Register app name: `disaster-web`
3. Copy the `firebaseConfig` object — it looks like:

```js
const firebaseConfig = {
  apiKey:            "AIza...",
  authDomain:        "disaster-command.firebaseapp.com",
  projectId:         "disaster-command",
  storageBucket:     "disaster-command.appspot.com",
  messagingSenderId: "123456789",
  appId:             "1:123:web:abc"
};
```

Paste this into all 4 HTML files (replacing `YOUR_API_KEY` etc.).

---

## 🗺️ Step 2 — Get a Google Maps API Key

1. Go to **https://console.cloud.google.com**
2. Left menu → **APIs & Services** → **Library**
3. Enable **"Maps JavaScript API"**
4. **Credentials** → **Create Credentials** → **API Key**
5. In `dashboard.html`, replace `YOUR_MAPS_API_KEY` in the script tag

---

## 🌱 Step 3 — Seed Firestore Resources (One-time)

1. Start the frontend server (Step 5 below)
2. Open `dashboard.html`, log in
3. Open **DevTools → Console**
4. Paste all code from `seed_resources.js` → Enter
5. You'll see: `✅ All resources seeded!`

---

## 🐍 Step 4 — Run the Python Backend

```powershell
cd C:\Users\Admin\IDEALAB\disaster-command-platform
python server.py
```

Test: `curl http://localhost:8000/health`

---

## 🌐 Step 5 — Serve the Frontend

```powershell
cd C:\Users\Admin\IDEALAB\disaster-command-platform
python -m http.server 3000
```
Open **http://localhost:3000**

---

## 🤖 AI Priority Rules

| Incident Type          | Priority   |
|------------------------|------------|
| fire, accident, injury | **HIGH**   |
| flood, damage          | **MEDIUM** |
| other                  | **LOW**    |

---

## ❗ Troubleshooting

| Problem | Fix |
|---|---|
| Map not showing | Check Maps API key; enable Maps JS API |
| Firebase errors | Verify config pasted in all 4 HTML files |
| Backend offline | Run `python server.py` |
| Resources empty | Run `seed_resources.js` seeder |

---

## 📋 Quick Checklist

- [ ] Firebase project created + Email/Password auth enabled
- [ ] Firestore created (test mode)
- [ ] `firebaseConfig` pasted in all 4 HTML files
- [ ] Google Maps API key in `dashboard.html`
- [ ] `python server.py` running on port 8000
- [ ] Frontend on `python -m http.server 3000`
- [ ] Resources seeded via `seed_resources.js`
- [ ] Test incident submitted → map marker appears
