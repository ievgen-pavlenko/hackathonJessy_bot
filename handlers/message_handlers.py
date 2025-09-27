"""
Message handlers for Telegram Bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user_message = update.message.text
    response = f"🔄 You said: {user_message}\n\nI'm echoing your message back to you!"
    
    keyboard = [
        [InlineKeyboardButton("📋 Menu", callback_data='menu')],
        [InlineKeyboardButton("🔄 Echo Again", callback_data='echo_again')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(response, reply_markup=reply_markup)
