import os
import nest_asyncio
nest_asyncio.apply()
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    msg = await update.message.reply_text("⏳ جاري التحميل...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(file_name, 'rb'))

        os.remove(file_name)

        await msg.delete()

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ:\n{e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("Bot Running...")

app.run_polling()
