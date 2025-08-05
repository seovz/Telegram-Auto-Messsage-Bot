import asyncio
from telethon.sync import TelegramClient
import schedule
import time
from datetime import datetime

# Telegram API credentials
api_id = 23942111 #api id https://my.telegram.org/apps
api_hash = 'b96aaab7c58f661a96afec67c92e69c7' #api hash https://my.telegram.org/apps
phone_number = '+' #your phone number


session_name = 'Active_session'

# Message text to send
message_text = """YOUR TEXT MESSAGE"""


client = TelegramClient(session_name, api_id, api_hash)

async def send_message_to_all_chats():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📢 Starting to send messages to all groups...")
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            try:
                chat_name = dialog.name
                await client.send_message(dialog.entity, message_text)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Message sent -> {chat_name} (ID: {dialog.id})")
                await asyncio.sleep(10)
            except Exception as e:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ ERROR -> {dialog.name} (ID: {dialog.id}): {e}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Finished sending messages to all groups.")

def schedule_job():
    asyncio.get_event_loop().run_until_complete(send_message_to_all_chats())

async def main():
    await client.start(phone_number)
    print("✅ Telegram connection successful.")

    await send_message_to_all_chats()

    schedule.every(30).minutes.do(schedule_job)

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

with client:
    client.loop.run_until_complete(main())
