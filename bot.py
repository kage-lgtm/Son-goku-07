import asyncio
import logging
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Logging setup
logging.basicConfig(level=logging.INFO)

# Aapke Telegram Credentials
API_ID = 38215355
API_HASH = "3f095c170be8c744b8f3d7f9c75ae544"
BOT_TOKEN = "8555113283:AAFTY7YNDz52tNArdoeIMXpQwc8efMXTylA"

# Pyrogram Client initialize karein
app = Client(
    "son_goku_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Aapki nayi Welcome Image ka Direct URL
WELCOME_PHOTO_URL = "https://i.ibb.co/JjcNKKg4/IMG-20261003-121133-129.jpg"

# Aapke Channels ke Naam aur Links
CHANNEL_1_NAME = "DXE Studio"
CHANNEL_1_LINK = "https://t.me/dubxempirestudio"

CHANNEL_2_NAME = "Join Channel 2"
CHANNEL_2_LINK = "https://t.me/+VzwHuVRrPYljOGJl"

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    args = message.command
    first_name = message.from_user.first_name
    
    # Check karein agar user Mini App se episode parameter ke sath aaya hai
    if len(args) > 1 and args[1].startswith("ep_"):
        ep_id = args[1].split("ep_")[1]
        
        caption = (
            f"🔥 **Hello {first_name}!** 🔥\n\n"
            f"🎬 **EPISODE ID:** `{ep_id}`\n"
            "✨ Hindi Fan Dubbed • 1080p HD\n\n"
            "⚠️ **Warning:** Yeh message 15 minutes ke baad automatically delete ho jayega! Kripya link save kar lein."
        )
        
        # Episode Watch/Download button aur dono channels ke buttons
        watch_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 Watch / Download Episode", url="https://t.me/+YourPrivateChannelInviteLink")],
            [InlineKeyboardButton(CHANNEL_1_NAME, url=CHANNEL_1_LINK)],
            [InlineKeyboardButton(CHANNEL_2_NAME, url=CHANNEL_2_LINK)]
        ])
        
        try:
            sent_msg = await message.reply_photo(
                photo=WELCOME_PHOTO_URL,
                caption=caption,
                reply_markup=watch_keyboard
            )
            
            # **15 Minutes Auto-Delete Timer (900 seconds)**
            asyncio.create_task(delete_message_after_delay(sent_msg, 900))
            
        except Exception as e:
            print(f"Episode send error: {e}")
            await message.reply_text("❌ Kuch galat ho gaya. Kripya dobara try karein.")
            
    else:
        # Normal Start Message with Image and Channel Buttons
        caption = (
            f"👋 **Hello {first_name}!**\n\n"
            "✨ DXE Studio bot me aapka swagat hai. Kripya neeche diye gaye channels ko join karein!"
        )
        
        welcome_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(CHANNEL_1_NAME, url=CHANNEL_1_LINK)],
            [InlineKeyboardButton(CHANNEL_2_NAME, url=CHANNEL_2_LINK)]
        ])
        
        try:
            await message.reply_photo(
                photo=WELCOME_PHOTO_URL,
                caption=caption,
                reply_markup=welcome_keyboard
            )
        except Exception as e:
            print(f"Photo error: {e}")
            await message.reply_text(caption, reply_markup=welcome_keyboard)

# 15 Minute Baad Message Delete Karne Wala Function
async def delete_message_after_delay(message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass

if __name__ == "__main__":
    print("🤖 Son Goku Bot with DXE Studio & Image is starting...")
    app.run()
