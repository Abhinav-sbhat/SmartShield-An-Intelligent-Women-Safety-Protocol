import time
import random
import threading
import pywhatkit as kit
import datetime
from geopy.distance import geodesic
from geopy.point import Point

TIME_INTERVAL = 15
TIMEOUT = 10
MESSAGE_INTERVAL = 300  # 5 minutes

emergency_active = False
danger_detected = False
user_passcode = ""
user_phone_number = "+916362382890"

HOME_LATITUDE = 12.8701
HOME_LONGITUDE = 77.5603
HOME_LOCATION = (HOME_LATITUDE, HOME_LONGITUDE)

def activate_emergency():
    global emergency_active, user_passcode

    if emergency_active:
        print("Emergency is already active.")
        return

    user_passcode = input("Enter a safety passcode: ")
    print(f"Emergency activated! Alerts will be sent to {user_phone_number}.")
    emergency_active = True

    while emergency_active:
        print("\n--- Emergency Mode ---")
        print("1. Continue Tracking and Safety Check")
        print("2. Deactivate Emergency")
        choice = input("Enter your choice: ")

        if choice == "1":
            location = track_location()
            if not danger_detected:
                safety_check(location)
            send_whatsapp_alert(location)
            recheck_passcode(location)  # Check passcode after sending alert
            time.sleep(TIME_INTERVAL)
        elif choice == "2":
            deactivate_emergency()
        else:
            print("Invalid choice! Please try again.")

def track_location():
    print("Tracking location... (Simulated)")
    random_location = create_random_location(HOME_LOCATION, max_distance_km=5)
    print(f"Current location: {random_location}")
    return random_location

def create_random_location(home_location, max_distance_km):
    distance_km = random.uniform(0, max_distance_km)
    bearing = random.uniform(0, 360)
    origin = Point(home_location)
    destination = geodesic(kilometers=distance_km).destination(origin, bearing)
    return (destination.latitude, destination.longitude)

def safety_check(location):
    global danger_detected
    print(f"Safety check: Re-enter your safety passcode within {TIMEOUT} seconds.")
    timer = threading.Timer(TIMEOUT, timeout_handler, [location])
    timer.start()
    input_code = input("Enter the passcode: ")

    if timer.is_alive():
        timer.cancel()

    if input_code == user_passcode:
        print("Safety check passed. You're safe.")
    else:
        print("Incorrect passcode! Alerting authorities and sending WhatsApp message...")
        danger_detected = True
        send_alert_to_authorities(location)

def timeout_handler(location):
    global danger_detected
    print("No input received within the time limit. Alerting authorities and sending WhatsApp message...")
    danger_detected = True
    send_alert_to_authorities(location)

def send_alert_to_authorities(location):
    print("Alert sent to authorities! Help is on the way.")
    send_whatsapp_alert(location)

def send_whatsapp_alert(location):
    global user_phone_number

    if not user_phone_number:
        print("No phone number provided. Unable to send WhatsApp message.")
        return

    try:
        now = datetime.datetime.now()
        scheduled_time = now + datetime.timedelta(minutes=2)
        hour = scheduled_time.hour
        minute = scheduled_time.minute
        message = f"Help me! I am in danger. My location is: Latitude: {location[0]}, Longitude: {location[1]}."
        print(f"Scheduling WhatsApp message to {user_phone_number} in 2 minutes...")
        kit.sendwhatmsg(user_phone_number, message, hour, minute, 15)
        print(f"WhatsApp message scheduled to be sent to {user_phone_number} at {hour}:{minute}.")
    except Exception as e:
        print(f"Failed to send WhatsApp message. Error: {e}")

def recheck_passcode(location):
    # Function to check passcode after sending alert
    print(f"Please re-enter your safety passcode within {MESSAGE_INTERVAL / 60} minutes.")
    timer = threading.Timer(MESSAGE_INTERVAL, resend_whatsapp_alert, [location])
    timer.start()

    input_code = input("Enter the passcode: ")

    if timer.is_alive():
        timer.cancel()

    if input_code == user_passcode:
        print("Passcode verified. You are safe. Terminating the server.")
        terminate_server()  # Terminate server if the passcode is correct
    else:
        print("Incorrect passcode! Resending WhatsApp alert...")
        send_whatsapp_alert(location)

def resend_whatsapp_alert(location):
    print("Resending WhatsApp alert due to incorrect passcode.")
    send_whatsapp_alert(location)

def terminate_server():
    print("Exiting the emergency mode and terminating the server...")
    exit(0)  # Terminate the program

def deactivate_emergency():
    global emergency_active, danger_detected
    if not emergency_active:
        print("Emergency is not active.")
        return

    if danger_detected:
        print("Cannot deactivate. Danger has been detected. Authorities have been alerted.")
        return

    passcode = input("Enter your safety passcode to deactivate: ")
    if passcode == user_passcode:
        print("Emergency deactivated.")
        emergency_active = False
        danger_detected = False
    else:
        print("Incorrect passcode. Emergency remains active.")

def main():
    while True:
        print("\n--- Women Safety Device Menu ---")
        print("1. Activate Emergency")
        print("2. Deactivate Emergency")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            activate_emergency()
        elif choice == "2":
            deactivate_emergency()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
