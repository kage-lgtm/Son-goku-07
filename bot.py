import asyncio
import logging
import io
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant

# Logging setup
logging.basicConfig(level=logging.INFO)

# Telegram Credentials
API_ID = 38215355
API_HASH = "3f095c170be8c744b8f3d7f9c75ae544"
BOT_TOKEN = "8555113283:AAFTY7YNDz52tNArdoeIMXpQwc8efMXTylA"

app = Client(
    "son_goku_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Aapka Welcome Image URL
WELCOME_PHOTO_URL = "https://pictureurl.com/api/storage/file?key=u%2Fanon%2F4b5aaa02-9ea3-4c7e-b649-a9c9cea4e03d-1000225779.jpg"

# Channels Details
CHANNEL_1_NAME = "DXE Studio"
CHANNEL_1_LINK = "https://t.me/dubxempirestudio"
CHANNEL_1_ID = "@dubxempirestudio"

CHANNEL_2_NAME = "Join Channel 2"
CHANNEL_2_LINK = "https://t.me/+VzwHuVRrPYljOGJl"
CHANNEL_2_ID = -1004392141410  # Numeric Channel ID

BOT_USERNAME = "Son_Goku_07bot"
DELETE_DELAY = 600  # 10 minutes (600 seconds)


# Helper Function: Download image securely with browser headers
def get_image_stream(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return io.BytesIO(response.content)
        else:
            logging.error(f"Image download failed with status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Image download error: {e}")
    return None


# Helper Function: Check if user joined required channels safely
async def check_user_joined(client, user_id):
    if CHANNEL_1_ID:
        try:
            await client.get_chat_member(CHANNEL_1_ID, user_id)
        except UserNotParticipant:
            return False
        except Exception as e:
            logging.error(f"Channel 1 Check Error: {e}")

    if CHANNEL_2_ID:
        try:
            await client.get_chat_member(CHANNEL_2_ID, user_id)
        except UserNotParticipant:
            return False
        except Exception as e:
            logging.error(f"Channel 2 Check Error: {e}")

    return True


# ==================== /START COMMAND HANDLER ====================
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    args = message.command

    is_joined = await check_user_joined(client, user_id)

    # 1. DEEP-LINK PROCESSING (Agar user file link se aaya hai)
    if len(args) > 1 and is_joined:
        payload = args[1]
        try:
            if payload.startswith("post_"):
                parts = payload.split("_")
                chat_id = int("-100" + parts[1])
                msg_id = int(parts[2])
                
                try:
                    orig_msg = await client.get_messages(chat_id, msg_id)
                except Exception:
                    chat_id = int("-" + parts[1])
                    orig_msg = await client.get_messages(chat_id, msg_id)
                
                if orig_msg:
                    sent_msg = await orig_msg.copy(chat_id=message.chat.id, protect_content=True)
                    if sent_msg:
                        asyncio.create_task(delete_message_after_delay(sent_msg, DELETE_DELAY))
                    return
        except Exception as e:
            logging.error(f"Error handling start payload: {e}")
            sent_err = await message.reply_text("❌ Yeh content ab available nahi hai ya link expire ho gaya hai.", protect_content=True)
            asyncio.create_task(delete_message_after_delay(sent_err, DELETE_DELAY))
            return

    # Image fetch karein
    photo_file = get_image_stream(WELCOME_PHOTO_URL)

    # 2. AGAR USER JOINED NAHI HAI ( Image Upar, Text Niche, Buttons Sabse Niche )
    if not is_joined:
        caption = (
            f"👋 **Hello {first_name}!**\n\n"
            "✨ Bot ka istemaal karne ke liye kripya neeche diye gaye dono channels ko join karein!"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(CHANNEL_1_NAME, url=CHANNEL_1_LINK)],
            [InlineKeyboardButton(CHANNEL_2_NAME, url=CHANNEL_2_LINK)],
            [InlineKeyboardButton("✅ I HAVE JOINED", callback_data="check_joined")]
        ])
        
        try:
            if photo_file:
                sent_msg = await message.reply_photo(
                    photo=photo_file,
                    caption=caption,
                    reply_markup=keyboard,
                    protect_content=True
                )
            else:
                sent_msg = await message.reply_text(
                    text=caption,
                    reply_markup=keyboard,
                    protect_content=True
                )
        except Exception as e:
            logging.error(f"Send photo error: {e}")
            sent_msg = await message.reply_text(
                text=caption,
                reply_markup=keyboard,
                protect_content=True
            )
            
        asyncio.create_task(delete_message_after_delay(sent_msg, DELETE_DELAY))
        return

    # 3. AGAR USER JOINED HAI ( Image Upar, Welcome Message Niche, Options uske niche )
    caption = (
        f"👋 **Welcome Back {first_name}!**\n\n"
        "✨ Aapne channels join kar liye hain. Neeche diye gaye options ka use karein:"
    )
    main_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about_btn"),
            InlineKeyboardButton("❓ Help", callback_data="help_btn")
        ]
    ])
    
    try:
        if photo_file:
            sent_msg = await message.reply_photo(
                photo=photo_file,
                caption=caption,
                reply_markup=main_keyboard,
                protect_content=True
            )
        else:
            sent_msg = await message.reply_text(
                text=caption,
                reply_markup=main_keyboard,
                protect_content=True
            )
    except Exception as e:
        logging.error(f"Send photo error: {e}")
        sent_msg = await message.reply_text(
            text=caption,
            reply_markup=main_keyboard,
            protect_content=True
        )
        
    asyncio.create_task(delete_message_after_delay(sent_msg, DELETE_DELAY))


