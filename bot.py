import logging
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from supabase import create_client, Client as SupabaseClient

# Logging setup
logging.basicConfig(level=logging.INFO)

# Aapke Telegram Credentials
API_ID = 38215355
API_HASH = "3f095c170be8c744b8f3d7f9c75ae544"
BOT_TOKEN = "8555113283:AAFTY7YNDz52tNArdoeIMXpQwc8efMXTylA"

# Aapka Supabase URL aur Key
SUPABASE_URL = "https://nveowfitvoligqecxofr.supabase.co"
SUPABASE_KEY = "sb_publishable_fqZzvMNKkcupSdiGMEtebA_J_UK9z9F"

# Supabase Client initialize karein
supabase: SupabaseClient = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pyrogram Client initialize karein
app = Client(
    "son_goku_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Aapka Private Channel / Episode Link
CHANNEL_INVITE_LINK = "https://t.me/+YourPrivateChannelInviteLink"

# DXE Studio Channel Link (Button ke liye)
DXE_CHANNEL_LINK = "https://t.me/dubxempirestudio"

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    args = message.command
    
    # Buttons layout (DXE Studio channel button)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("DXE STUDIO", url=DXE_CHANNEL_LINK)]
    ])
    
    # Aapka DXE Studio ka image URL (Aap chahein toh isko direct image link ya file_id se bhi bhej sakte hain)
    # Note: Agar image local file se bhejni hai ya URL se, Pyrogram seedha URL se photo bhej deta hai.
    # Hum yahan ek public image link ya placeholder use kar rahe hain, aap apna image ka direct link yahan daal sakte hain.
    PHOTO_URL = "https://i.ibb.co/1G598Y8/dxe-studio.jpg" # (Aap ise apne image ke direct URL se replace kar sakte hain)

    # Check karein agar user Mini App ke "Send to Channel Bot" button se aaya hai
    if len(args) > 1 and args[1].startswith("redeem_"):
        code = args[1].split("_")[1]
        
        # Supabase database se check karein ki code exist karta hai aur unused hai
        response = supabase.table("redeem_codes").select("*").eq("code", code).execute()
        
        if not response.data:
            await message.reply_text("❌ **Invalid or non-existent redeem code!**")
            return
            
        code_data = response.data[0]
        
        if code_data.get("is_used"):
            await message.reply_text(
                "❌ **This redeem code has already been used!**\n"
                "Please generate a new code from the mini app."
            )
            return
            
        # Database me code ko used mark kar dein
        supabase.table("redeem_codes").update({"is_used": True, "used_by": user_id}).eq("code", code).execute()
        
        # User ko episode link bhejein
        await message.reply_text(
            f"🔥 **HELLO DEAR {message.from_user.first_name}** 🔥\n\n"
            "🎬 **YE RAHA AAPKA ANIME EPISODE** ⚡\n"
            "ENJOY THE EPISODE 💙",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌸 Watch Anime 🌸", url=CHANNEL_INVITE_LINK)],
                [InlineKeyboardButton("DXE STUDIO", url=DXE_CHANNEL_LINK)]
            ])
        )
        
        # 15 min expiry warning message
        await message.reply_text(
            "⏳ **Warning:** This channel link will expire in 15 minutes! "
            "Make sure to request to join now."
        )
    else:
        # Normal Start message with Photo and DXE Studio Button
        caption = (
            f"👋 **Hello {message.from_user.first_name}!**\n\n"
            "✨ Send your Redeem Code here (or click `/redeem <code>`) "
            "and I will provide your episode channel link!"
        )
        try:
            await message.reply_photo(
                photo=PHOTO_URL,
                caption=caption,
                reply_markup=keyboard
            )
        except Exception:
            # Fallback agar photo URL load hone me koi dikkat ho
            await message.reply_text(caption, reply_markup=keyboard)

@app.on_message(filters.command("redeem"))
async def redeem_handler(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "⚠️ **Please provide your redeem code.**\n"
            "Example: `/redeem U5RSM53J7J`"
        )
        return
        
    code = message.command[1].strip()
    user_id = message.from_user.id
    
    # Supabase se check karein
    response = supabase.table("redeem_codes").select("*").eq("code", code).execute()
    
    if not response.data:
        await message.reply_text("❌ **Invalid or non-existent redeem code.**")
        return
        
    code_data = response.data[0]
    
    if code_data.get("is_used"):
        await message.reply_text("❌ **This redeem code has already been used!**")
        return
        
    # Database me used mark karein
    supabase.table("redeem_codes").update({"is_used": True, "used_by": user_id}).eq("code", code).execute()
    
    await message.reply_text(
        "✅ **Code verified successfully!**\n\n"
        "🎬 **YE RAHA AAPKA ANIME EPISODE**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🌸 Watch Anime 🌸", url=CHANNEL_INVITE_LINK)],
            [InlineKeyboardButton("DXE STUDIO", url=DXE_CHANNEL_LINK)]
        ])
    )
    await message.reply_text("⏳ **Warning:** This channel link will expire in 15 minutes! Make sure to request to join now.")

if __name__ == "__main__":
    print("🤖 Son Goku Bot with Image & DXE Studio is starting...")
    app.run()
