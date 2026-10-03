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

# Bot ka username
BOT_USERNAME = "Son_Goku_07bot"


# ==================== /START & DEEP-LINK HANDLER ====================
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    first_name = message.from_user.first_name
    args = message.command
    
    # Check karein agar user kisi specific post/episode link se aaya hai
    if len(args) > 1 and args[1].startswith("post_"):
        try:
            parts = args[1].split("_")
            chat_id = int("-" + parts[1])
            msg_id = int(parts[2])
            
            # Original post ko channel se copy karke user ko bhejein
            sent_msg = await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=chat_id,
                message_id=msg_id
            )
            
            # **15 Minutes Auto-Delete Timer (900 seconds)**
            asyncio.create_task(delete_message_after_delay(sent_msg, 900))
            return
            
        except Exception as e:
            print(f"Error copying post: {e}")
            await message.reply_text("❌ Yeh content ab available nahi hai ya link expired ho gaya hai.")
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


# ==================== READY-MADE POST & LINK GENERATOR ====================
@app.on_message(filters.forwarded & filters.private)
async def forwarded_message_handler(client, message):
    """
    Jab aap channel se koi post bot par forward karenge, 
    bot uska deep link banakar ek ready-made post button ke sath wapas dega.
    """
    try:
        if message.forward_from_chat:
            chat_id = message.forward_from_chat.id
            msg_id = message.forward_from_message_id
            
            # Unique payload
            payload = f"post_{abs(chat_id)}_{msg_id}"
            generated_link = f"https://t.me/{BOT_USERNAME}?start={payload}"
            
            # Button jo aapke channel post par lagega
            button = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔥 Watch Anime 🔥", url=generated_link)]
            ])
            
            # Bot me preview bhejenge jisme button laga hoga
            if message.photo:
                await message.reply_photo(
                    photo=message.photo.file_id,
                    caption=message.caption or "🎬 **New Episode Available!**",
                    reply_markup=button
                )
            elif message.video:
                await message.reply_video(
                    video=message.video.file_id,
                    caption=message.caption or "🎬 **New Episode Available!**",
                    reply_markup=button
                )
            else:
                await message.reply_text(
                    text=message.text or "🎬 **New Episode Available!**",
                    reply_markup=button
                )
                
            # Saath me raw link bhi bhej denge copy karne ke liye
            await message.reply_text(
                f"🔗 **Deep Link:**\n`{generated_link}`",
                disable_web_page_preview=True
            )
            
        else:
            await message.reply_text("⚠️ Kripya kisi Public/Private channel ki post ko directly forward karein.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


# ==================== OTHER COMMANDS ====================
@app.on_message(filters.command("genlink") & filters.private)
async def genlink_cmd(client, message):
    await message.reply_text("🔗 **GenLink:** Aap apne channel se kisi bhi episode/poster message ko seedha is bot par **forward** karein!")


# ==================== AUTO-DELETE FUNCTION ====================
async def delete_message_after_delay(message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


if __name__ == "__main__":
    print("🤖 Son Goku Bot is running...")
    app.run()
