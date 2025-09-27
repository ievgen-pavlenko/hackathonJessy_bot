"""
Main entry point for Telegram Bot
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Import configuration and handlers
from config import Config
from handlers import (
    start, help_command, info_command, menu_command, joke_command,
    echo, button_callback, error_handler
)
from utils import setup_logging

# Setup logging
setup_logging(Config.LOG_LEVEL, Config.LOG_FORMAT, Config.IS_DOCKER)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(Config.BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("joke", joke_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    logger.info(f"🤖 {Config.BOT_NAME} v{Config.BOT_VERSION} is starting...")
    print(f"🤖 {Config.BOT_NAME} v{Config.BOT_VERSION} is starting...")
    print("Press Ctrl+C to stop the bot")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
