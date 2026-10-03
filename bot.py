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
CHANNEL_1_NAME = "ZK Dubbing Studio"
CHANNEL_1_LINK = "https://t.me/ZK_Dubbing_Studio"

CHANNEL_2_NAME = "Join Channel 2"
CHANNEL_2_LINK = "https://t.me/+VzwHuVRrPYljOGJl"

# Aapka Bot Username
BOT_USERNAME = "Zk_dubbing_studio_bot"


# ==================== /START & DEEP-LINK HANDLER ====================
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    first_name = message.from_user.first_name
    args = message.command
    
    # Check karein agar user deep link (jaise file/post id) se aaya hai
    if len(args) > 1:
        payload = args[1]
        try:
            # Agar payload post format me hai (post_chatid_msgid)
            if payload.startswith("post_"):
                parts = payload.split("_")
                chat_id = int("-" + parts[1])
                msg_id = int(parts[2])
                
                sent_msg = await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=chat_id,
                    message_id=msg_id
                )
                # 15 Minutes Auto-Delete Timer (900 seconds)
                asyncio.create_task(delete_message_after_delay(sent_msg, 900))
                return
            
            else:
                # Agar Pyrogram ki standard file file_id hai
                sent_msg = await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=message.chat.id, # Fallback
                    message_id=int(payload) if payload.isdigit() else message.id
                )
                asyncio.create_task(delete_message_after_delay(sent_msg, 900))
                return
                
        except Exception as e:
            print(f"Error handling start payload: {e}")
            # Fallback: Agar copy_message fail ho toh file ID samajh kar bhejne ki koshish karein
            try:
                sent_msg = await client.send_cached_media(
                    chat_id=message.chat.id,
                    file_id=payload
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
        "✨ ZK Dubbing Studio bot me aapka swagat hai. Kripya neeche diye gaye channels ko join karein!"
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


# ==================== FORWARDED MESSAGE LINK GENERATOR ====================
@app.on_message(filters.forwarded & filters.private)
async def forwarded_message_handler(client, message):
    """
    Jaise hi aap koi post forward karenge, pehle 'processing..' dikhayega,
    phir exact link aur Share URL button generate karke dega.
    """
    # Step 1: Send processing message
    proc_msg = await message.reply_text("processing..")
    
    try:
        # Check karein ki message kisi channel se forward hua hai ya direct file hai
        if message.forward_from_chat:
            chat_id = message.forward_from_chat.id
            msg_id = message.forward_from_message_id
            payload = f"post_{abs(chat_id)}_{msg_id}"
        else:
            # Agar direct media file hai toh uska message id use kar lenge
            payload = str(message.id)
            
        generated_link = f"https://t.me/{BOT_USERNAME}?start={payload}"
        
        # Step 2: Delete processing message
        await proc_msg.delete()
        
        # Step 3: Send final response with Share URL button
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
    print("🤖 ZK Dubbing Studio Bot is running...")
    app.run()
