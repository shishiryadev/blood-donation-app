# 🩸 BloodLink — Real-time Blood Donation Platform

BloodLink is a **web + mobile-ready** blood donation platform that connects donors with recipients in **real time**, organizes **community blood drives**, and sends **emergency alerts**.

This project includes:
- **Backend**: Flask + PostgreSQL + JWT Auth + Socket.IO  
- **Frontend**: HTML, CSS, JavaScript (vanilla, no framework)  
- **Database**: PostgreSQL for persistent user, donation, and drive data  
- **Real-time**: Emergency alerts & match notifications with Socket.IO  

---

## 📂 Project Structure
blood-donation-app/          
├── backend/    
│ ├── app.py  
│ ├── models.py  
│ ├── routes/  
│ │ ├── init.py  
│ │ ├── auth.py  
│ │ ├── donors.py  
│ │ ├── recipients.py  
│ │ └── drives.py  
│ ├── database.py  
│ ├── config.py  
│ └── requirements.txt  
├── frontend/  
│ ├── index.html  
│ ├── css/  
│ │ └── style.css  
│ ├── js/  
│ │ ├── app.js  
│ │ ├── auth.js  
│ │ └── socket.js  
│ ├── pages/  
│ │ ├── dashboard.html  
│ │ ├── profile.html  
│ │ ├── donors.html  
│ │ ├── recipients.html  
│ │ └── drives.html  
│ ├── images/  
│ ├── manifest.json  
│ └── service-worker.js  
└── README.md


## ⚙️ Backend Setup

### 1️⃣ Install PostgreSQL
Make sure PostgreSQL is installed and running.  
Create a database:
```bash
createdb blood_donation_db
```

### 2️⃣ Clone & Install Requirements

```bash

git clone https://github.com/shishiryadav123/blood-donation-app.git
cd blood-donation-app/backend
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt

```

### 3️⃣ Configure Environment Variables (optional)
You can edit config.py or set:

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/blood_donation_db"
export SECRET_KEY="your_secret"
export JWT_SECRET_KEY="your_jwt_secret"
```

### 4️⃣ Run the Backend
```bash
python app.py
```

This starts the backend at:
```arduino
http://localhost:5000
```

## 💻 Frontend Setup

### 1️⃣ Open `frontend` folder

```bash
cd ../frontend
```

### 2️⃣ Start a local static server
Option 1: Python server

```bash
python -m http.server 8000
```

Option 2: VS Code Live Server
(Install Live Server extension → Right-click `index.html` → "Open with Live Server")

Frontend runs at:

```arduino
http://localhost:8000
```
🔌 Connect Frontend to Backend
In your browser console (on the frontend site):

```javascript
localStorage.setItem("api_base", "http://localhost:5000");
localStorage.setItem("socket_base", "http://localhost:5000");
```
Then refresh the page.

📡 Features
✅ User Registration & Login (Donor or Recipient)
✅ Donor Search by Blood Type & Location
✅ Create Blood Requests & Close Them
✅ Accept Requests as Donor
✅ Create & Register for Drives
✅ Real-time Emergency Alerts (Socket.IO)
✅ PWA Ready — Installable on mobile

🚀 Running Locally (Quick Start)
```bash
# Terminal 1 — Backend
cd backend
source venv/bin/activate
python app.py

# Terminal 2 — Frontend
cd frontend
python -m http.server 8000
```
Open:

Backend API → `http://localhost:5000/api/health`

Frontend → `http://localhost:8000`

## 📱 Screenshots

 ![1](blood-donation-app-1.png) ![2](blood-donation-app-2.png) ![3](blood-donation-app-3.png) ![4](blood-donation-app-4.png) ![5](blood-donation-app-5.png) ![6](blood-donation-app-6.png)

🛠 API Endpoints
### Auth
- `POST /api/auth/register`

- `POST /api/auth/login`

- `GET /api/auth/me`

- `PUT /api/auth/me`

### Donors
- `GET /api/donors/`

- `PUT /api/donors/profile`

- `POST /api/donors/accept_request`

### Recipients
- `POST /api/recipients/request`

- `GET /api/recipients/nearby_donors`

- `GET /api/recipients/requests`

- `POST /api/recipients/close`

### Drives
- `POST /api/drives/`

- `GET /api/drives/`

- `POST /api/drives/register`