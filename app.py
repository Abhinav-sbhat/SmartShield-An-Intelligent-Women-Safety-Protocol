from flask import Flask, render_template, request, redirect, url_for, jsonify
import threading
import pywhatkit as kit
import pygame
import time
import random


app = Flask(__name__)

user_passcode = None  
TIMEOUT = 10
emergency_active = False
danger_detected = False
alert_sent = False
timer = None
repeating_alert_timer = None 
message_loop_active = False  

PHONE_NUMBERS = ["+918431011609", "+916362382890"]

# Fallback locations if geolocation fails
USER_LOCATIONS = [
    (12.939443, 77.545355),
    (12.939626, 77.545125),
    (12.939145, 77.545361),
    (12.939828, 77.545380)
]
# Global variable to store real-time location from browser
current_location = None  # Will be (lat, lng) or None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activate', methods=['POST'])
def activate():
    global emergency_active, alert_sent, current_location
    emergency_active = True
    alert_sent = False
    current_location = None  # Reset location on new activation
    return redirect(url_for('set_passcode'))

@app.route('/set_passcode', methods=['GET', 'POST'])
def set_passcode():
    global user_passcode
    if request.method == 'POST':
        user_passcode = request.form['new_passcode']
        return redirect(url_for('reenter_passcode')) 
    return render_template('set_passcode.html')

@app.route('/reenter_passcode')
def reenter_passcode():
    global timer, alert_sent, message_loop_active
    if timer is None and not alert_sent:
        timer = threading.Timer(TIMEOUT, timeout_handler)
        timer.start()
    message_loop_active = True  
    return render_template('index3.html')

# New route to receive location from frontend
@app.route('/submit_location', methods=['POST'])
def submit_location():
    global current_location
    data = request.get_json()
    if data and 'lat' in data and 'lng' in data:
        current_location = (float(data['lat']), float(data['lng']))
        print(f"Real-time location received: {current_location}")
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@app.route('/verify_reenter_passcode', methods=['POST'])
def verify_reenter_passcode():
    global danger_detected, timer, alert_sent, repeating_alert_timer, message_loop_active, current_location

    passcode = request.form['passcode']
    
    if passcode == user_passcode:
        # Correct passcode → deactivate everything
        danger_detected = False
        emergency_active = False
        message_loop_active = False  
        current_location = None
        
        if timer is not None:
            timer.cancel()
            timer = None
        if repeating_alert_timer is not None:
            repeating_alert_timer.cancel() 
            repeating_alert_timer = None
        
        return render_template('passcode.html')  # Safe page
    else:
        # Wrong passcode → trigger alert
        if not alert_sent:
            danger_detected = True
            alert_sent = True
            if timer is not None:
                timer.cancel()
                timer = None
            play_emergency_sound()  
            return redirect(url_for('send_alert'))
        else:
            return render_template('alert.html')

def play_emergency_sound():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(r'C:\Users\abhib\Desktop\Projects\5th sem Mini Project\activate message.mp3')
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Sound play error: {e}")

def timeout_handler():
    global alert_sent
    if not alert_sent:
        play_emergency_sound()  
        send_alert()

@app.route('/send_alert')
def send_alert():
    global danger_detected, alert_sent, repeating_alert_timer, message_loop_active, current_location

    danger_detected = True
    alert_sent = True

    # Use real location if available, otherwise fallback
    if current_location:
        lat, lng = current_location
        print(f"Using real-time location: {lat}, {lng}")
    else:
        selected_location = random.choice(USER_LOCATIONS)
        lat, lng = selected_location
        print(f"Geolocation unavailable. Using fallback: {lat}, {lng}")

    location_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    
    message = (
        f"⚠️ EMERGENCY ALERT ⚠️\n\n"
        f"I am in danger and need immediate help!\n\n"
        f"📍 My Current Location:\n{location_link}\n\n"
        f"Please contact me urgently or inform authorities.\n"
        f"Thank you!\n"
    )

    try:
        send_whatsapp_message_sequence(PHONE_NUMBERS, message)
        
        # Repeat alert every 20 seconds if still in emergency mode
        if emergency_active and message_loop_active:
            repeating_alert_timer = threading.Timer(20, send_alert)
            repeating_alert_timer.start()

        return render_template('alert.html')
    except Exception as e:
        return f"Error sending WhatsApp message: {str(e)}"

def send_whatsapp_message_sequence(phone_numbers, message, retries=3):
    initial_wait_time = 15  
    print(f"Waiting {initial_wait_time} seconds for WhatsApp Web to load...")
    time.sleep(initial_wait_time) 
    
    for i, number in enumerate(phone_numbers):
        print(f"Sending to {number}...")
        for attempt in range(retries):
            try:
                kit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
                print(f"Message sent successfully to {number}")
                time.sleep(10)
                break  
            except Exception as e:
                print(f"Error sending to {number} (attempt {attempt+1}): {e}")
                time.sleep(5)

if __name__ == "__main__":
    app.run(debug=True)
