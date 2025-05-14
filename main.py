
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaGiveaway
from telethon.tl.functions.channels import JoinChannelRequest
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Telegram API
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
giveaway_channels = os.getenv('GIVEAWAY_CHANNELS').split(',')
your_country = os.getenv('YOUR_COUNTRY')
your_telegram_id = int(os.getenv('YOUR_TELEGRAM_ID'))  # 👈 DM yuboriladigan ID

# Client
client = TelegramClient('1', api_id, api_hash)


# 📩 Sizga DM yuboruvchi funksiya
async def send_message_to_me(text):
    try:
        await client.send_message(your_telegram_id, text)
    except Exception as e:
        print(f"❌ Xabar yuborishda xatolik: {e}")


@client.on(events.NewMessage(chats=giveaway_channels))
async def giveaway_handler(event):
    media = event.message.media
    if isinstance(media, MessageMediaGiveaway):
        stars_count = getattr(media, 'stars', None)
        premium_months = getattr(media, 'months', None)
        channels_to_join = getattr(media, 'channels', [])
        countries_iso2 = getattr(media, 'countries_iso2', [])

        # Sovrin turi
        if stars_count:
            msg = f"🎉 Stars Giveaway topildi: {stars_count} ta yulduz!"
        elif premium_months:
            msg = f"🎉 Premium Giveaway topildi: {premium_months} oy Premium!"
        else:
            msg = "🎉 Giveaway topildi, lekin turi noma'lum."
        
        print(msg)
        await send_message_to_me(msg)

        # Mamlakat tekshiruvi
        if countries_iso2 and your_country not in countries_iso2:
            warning = f"🚫 Siz ishtirok eta olmaysiz (davlat: {your_country})."
            print(warning)
            await send_message_to_me(warning)
            return

        # Kanallarga qo‘shilish
        if channels_to_join:
            await send_message_to_me("📲 Kanallarga qo‘shilish boshlandi...")
            for channel_id in channels_to_join:
                try:
                    result = await client(JoinChannelRequest(channel_id))
                    success = f"✅ Qo‘shildi: {channel_id}"
                    print(success)
                    await send_message_to_me(success)
                except Exception as e:
                    fail = f"⚠️ Qatnashib bo‘lmadi: {channel_id} - {e}"
                    print(fail)
                    await send_message_to_me(fail)
        else:
            print("ℹ️ Kanallar ko‘rsatilmagan.")
            await send_message_to_me("ℹ️ Kanallar ko‘rsatilmagan.")
    else:
        print("⏭️ Giveaway yo‘q.")


# Run client

with client:
    print("👀 Giveawaylar uchun xabarlarni tinglamoqda...")
    client.run_until_disconnected()
