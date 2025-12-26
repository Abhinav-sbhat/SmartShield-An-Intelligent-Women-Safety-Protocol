🛡️ SmartShield — An Intelligent Women Safety Protocol

SmartShield is a real-time intelligent women safety system that enables instant emergency response through a passcode-based safety validation mechanism, automated WhatsApp alerts, and live location sharing. The system is designed to help women trigger silent emergency support even when they are unable to manually call for help, ensuring rapid response during critical situations. 


🚨 Problem Statement

Women in unsafe or threatening situations often cannot manually call for help, leading to delayed response and increased risk. SmartShield addresses this by providing an auto-trigger emergency protocol that activates when the user fails to confirm safety within a time limit. 


💡 Solution Overview

SmartShield implements a secure passcode re-entry fail-safe model that:

Detects when the user cannot confirm safety

Triggers automatic WhatsApp alerts

Shares real-time live location (Google Maps link)

Activates emergency alarm sounds

This ensures instant support and faster response during critical situations. 


🌟 Key Features

🔐 Secure 4-digit passcode protection

⏱️ Auto-alert on timeout or wrong passcode

📍 Live GPS location sharing via Google Maps link

📲 Instant WhatsApp emergency messaging

🔊 Emergency siren & alert tones

🌑 Dark-mode / neon UI for night environments

⚙️ Modular Flask backend with real-time logic 


🧠 System Workflow

User activates Emergency Mode from the browser

User sets a secure passcode

System prompts for passcode re-entry within a limited time

❌ If passcode is wrong / timeout occurs

Emergency alarm triggers

WhatsApp alert sent automatically

Live location shared to trusted contacts

✅ If passcode is correct

Emergency mode safely deactivates 


🏗️ Architecture (High-Level)

Browser UI → Flask Backend → Timer & Validation Logic

Auto-Trigger Alert Engine → WhatsApp Automation → Location Sharing

Emergency loop re-activates until safely resolved 


🧰 Technology Stack
Frontend

HTML5, CSS3, JavaScript

Backend

Python, Flask

Communication & Utilities

PyWhatKit (WhatsApp automation)

Geopy / Google Location Services

OS & Time modules 

🌍 Google Technologies Used

HTML5 Geolocation API via navigator.geolocation.watchPosition() (high-accuracy mode)

Google Maps link generation for live location sharing

Chrome / Android Google Location Services for GPS + Wi-Fi + Cell-tower positioning
(Complies with Google guidelines — Dec 2025) 


📁 Project Structure
SmartShield/
│
├── app.py
├── Run_file.py
├── templates/
│   ├── index1.html
│   ├── set_passcode.html
│   ├── passcode.html
│   ├── alert.html
│   └── google_maps_location.html
│
├── static/
│   └── styles.css
│
├── activate message.mp3
├── PyWhatKit_DB.txt
└── README.md

▶️ How to Run the Project (MVP)

1️⃣ Clone the Repository
``` bash 
git clone https://github.com/Abhinav-sbhat/SmartShield-An-Intelligent-Women-Safety-Protocol.git
cd SmartShield-An-Intelligent-Women-Safety-Protocol

```
2️⃣ Install Dependencies
``` bash 
pip install flask pywhatkit geopy
```
3️⃣ Run the Application
``` bash 
python app.py
```

Open in browser:

http://127.0.0.1:5000

⚠️ Important Notes

WhatsApp Web must be logged in before alerts can be sent

Internet connection is required for messaging & maps

Location values can be customized in backend

System is built for educational and safety assistance purposes

🚀 Future Enhancements

📱 Mobile App (Android)

🤖 AI-based threat detection

⌚ Wearable / Smartwatch trigger

📡 IoT panic button integration

☁️ Cloud deployment & SMS backup
