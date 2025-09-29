#!/usr/bin/env python3
"""
Main entry point for Telegram Bot (Refactored)
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Import configuration and handlers
from config import Config
from handlers.base_handlers import (
    StartCommandHandler, HelpCommandHandler, InfoCommandHandler,
    MenuCommandHandler, StatsCommandHandler, AdminCommandHandler,
    JokeCommandHandler, StatsCallbackHandler,
    AdminCallbackHandler, JokeCallbackHandler, LanguageCommandHandler
)
from handlers.callback_handlers import button_callback
from handlers.error_handlers import error_handler
from handlers.message_handlers import echo
from utils import setup_logging

# Setup logging
setup_logging(Config.LOG_LEVEL, Config.LOG_FORMAT, Config.IS_DOCKER)
logger = logging.getLogger(__name__)

# Create handler instances
start_handler = StartCommandHandler()
help_handler = HelpCommandHandler()
info_handler = InfoCommandHandler()
menu_handler = MenuCommandHandler()
stats_handler = StatsCommandHandler()
admin_handler = AdminCommandHandler()
joke_handler = JokeCommandHandler()
stats_callback_handler = StatsCallbackHandler()
admin_callback_handler = AdminCallbackHandler()
joke_callback_handler = JokeCallbackHandler()
language_handler = LanguageCommandHandler()

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(Config.BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_handler.handle))
    application.add_handler(CommandHandler("help", help_handler.handle))
    application.add_handler(CommandHandler("info", info_handler.handle))
    application.add_handler(CommandHandler("menu", menu_handler.handle))
    application.add_handler(CommandHandler("joke", joke_handler.handle))
    application.add_handler(CommandHandler("stats", stats_handler.handle))
    application.add_handler(CommandHandler("admin", admin_handler.handle))
    application.add_handler(CommandHandler("language", language_handler.handle))
    
    # Register message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Register callback handlers
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
