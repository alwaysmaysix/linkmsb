import nest_asyncio
import asyncio
from pyrogram import Client, filters
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

# Allow nested asyncio loops (useful for environments like notebooks)
nest_asyncio.apply()

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
    async def welcome(client, message):
        await message.reply_text("Welcome to the bot! Type /help for more information.")

    @app.on_message(filters.command("help"))
    async def send_help(client, message):
        await message.reply_text("Here are the available commands:\n/start - Welcome message\n/help - Show this help\n/ping - Check bot status")

    @app.on_message(filters.command("ping"))
    async def send_ping(client, message):
        await message.reply_text("Pong!")

    @app.on_message(filters.command("cyberdrop"))
    async def send_cybermedia(client, message):
        await message.reply_text("Cyberdrop media handler called!")

    @app.on_message(filters.command("bunkr"))
    async def send_bunkrmedia(client, message):
        await message.reply_text("Bunkr media handler called!")

    @app.on_message(filters.command("streamdl"))
    async def send_streamtape(client, message):
        if config("API_USERNAME") != "None" and config("API_PASSWORD") != "None":
            await message.reply_text("Streamtape download handler called!")
        else:
            await message.reply_text("Streamtape credentials not found.")

    @app.on_message(filters.video)
    async def upload_streamtape(client, message):
        if config("API_USERNAME") != "None" and config("API_PASSWORD") != "None":
            await message.reply_text("Streamtape upload handler called!")
        else:
            await message.reply_text("Streamtape credentials not found.")


# Function to run the bot
async def run_bot():
    # Setup the bot's handlers
    setup_handlers()
    
    await app.start()
    logging.info("Bot started.")
    
    try:
        await asyncio.Event().wait()  # Keeps the bot running indefinitely
    finally:
        await app.stop()
        logging.info("Bot stopped.")


# Run the bot in the event loop
if __name__ == "__main__":
    asyncio.run(run_bot())
