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

# Bot ka username (Link banane ke liye)
BOT_USERNAME = "Son_Goku_07bot"


# ==================== /START & EPISODE HANDLER ====================
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    first_name = message.from_user.first_name
    args = message.command
    
    # Check karein agar user Mini App ya deep-link se aaya hai
    if len(args) > 1:
        payload = args[1]
        
        # Agar payload 'ep_' se hai ya koi file id/number hai
        caption = (
            f"🔥 **Hello {first_name}!** 🔥\n\n"
            f"🎬 **CONTENT ID:** `{payload}`\n"
            "✨ Hindi Fan Dubbed • 1080p HD\n\n"
            "⚠️ **Warning:** Yeh message 15 minutes ke baad automatically delete ho jayega! Kripya link save kar lein."
        )
        
        watch_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 Watch / Download Episode", url=f"https://t.me/{BOT_USERNAME}?start={payload}")],
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


# ==================== REAL LINK GENERATOR (FORWARD HANDLER) ====================
@app.on_message(filters.forwarded & filters.private)
async def forwarded_message_handler(client, message):
    """
    Jab aap channel se koi post is bot par forward karenge, 
    yeh handler uska unique payload/ID banakar link dega.
    """
    try:
        # Forwarded message ki chat aur message ID se unique code banate hain
        if message.forward_from_chat:
            chat_id = message.forward_from_chat.id
            msg_id = message.forward_from_message_id
            
            # Unique payload encode kar lete hain (jaise: c_chatid_msgid)
            payload = f"post_{abs(chat_id)}_{msg_id}"
            generated_link = f"https://t.me/{BOT_USERNAME}?start={payload}"
            
            await message.reply_text(
                "✅ **Link Generated Successfully!**\n\n"
                f"🔗 **Your Deep Link:**\n`{generated_link}`\n\n"
                "Is link ko aap apne Ads / Mini App ke button ke peeche laga sakte hain.",
                disable_web_page_preview=True
            )
        else:
            await message.reply_text("⚠️ Kripya kisi Public/Private channel ki post ko directly forward karein.")
    except Exception as e:
        await message.reply_text(f"❌ Error generating link: {e}")


# ==================== OTHER COMMANDS ====================
@app.on_message(filters.command("genlink") & filters.private)
async def genlink_cmd(client, message):
    await message.reply_text("🔗 **GenLink:** Aap apne channel se kisi bhi episode/poster message ko seedha is bot par **forward** karein, bot aapko uska link de dega!")

@app.on_message(filters.command("batch") & filters.private)
async def batch_cmd(client, message):
    await message.reply_text("📦 **Batch:** Multiple messages ke liye channel post ka link use karein.")


# ==================== AUTO-DELETE FUNCTION ====================
async def delete_message_after_delay(message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


if __name__ == "__main__":
    print("🤖 Son Goku Bot with Forward-Link Generator is starting...")
    app.run()
