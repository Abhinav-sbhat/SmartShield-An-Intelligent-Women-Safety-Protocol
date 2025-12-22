# 🛡️ SmartShield  
## An Intelligent Women Safety Protocol

SmartShield is a **real-time, intelligent women safety system** designed to provide **instant emergency alerts** using a secure passcode mechanism, automated messaging, and live location tracking.  
The system ensures **rapid response during critical situations** by automatically notifying trusted contacts when the user is unable to confirm safety.

---

## 🚀 Key Features

- 🔐 **Passcode-Protected Emergency Activation**
- ⏱️ **Automatic Alert Trigger on Timeout or Wrong Passcode**
- 📍 **Real-Time Location Sharing (Google Maps Integration)**
- 📲 **Instant WhatsApp Alert Messaging**
- 🔊 **Emergency Sound & Alert Beeps**
- 🌐 **User-Friendly Web Interface (HTML + CSS)**
- ⚡ **Flask-Based Backend for Real-Time Control**

---

## 🧠 System Working (High-Level)

1. User activates **Emergency Mode** from the web interface  
2. User sets a **secure 4-digit passcode**  
3. System prompts for passcode re-entry within a limited time  
4. ❌ If passcode is **wrong or not entered**:
   - Emergency alarm is triggered
   - WhatsApp alert message is sent automatically
   - Live location is shared with trusted contacts  
5. ✅ If passcode is correct, emergency mode is safely deactivated

---

## 🏗️ System Architecture

---

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Communication & Utilities
- PyWhatKit (WhatsApp Automation)
- Google Maps (Location Sharing)
- OS & Time Modules

---

## 📁 Project Structure

SmartShield/
│
├── app.py
├── Run_file.py
├── Templates/
│ ├── index1.html
│ ├── set_passcode.html
│ ├── passcode.html
│ ├── alert.html
│ └── google_maps_location.html
│
├── static/
│ └── styles.css
│
├── activate message.mp3
├── PyWhatKit_DB.txt
└── README.md


---

## ▶️ How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Abhinav-sbhat/SmartShield-An-Intelligent-Women-Safety-Protocol.git

cd SmartShield-An-Intelligent-Women-Safety-Protocol

pip install flask pywhatkit

python app.py

http://127.0.0.1:5000
```

⚠️ Important Notes

WhatsApp Web must be logged in before sending alerts

Internet connection is required for messaging & maps

Location values can be customized in backend

System is designed for educational and safety purposes

🎯 Future Enhancements

📱 Mobile App Integration (Android)

🤖 AI-Based Threat Detection

⌚ Wearable Device Support

📡 IoT Panic Button Integration

☁️ Cloud Deployment & SMS Backup
