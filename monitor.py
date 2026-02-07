import requests
import time
import os
from datetime import datetime

# --- CONFIGURATION ---
# The URL to monitor
URL = "https://reservation.umai.io/en/block/rembayung"

# Check interval in seconds (default: 5 minutes)
CHECK_INTERVAL = 300

# Telegram Configuration (Optional)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8012222526:AAENnVw6aHAeP2HVxfuFg9mEbSTne3_f6Uo")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "856214397")

# WhatsApp Configuration (Optional - via CallMeBot API)
# Get your API key by sending "I allow callmebot to send me messages" to +34 644 66 32 62 on WhatsApp
WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "YOUR_PHONE_NUMBER_WITH_COUNTRY_CODE")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "YOUR_API_KEY")

# --- NOTIFICATION LOGIC ---

def send_telegram_message(message):
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN":
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def send_whatsapp_message(message):
    if WHATSAPP_API_KEY == "YOUR_API_KEY":
        return
    # CallMeBot API: https://api.callmebot.com/whatsapp.php?phone=[phone]&text=[text]&apikey=[apikey]
    url = "https://api.callmebot.com/whatsapp.php"
    params = {
        "phone": WHATSAPP_PHONE,
        "text": message,
        "apikey": WHATSAPP_API_KEY
    }
    try:
        requests.get(url, params=params)
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

def notify(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] NOTIFICATION: {message}")
    
    # Log to a file so you have a history of availability
    with open("availability_history.log", "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    
    send_telegram_message(message)
    send_whatsapp_message(message)

# --- MONITORING LOGIC ---

def check_availability():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        content = response.text.lower()
        
        # Check for keywords that indicate "Fully Booked"
        # Based on analysis, the page says "We are fully booked" or "at capacity"
        if "fully booked" in content or "at capacity" in content:
            return False, "Still fully booked."
        
        # If the keywords are NOT found, it might be available or the structure changed
        return True, "Slots might be available! Check here: " + URL
        
    except Exception as e:
        return None, f"Error checking site: {e}"

def main():
    print(f"Starting Rembayung monitor on {URL}...")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    
    last_state = None # None: Initial, False: Unavailable, True: Available
    
    while True:
        available, msg = check_availability()
        
        if available is None:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
        elif available != last_state:
            # State changed
            if available:
                notify(f"🚨 ALERT: Rembayung available slots detected!\n\nBook here: {URL}")
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
            last_state = available
        else:
            # No state change
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
