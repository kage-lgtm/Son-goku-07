import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Logging setup karein
logging.basicConfig(level=logging.INFO)

# Aapke Real API Credentials aur Bot Token
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

# Temporary memory store (Production ke liye yahan Supabase Database connect karein)
USED_CODES = set()

# Apna Private Channel / Episode Link yahan daalein
CHANNEL_INVITE_LINK = "https://t.me/+YourPrivateChannelInviteLink"

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    args = message.command
    
    # Check karein agar user Mini App ke "Send to Channel Bot" button se aaya hai
    if len(args) > 1 and args[1].startswith("redeem_"):
        code = args[1].split("_")[1]
        
        # Check karein code pehle use toh nahi ho chuka
        if code in USED_CODES:
            await message.reply_text(
                "❌ **This redeem code has already been used or expired!**\n"
                "Please generate a new code from the mini app."
            )
            return
            
        # Code ko mark kar de taaki dobara use na ho sake
        USED_CODES.add(code)
        
        # User ko episode link bhejein
        await message.reply_text(
            f"🔥 **HELLO DEAR {message.from_user.first_name}** 🔥\n\n"
            "🎬 **YE RAHA AAPKA ANIME EPISODE** ⚡\n"
            "ENJOY THE EPISODE 💙",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌸 Watch Anime 🌸", url=CHANNEL_INVITE_LINK)]
            ])
        )
        
        # 15 min expiry warning message
        await message.reply_text(
            "⏳ **Warning:** This channel link will expire in 15 minutes! "
            "Make sure to request to join now."
        )
    else:
        # Normal Start message
        await message.reply_text(
            f"👋 **Hello {message.from_user.first_name}!**\n\n"
            "✨ Send your Redeem Code here (or use `/redeem <your_code>`) "
            "to get your episode channel link!"
        )

@app.on_message(filters.command("redeem"))
async def redeem_handler(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "⚠️ **Please provide your redeem code.**\n"
            "Example: `/redeem U5RSM53J7J`"
        )
        return
        
    code = message.command[1].strip()
    
    # Check karein code valid hai ya pehle use ho chuka hai
    if code in USED_CODES:
        await message.reply_text("❌ **Invalid, expired, or already used redeem code.**")
        return
        
    # Code ko use mark kar dein
    USED_CODES.add(code)
    
    await message.reply_text(
        "✅ **Code verified successfully!**\n\n"
        "🎬 **YE RAHA AAPKA ANIME EPISODE**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🌸 Watch Anime 🌸", url=CHANNEL_INVITE_LINK)]
        ])
    )
    await message.reply_text("⏳ **Warning:** This channel link will expire in 15 minutes! Make sure to request to join now.")

if __name__ == "__main__":
    print("🤖 Son Goku Bot is starting...")
    app.run()
