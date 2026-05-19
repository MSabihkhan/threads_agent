import os 
import threading
import dotenv
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from engine import run_

dotenv.load_dotenv()

# --- Flask Server Setup for Render ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is active and polling!", 200

def run_health_server():
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
# -------------------------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get text from either message text or photo caption
    user_text = update.message.caption if update.message.photo else update.message.text
    image_path = None
    
    # Check if message contains a photo
    if update.message.photo:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
        
        # Get the highest resolution photo (last item in photo array)
        photo = update.message.photo[-1]
        
        # Download the photo to /tmp directory
        photo_file = await photo.get_file()
        image_path = f"/tmp/{photo.file_id}.jpg"
        await photo_file.download_to_drive(image_path)
        
        print(f"Photo downloaded to: {image_path}")
    else:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Pass both text and image path to your pipeline
    # OpenRouter generates the caption, Zernio attaches the image
    bot_response = run_(user_text, image_path=image_path)
    
    # Clean up the downloaded image after posting
    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
            print(f"Cleaned up temporary file: {image_path}")
        except Exception as e:
            print(f"Failed to clean up {image_path}: {e}")
    
    await update.message.reply_text(bot_response)


def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN missing!")
        return

    print("Starting Render health check server...")
    threading.Thread(target=run_health_server, daemon=True).start()

    application = Application.builder().token(TOKEN).build()
    
    # Listen for both text messages AND photos with captions
    application.add_handler(MessageHandler(
        (filters.TEXT | filters.PHOTO) & ~filters.COMMAND, 
        handle_message
    ))
    
    print("Telegram Bot is running and listening for messages and photos...")
    application.run_polling()

if __name__ == "__main__":
    main()