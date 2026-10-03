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

# Aapka Bot Username
BOT_USERNAME = "Son_Goku_07bot"


# ==================== /START & SMART DEEP-LINK HANDLER ====================
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    first_name = message.from_user.first_name
    args = message.command
    
    if len(args) > 1:
        payload = args[1]
        try:
            # Check karein agar payload naye format (post_chatid_msgid) me hai
            if payload.startswith("post_"):
                parts = payload.split("_")
                chat_id = int("-" + parts[1])
                msg_id = int(parts[2])
                
                sent_msg = await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=chat_id,
                    message_id=msg_id
                )
                asyncio.create_task(delete_message_after_delay(sent_msg, 900))
                return
            
            else:
                # Agar purana file_id format hai, toh cache media try karein
                try:
                    sent_msg = await client.send_cached_media(
                        chat_id=message.chat.id,
                        file_id=payload
                    )
                    asyncio.create_task(delete_message_after_delay(sent_msg, 900))
                    return
                except Exception:
                    # Agar file_id fail ho toh user ko batayein
                    pass
                
        except Exception as e:
            print(f"Error handling start payload: {e}")
            
        await message.reply_text("❌ Yeh content ab available nahi hai ya link expire ho gaya hai.")
        return

    # Normal /Start Command
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


# ==================== ROBUST LINK GENERATOR ====================
@app.on_message(filters.forwarded & filters.private)
async def forwarded_message_handler(client, message):
    """
    Yeh handler channel ki original post ki chat_id aur message_id nikal kar 
    ek 100% working deep link banata hai.
    """
    proc_msg = await message.reply_text("processing..")
    
    try:
        if message.forward_from_chat:
            chat_id = message.forward_from_chat.id
            msg_id = message.forward_from_message_id
            payload = f"post_{abs(chat_id)}_{msg_id}"
        else:
            # Agar direct file hai toh file_id use karenge
            if message.document:
                payload = message.document.file_id
            elif message.video:
                payload = message.video.file_id
            elif message.audio:
                payload = message.audio.file_id
            elif message.photo:
                payload = message.photo.file_id
            else:
                payload = str(message.id)
            
        generated_link = f"https://t.me/{BOT_USERNAME}?start={payload}"
        
        await proc_msg.delete()
        
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 SHARE URL", url=f"https://t.me/share/url?url={generated_link}")]
        ])
        
        await message.reply_text(
            f"Here is your link:\n\n`{generated_link}`",
            reply_markup=button,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        await proc_msg.edit_text(f"❌ Error generating link: {e}")


# ==================== /GENLINK COMMAND HANDLER ====================
@app.on_message(filters.command("genlink") & filters.private)
async def genlink_cmd(client, message):
    await message.reply_text("Send A Message For To Get Your Shareable Link")


# ==================== AUTO-DELETE FUNCTION ====================
async def delete_message_after_delay(message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


if __name__ == "__main__":
    print("🤖 Son Goku Robust Bot is running...")
    app.run()
