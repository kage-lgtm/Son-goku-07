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

# Aapki Welcome Image ka Direct URL
WELCOME_PHOTO_URL = "https://i.ibb.co/JjcNKKg4/IMG-20261003-121133-129.jpg"

# Aapke Channels ke Naam aur Links
CHANNEL_1_NAME = "DXE Studio"
CHANNEL_1_LINK = "https://t.me/dubxempirestudio"

CHANNEL_2_NAME = "Join Channel 2"
CHANNEL_2_LINK = "https://t.me/+VzwHuVRrPYljOGJl"

# Admin User IDs (Yahan apni Telegram User ID daal sakte hain broadcast/ban ke liye)
ADMINS = [123456789]  # Apni ID yahan rakh sakte hain

# ==================== /START & EPISODE HANDLER ====================
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    first_name = message.from_user.first_name
    args = message.command
    
    # Check karein agar user Mini App se episode parameter ke sath aaya hai
    if len(args) > 1 and args[1].startswith("ep_"):
        ep_id = args[1].split("ep_")[1]
        
        caption = (
            f"🔥 **Hello {first_name}!** 🔥\n\n"
            f"🎬 **EPISODE ID:** `{ep_id}`\n"
            "✨ Hindi Fan Dubbed • 1080p HD\n\n"
            "⚠️ **Warning:** Yeh message 15 minutes ke baad automatically delete ho jayega! Kripya link save kar lein."
        )
        
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


# ==================== FILE STORE & LINK COMMANDS ====================

@app.on_message(filters.command("genlink") & filters.private)
async def genlink_handler(client, message):
    await message.reply_text(
        "🔗 **GenLink Command:**\n"
        "Kisi bhi file ya message ka link banane ke liye us message ko is bot par forward karein ya channel me bot ko admin banakar post ka link bhejein."
    )

@app.on_message(filters.command("batch") & filters.private)
async def batch_handler(client, message):
    await message.reply_text(
        "📦 **Batch Link Command:**\n"
        "Ek sath multiple messages ka link banane ke liye channel ke pehle aur aakhri message ka link ya forward use karein."
    )

@app.on_message(filters.command("universal_link") & filters.private)
async def universal_link_handler(client, message):
    await message.reply_text("🌐 **Universal Link:** Multiple messages ko kisi bhi clone se access karne ke liye yeh command hai.")

@app.on_message(filters.command("custom_batch") & filters.private)
async def custom_batch_handler(client, message):
    await message.reply_text("📑 **Custom Batch:** Multiple random messages ko ek sath store karne ke liye.")

@app.on_message(filters.command("special_link") & filters.private)
async def special_link_handler(client, message):
    await message.reply_text("⭐ **Special Link:** Editable links generate karne ke liye (Moderators only).")

@app.on_message(filters.command("shortener") & filters.private)
async def shortener_handler(client, message):
    await message.reply_text("✂️ **Shortener:** Apne shareable links ko short karne ke liye settings configure karein.")

@app.on_message(filters.command("settings") & filters.private)
async def settings_handler(client, message):
    await message.reply_text("⚙️ **Bot Settings:** Aap yahan apni zaroorat ke mutabiq auto-delete timer, force-subscription aur baaki cheezein customize kar sakte hain.")

@app.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ Aapke paas yeh command use karne ki permission nahi hai.")
        return
    await message.reply_text("📢 **Broadcast:** Sabhi users ko message bhejne ke liye message aage forward karein.")

@app.on_message(filters.command("ban") & filters.private)
async def ban_handler(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ Yeh command sirf admin ke liye hai.")
        return
    await message.reply_text("🚫 **Ban User:** Kisi user ko ban karne ke liye use karein.")

@app.on_message(filters.command("unban") & filters.private)
async def unban_handler(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ Yeh command sirf admin ke liye hai.")
        return
    await message.reply_text("✅ **Unban User:** Banned user ko hataane ke liye use karein.")


# ==================== AUTO-DELETE FUNCTION ====================
async def delete_message_after_delay(message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


if __name__ == "__main__":
    print("🤖 Son Goku Bot with Full Commands & DXE Studio is starting...")
    app.run()
