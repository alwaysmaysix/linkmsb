from pyrogram import Client
from pyrogram import filters

from decouple import config
import logging
import session.session_gen
import handlers.cyberdrop
import handlers.bunkr
import handlers.start
import handlers.help
import handlers.streamdl
import handlers.streamul
import handlers.ping

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get environment variables
api_id = config("API_ID")  # API ID from Telegram
api_hash = config("API_HASH")  # API hash from Telegram
bot_token = config("BOT_TOKEN")  # Bot token from @BotFather
log_chat_id = config("LOG_CHAT_ID", default=None)  # Optional: chat ID to log startup message

# Initialize the Pyrogram client session
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Define bot's functionality
def setup_handlers():
    @app.on_message(filters.command("start"))
    def welcome(client, message):
        message.reply_text("Welcome to the bot! Type /help for more information.")

    @app.on_message(filters.command("help"))
    def send_help(client, message):
        message.reply_text("Here are the available commands:\n/start - Welcome message\n/help - Show this help\n/ping - Check bot status")

    @app.on_message(filters.command("ping"))
    def send_ping(client, message):
        message.reply_text("Pong!")

    @app.on_message(filters.command("cyberdrop"))
    def send_cybermedia(client, message):
        # Execute functionality for cyberdrop command
        message.reply_text("Cyberdrop media handler called!")

    @app.on_message(filters.command("bunkr"))
    def send_bunkrmedia(client, message):
        # Execute functionality for bunkr command
        message.reply_text("Bunkr media handler called!")

    @app.on_message(filters.command("streamdl"))
    def send_streamtape(client, message):
        if config("API_USERNAME") != "None" and config("API_PASSWORD") != "None":
            message.reply_text("Streamtape download handler called!")
        else:
            message.reply_text("Streamtape credentials not found.")

    @app.on_message(filters.video)
    def upload_streamtape(client, message):
        if config("API_USERNAME") != "None" and config("API_PASSWORD") != "None":
            message.reply_text("Streamtape upload handler called!")
        else:
            message.reply_text("Streamtape credentials not found.")

# Log the bot startup
@app.on_message(filters.command("start"))
def send_startup_log(client, message):
    if log_chat_id:
        app.send_message(int(log_chat_id), "Bot is running...")


if __name__ == "__main__":
    # Setup the bot's handlers
    setup_handlers()

    # Start the bot
    app.run()
