"""
Message handlers for Telegram Bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils import get_random_joke

logger = logging.getLogger(__name__)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages as joke requests."""
    try:
        # Check if update.message exists
        if not update.message:
            logger.error("Update.message is None in echo handler")
            return
            
        user_message = update.message.text
        
        # Send loading message
        loading_message = await update.message.reply_text("🎭 Creating a joke for you...")
        
        # Get joke based on user input
        joke_text = await get_random_joke(user_message)
        
        # Update message with joke
        keyboard = [
            [InlineKeyboardButton("🎭 Another Joke", callback_data='joke'), InlineKeyboardButton("📋 Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await loading_message.edit_text(
            joke_text, 
            reply_markup=reply_markup, 
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in echo handler: {e}")
        error_message = "😅 Sorry, I couldn't create a joke right now. Try again later!"
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data='joke'), InlineKeyboardButton("📋 Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(
                error_message, 
                reply_markup=reply_markup
            )
        else:
            logger.error("Cannot send error message: update.message is None")
