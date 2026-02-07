# Rembayung Reservation Monitor

A lightweight Python script to monitor reservation availability for **Rembayung** (by Khairulaming) via the UMAI reservation system. Receive instant notifications on Telegram as soon as a slot opens up!

## 🚀 Features

- **Real-time Monitoring**: Polling the reservation page for changes in status.
- **Instant Notifications**: Automated alerts sent directly to your Telegram bot.
- **Availability History**: Automatically logs every detected opening to `availability_history.log`.
- **Easy Execution**: Includes a one-click `.bat` launcher for Windows users.
- **Simulation Mode**: Includes a test script to verify your notification setup.

## 🛠️ Setup

### Prerequisites
- Python 3.x
- `requests` library

```bash
pip install requests
```

### 1. Telegram Bot Configuration
1. Create a bot via [@BotFather](https://t.me/botfather).
2. Get your Chat ID (use [@userinfobot](https://t.me/userinfobot)).
3. Open `monitor.py` and enter your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

### 2. Usage
- **Windows**: Double-click `run_monitor.bat`.
- **Other Systems**: Run `python monitor.py`.

## 📂 Project Structure

- `monitor.py`: The main monitoring engine.
- `run_monitor.bat`: Windows launcher script.
- `test_simulation.py`: Simulation script to test notifications.
- `availability_history.log`: (Auto-generated) Log of historical availability.

## ⚠️ Disclaimer
This project is for personal use to assist with manual reservations. Please use responsibly and respect the restaurant's booking policies.

---
Created with ❤️ for Rembayung fans.