# ==================== CALLBACK BUTTONS HANDLER ====================
@app.on_callback_query()
async def callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "check_joined":
        is_joined = await check_user_joined(client, user_id)
        if is_joined:
            await callback_query.answer("✅ Subscriptions Verified!", show_alert=True)
            main_keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("ℹ️ About", callback_data="about_btn"),
                    InlineKeyboardButton("❓ Help", callback_data="help_btn")
                ]
            ])
            try:
                await callback_query.message.edit_caption(
                    caption=f"👋 **Welcome {callback_query.from_user.first_name}!**\n\nAapne sabhi channels join kar liye hain.",
                    reply_markup=main_keyboard
                )
            except Exception:
                await callback_query.message.edit_text(
                    text=f"👋 **Welcome {callback_query.from_user.first_name}!**\n\nAapne sabhi channels join kar liye hain.",
                    reply_markup=main_keyboard
                )
        else:
            await callback_query.answer("❌ Aapne abhi tak sabhi channels join nahi kiye hain!", show_alert=True)

    elif data == "about_btn":
        about_text = (
            "✨ **ᴀʙᴏᴜᴛ ᴍᴇ**\n\n"
            "✰ **ᴍʏ ɴᴀᴍᴇ:** @Son_Goku_07bot\n"
            "✰ **ᴅᴇᴠᴇʟᴏᴘᴇʀ:** @kage_x_edit\n"
            "✰ **ᴍʏ ᴏᴡɴᴇʀ:** @Rishu_dubs\n"
            "✰ **ᴜᴘᴅᴀᴛᴇs:** [kage bots](https://t.me/zyphorkagex_chat)\n"
            "✰ **sᴜᴘᴘᴏʀᴛ:** @zyphorkagex"
        )
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ])
        try:
            await callback_query.message.edit_caption(caption=about_text, reply_markup=back_keyboard)
        except Exception:
            await callback_query.message.edit_text(text=about_text, reply_markup=back_keyboard)

    elif data == "help_btn":
        help_text = (
            "❓ **ʜᴇʟᴘ & ᴜsᴀɢᴇ**\n\n"
            "1. Kisi bhi post ka shareable link banane ke liye post ko yahan forward karein.\n"
            "2. Bot aapko ek unique link dega jisse aap share kar sakte hain.\n"
            "3. Sabhi messages 10 minutes me auto-delete ho jayenge."
        )
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ])
        try:
            await callback_query.message.edit_caption(caption=help_text, reply_markup=back_keyboard)
        except Exception:
            await callback_query.message.edit_text(text=help_text, reply_markup=back_keyboard)

    elif data == "back_to_main":
        main_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ℹ️ About", callback_data="about_btn"),
                InlineKeyboardButton("❓ Help", callback_data="help_btn")
            ]
        ])
        try:
            await callback_query.message.edit_caption(
                caption=f"👋 **Welcome {callback_query.from_user.first_name}!**\n\nNeeche diye gaye options select karein:",
                reply_markup=main_keyboard
            )
        except Exception:
            await callback_query.message.edit_text(
                text=f"👋 **Welcome {callback_query.from_user.first_name}!**\n\nNeeche diye gaye options select karein:",
                reply_markup=main_keyboard
            )


# ==================== FORWARDED POST HANDLER ====================
@app.on_message(filters.forwarded & filters.private)
async def forwarded_message_handler(client, message):
    if not await check_user_joined(client, message.from_user.id):
        sent_err = await message.reply_text("❌ Pehle /start dabakar channels join karein!", protect_content=True)
        asyncio.create_task(delete_message_after_delay(sent_err, DELETE_DELAY))
        return

    proc_msg = await message.reply_text("processing..", protect_content=True)
    
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
            disable_web_page_preview=True,
            protect_content=True
        )
        asyncio.create_task(delete_message_after_delay(sent_msg, DELETE_DELAY))
        
    except Exception as e:
        sent_err = await proc_msg.edit_text(f"❌ Error generating link: {e}")
        asyncio.create_task(delete_message_after_delay(sent_err, DELETE_DELAY))


# ==================== /GENLINK COMMAND HANDLER ====================
@app.on_message(filters.command("genlink") & filters.private)
async def genlink_cmd(client, message):
    sent_msg = await message.reply_text("Send A Message To Get Your Shareable Link", protect_content=True)
    asyncio.create_task(delete_message_after_delay(sent_msg, DELETE_DELAY))


# ==================== GENERAL MESSAGE HANDLER ====================
@app.on_message(filters.private & ~filters.command(["start", "genlink"]) & ~filters.forwarded)
async def general_message_handler(client, message):
    sent_msg = await message.reply_text("⚠️ Yeh bot sirf files/links ke liye hai. Yeh message 10 minutes me delete ho jayega.", protect_content=True)
    asyncio.create_task(delete_message_after_delay(sent_msg, DELETE_DELAY))


# ==================== AUTO-DELETE FUNCTION ====================
async def delete_message_after_delay(message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


if __name__ == "__main__":
    print("🤖 Son Goku Bot running successfully...")
    app.run()
