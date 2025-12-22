from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import threading
import pywhatkit as kit
import pygame
import time
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for sessions

user_passcode = None  
TIMEOUT = 10
emergency_active = False
danger_detected = False
alert_sent = False
timer = None
repeating_alert_timer = None 
message_loop_active = False  

# Store location in session
PHONE_NUMBERS = ["+918431011609", "+916362382890"]

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/activate', methods=['POST'])
def activate():
    global emergency_active, alert_sent
    emergency_active = True
    alert_sent = False
    
    # Check if we have location stored
    if 'user_location' not in session or session['user_location'] is None:
        return redirect(url_for('get_location_page'))  # Redirect to get location first
    
    return redirect(url_for('set_passcode'))

@app.route('/get_location_page')
def get_location_page():
    """Page to get accurate GPS location"""
    return render_template('get_location.html')

@app.route('/save_gps_location', methods=['POST'])
def save_gps_location():
    """Save accurate GPS location from browser"""
    try:
        data = request.json
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        accuracy = data.get('accuracy', None)
        
        # Store in session
        session['user_location'] = {
            'latitude': latitude,
            'longitude': longitude,
            'accuracy': accuracy,
            'timestamp': datetime.now().isoformat()
        }
        
        # Also get address for better context
        address = get_address_from_coords(latitude, longitude)
        if address:
            session['user_location']['address'] = address
        
        return jsonify({
            'success': True,
            'message': 'Location saved successfully',
            'location': session['user_location'],
            'map_link': f'https://maps.google.com/?q={latitude},{longitude}'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

def get_address_from_coords(lat, lon):
    """Get human-readable address from coordinates (free API)"""
    try:
        # Using OpenStreetMap Nominatim (free, no API key needed)
        response = requests.get(
            f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1',
            headers={'User-Agent': 'EmergencyAlertApp/1.0'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            address = data.get('display_name', '')
            
            # Extract important parts
            address_parts = []
            if data.get('address'):
                addr = data['address']
                if addr.get('road'): address_parts.append(addr['road'])
                if addr.get('suburb'): address_parts.append(addr['suburb'])
                if addr.get('city') or addr.get('town') or addr.get('village'):
                    address_parts.append(addr.get('city') or addr.get('town') or addr.get('village'))
                if addr.get('state'): address_parts.append(addr['state'])
                if addr.get('country'): address_parts.append(addr['country'])
            
            return ', '.join(address_parts) if address_parts else address
    except:
        pass
    return None

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
    
    # Show current location in template
    current_location = session.get('user_location', {})
    return render_template('index3.html', location=current_location)

@app.route('/verify_reenter_passcode', methods=['POST'])
def verify_reenter_passcode():
    global danger_detected, timer, alert_sent, repeating_alert_timer, message_loop_active
    passcode = request.form['passcode']
    
    if passcode == user_passcode:
        danger_detected = False
        emergency_active = False
        message_loop_active = False  
        if timer is not None:
            timer.cancel()
            timer = None
        if repeating_alert_timer is not None:
            repeating_alert_timer.cancel() 
            repeating_alert_timer = None
        return render_template('passcode.html')
    else:
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
    pygame.mixer.init()
    pygame.mixer.music.load(r'C:\Users\abhib\Desktop\Projects\5th sem Mini Project\activate message.mp3')
    pygame.mixer.music.play()

def timeout_handler():
    global alert_sent
    if not alert_sent:
        play_emergency_sound()  
        send_alert()

@app.route('/send_alert')
def send_alert():
    global danger_detected, alert_sent, repeating_alert_timer, message_loop_active
    danger_detected = True
    alert_sent = True

    # Get location from session
    location_data = session.get('user_location')
    if not location_data:
        return "Error: No location available. Please enable GPS."
    
    lat = location_data['latitude']
    lon = location_data['longitude']
    accuracy = location_data.get('accuracy', 'Unknown')
    address = location_data.get('address', '')
    
    # Multiple map links for reliability
    google_maps_link = f"https://maps.google.com/?q={lat},{lon}"
    openstreetmap_link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}"
    what3words_link = get_what3words_link(lat, lon)  # Alternative
    
    # Better formatted message
    message = (
        f"⚠️ *EMERGENCY ALERT - URGENT ASSISTANCE REQUIRED* ⚠️\n\n"
        f"🚨 *I AM IN DANGER AND NEED IMMEDIATE HELP!* 🚨\n\n"
        f"📍 *PRECISE LOCATION*:\n"
        f"• Google Maps: {google_maps_link}\n"
        f"• Coordinates: {lat}, {lon}\n"
        f"• Accuracy: ±{accuracy}m\n\n"
    )
    
    if address:
        message += f"📌 *NEAR*: {address}\n\n"
    
    message += (
        f"🕒 *Time*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"🚑 *PLEASE*:\n"
        f"1. Call emergency services immediately\n"
        f"2. Share with nearby contacts\n"
        f"3. Attempt to reach me\n\n"
        f"📱 *This is an automated emergency alert*"
    )

    try:
        send_whatsapp_message_sequence(PHONE_NUMBERS, message)
        
        if emergency_active and message_loop_active:
            repeating_alert_timer = threading.Timer(20, send_alert)
            repeating_alert_timer.start()

        return render_template('alert.html', 
                             location=location_data,
                             google_maps_link=google_maps_link,
                             openstreetmap_link=openstreetmap_link)
    except Exception as e:
        return f"Error sending WhatsApp message: {str(e)}"

def get_what3words_link(lat, lon):
    """Get what3words link (alternative location system)"""
    try:
        response = requests.get(
            f'https://api.what3words.com/v3/convert-to-3wa',
            params={'coordinates': f'{lat},{lon}', 'key': 'YOUR_KEY_HERE'},  # Free key available
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            words = data.get('words')
            if words:
                return f'https://what3words.com/{words}'
    except:
        pass
    return ""

def send_whatsapp_message_sequence(phone_numbers, message, retries=3):
    initial_wait_time = 15 
    print(f"Waiting {initial_wait_time} seconds for WhatsApp Web to load...")
    time.sleep(initial_wait_time) 
    
    for i, number in enumerate(phone_numbers):
        for attempt in range(retries):
            try:
                kit.sendwhatmsg_instantly(number, message, wait_time=10)
                print(f"✓ Emergency alert sent to {number}")
                print(f"  Location accuracy: Good")
                time.sleep(10) 
                break 
            except kit.core.exceptions.CallTimeException:
                print(f"↻ Retry {attempt + 1}/{retries} for {number}")
                time.sleep(5) 
            except Exception as e:
                print(f"✗ Error sending to {number}: {e}")
                break

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)