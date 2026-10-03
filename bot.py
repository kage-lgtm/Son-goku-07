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


# ==================== /START & FILE-ID HANDLER ====================
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    first_name = message.from_user.first_name
    args = message.command
    
    if len(args) > 1:
        payload = args[1]
        try:
            # Agar payload file unique id hai, toh seedha media bhej dein
            sent_msg = await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=payload
            )
            # 15 Minutes Auto-Delete Timer (900 seconds)
            asyncio.create_task(delete_message_after_delay(sent_msg, 900))
            return
        except Exception as e:
            print(f"Error sending cached media: {e}")
            # Fallback: Agar copy_message try karna ho
            try:
                parts = payload.split("_")
                if len(parts) == 3:
                    chat_id = int("-" + parts[1])
                    msg_id = int(parts[2])
                    sent_msg = await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=chat_id,
                        message_id=msg_id
                    )
                    asyncio.create_task(delete_message_after_delay(sent_msg, 900))
                    return
            except Exception as inner_e:
                print(f"Fallback error: {inner_e}")
                
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


# ==================== FILE LINK GENERATOR ====================
@app.on_message((filters.document | filters.video | filters.audio | filters.photo) & filters.private)
async def file_handler(client, message):
    """
    Jab aap bot par koi bhi file, video ya photo bhejenge,
    yeh uska file_id nikal kar waisa hi lamba link bana dega.
    """
    proc_msg = await message.reply_text("processing..")
    
    try:
        # File ki unique file_id nikalte hain (jaisa doosre studios me hota hai)
        if message.document:
            file_id = message.document.file_id
        elif message.video:
            file_id = message.video.file_id
        elif message.audio:
            file_id = message.audio.file_id
        elif message.photo:
            file_id = message.photo.file_id
        else:
            file_id = None
            
        if file_id:
            generated_link = f"https://t.me/{BOT_USERNAME}?start={file_id}"
            
            await proc_msg.delete()
            
            button = InlineKeyboardMarkup([
                [InlineKeyboardButton("📤 SHARE URL", url=f"https://t.me/share/url?url={generated_link}")]
            ])
            
            await message.reply_text(
                f"Here is your link:\n\n`{generated_link}`",
                reply_markup=button,
                disable_web_page_preview=True
            )
        else:
            await proc_msg.edit_text("⚠️ Kripya koi valid file ya video bhejें.")
            
    except Exception as e:
        await proc_msg.edit_text(f"❌ Error: {e}")


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
    print("🤖 Son Goku File-ID Bot is running...")
    app.run()
