import os 
import threading
import dotenv
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Import the pipeline function from your driver file
from engine import run_

dotenv.load_dotenv()

# --- Flask Server Setup for Render ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is active and polling!", 200

def run_health_server():
    # Render automatically injects a PORT environment variable
    port = int(os.getenv("PORT", 10000))
    # host '0.0.0.0' allows external network pings to reach it
    app.run(host="0.0.0.0", port=port)
# -------------------------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Grab the message text from Telegram
    user_text = update.message.text
    
    # Optional: Send a typing indicator so the user knows the bot is working
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # 2. Pass the message into your driver pipeline and get the final result
    bot_response = run_(user_text)
    
    # 3. Send that final response back to the Telegram user
    await update.message.reply_text(bot_response)


def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN missing!")
        return

    # Start the Flask health check server in a daemon thread 
    # so it does not block python-telegram-bot's own event loop
    print("Starting Render health check server...")
    threading.Thread(target=run_health_server, daemon=True).start()

    # Build and start the Telegram bot application
    application = Application.builder().token(TOKEN).build()
    
    # Listen for any text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Telegram Bot is running and listening for messages...")
    application.run_polling()

if __name__ == "__main__":
    main()