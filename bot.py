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


# ==================== /START & BUTTON-FIXED DEEP-LINK HANDLER ====================
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    first_name = message.from_user.first_name
    args = message.command
    
    if len(args) > 1:
        payload = args[1]
        try:
            # Agar payload post format me hai (post_chatid_msgid)
            if payload.startswith("post_"):
                parts = payload.split("_")
                chat_id = int("-100" + parts[1])
                msg_id = int(parts[2])
                
                try:
                    # Channel se original message fetch karein (buttons ke sath)
                    orig_msg = await client.get_messages(chat_id, msg_id)
                except Exception:
                    chat_id = int("-" + parts[1])
                    orig_msg = await client.get_messages(chat_id, msg_id)
                
                if orig_msg:
                    sent_msg = None
                    # Check karein ki message me kya hai aur waise hi send karein
                    if orig_msg.photo:
                        sent_msg = await orig_msg.copy(chat_id=message.chat.id)
                    elif orig_msg.video:
                        sent_msg = await orig_msg.copy(chat_id=message.chat.id)
                    elif orig_msg.document:
                        sent_msg = await orig_msg.copy(chat_id=message.chat.id)
                    else:
                        sent_msg = await orig_msg.copy(chat_id=message.chat.id)
                    
                    # 15 Minutes Auto-Delete Timer (900 seconds)
                    if sent_msg:
                        asyncio.create_task(delete_message_after_delay(sent_msg, 900))
                    return
                
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
        sent_msg = await message.reply_photo(
            photo=WELCOME_PHOTO_URL,
            caption=caption,
            reply_markup=welcome_keyboard
        )
        # Welcome message ko bhi 15 min me delete karne ke liye
        asyncio.create_task(delete_message_after_delay(sent_msg, 900))
    except Exception as e:
        print(f"Photo error: {e}")
        sent_msg = await message.reply_text(caption, reply_markup=welcome_keyboard)
        asyncio.create_task(delete_message_after_delay(sent_msg, 900))


# ==================== FORWARDED POST HANDLER ====================
@app.on_message(filters.forwarded & filters.private)
async def forwarded_message_handler(client, message):
    """
    Yeh handler channel ki post ka sahi ID extract karke link banata hai.
    """
    proc_msg = await message.reply_text("processing..")
    
    try:
        if message.forward_from_chat:
            chat_id = message.forward_from_chat.id
            msg_id = message.forward_from_message_id
            
            clean_chat_id = str(abs(chat_id)).replace("100", "", 1) if str(abs(chat_id)).startswith("100") else str(abs(chat_id))
            payload = f"post_{clean_chat_id}_{msg_id}"
        else:
            payload = f"post_{abs(message.chat.id)}_{message.id}"
            
        generated_link = f"https://t.me/{BOT_USERNAME}?start={payload}"
        
        await proc_msg.delete()
        
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 SHARE URL", url=f"https://t.me/share/url?url={generated_link}")]
        ])
        
        sent_msg = await message.reply_text(
            f"Here is your link:\n\n`{generated_link}`",
            reply_markup=button,
            disable_web_page_preview=True
        )
        asyncio.create_task(delete_message_after_delay(sent_msg, 900))
        
    except Exception as e:
        await proc_msg.edit_text(f"❌ Error generating link: {e}")


# ==================== /GENLINK COMMAND HANDLER ====================
@app.on_message(filters.command("genlink") & filters.private)
async def genlink_cmd(client, message):
    sent_msg = await message.reply_text("Send A Message For To Get Your Shareable Link")
    asyncio.create_task(delete_message_after_delay(sent_msg, 900))


# ==================== GENERAL MESSAGE AUTO-DELETE HANDLER ====================
@app.on_message(filters.private & ~filters.command(["start", "genlink"]) & ~filters.forwarded)
async def general_message_handler(client, message):
    """
    Bot par aane wale kisi bhi aam message (jo upar wale handlers me nahi aaye) 
    ko 15 minutes (900 seconds) baad delete kar dega.
    """
    # Agar aap chahein toh user ke bheje hue message ko bhi turant ya baad me delete kar sakte hain:
    # try:
    #     await message.delete()
    # except Exception:
    #     pass
    
    # Agar bot ke reply ko delete karna hai:
    sent_msg = await message.reply_text("⚠️ Yeh bot sirf files/links ke liye hai. Yeh message 15 minutes me delete ho jayega.")
    asyncio.create_task(delete_message_after_delay(sent_msg, 900))


# ==================== AUTO-DELETE FUNCTION ====================
async def delete_message_after_delay(message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


if __name__ == "__main__":
    print("🤖 Son Goku Final Bot is running...")
    app.run()
