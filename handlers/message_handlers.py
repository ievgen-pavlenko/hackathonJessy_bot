"""
Message handlers for Telegram Bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils import get_random_joke, track_user_interaction, track_command_usage
from base import UserInfo
from constants import TranslationKeys
from user_states import state_manager, UserState
from stats import stats_manager
from localization import translate

logger = logging.getLogger(__name__)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages with echo response or joke creation."""
    try:
        # Check if update.message exists
        if not update.message:
            logger.error("Update.message is None in echo handler")
            return
        
        # Track user interaction
        user = update.message.from_user
        track_user_interaction(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        track_command_usage(user.id, 'message')
            
        user_message = update.message.text
        
        # Check if user is waiting for joke input
        if state_manager.is_waiting_for_joke_input(user.id):
            # User is waiting for joke input - create joke
            await handle_joke_creation(update, user_message)
            # Clear user state after processing
            state_manager.clear_user_state(user.id)
        else:
            # Normal echo behavior
            await handle_normal_echo(update, user_message)
        
    except Exception as e:
        logger.error(f"Error in echo handler: {e}")
        error_message = "😅 Sorry, something went wrong. Please try again!"
        keyboard = [
            [InlineKeyboardButton("📋 Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(
                error_message, 
                reply_markup=reply_markup
            )
        else:
            logger.error("Cannot send error message: update.message is None")

async def handle_normal_echo(update: Update, user_message: str) -> None:
    """Handle normal echo response"""
    user_id = update.message.from_user.id
    lang = stats_manager.get_user_language(user_id)

    # Echo the message back to the user
    echo_response = translate(TranslationKeys.YOU_SAID, lang).format(user_message=user_message)
    
    # Add helpful message
    help_text = translate(TranslationKeys.JOKE_BOT_HELP, lang)
    
    # Create keyboard with options
    keyboard = [
        [InlineKeyboardButton(translate(TranslationKeys.CREATE_JOKE, lang), callback_data='joke'), InlineKeyboardButton(translate(TranslationKeys.MENU, lang), callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{echo_response}\n\n{help_text}",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_joke_creation(update: Update, user_message: str) -> None:
    """Handle joke creation from user input"""
    user_id = update.message.from_user.id
    lang = stats_manager.get_user_language(user_id)

    # Send loading message
    loading_message = await update.message.reply_text(translate(TranslationKeys.CREATING_JOKE, lang))
    
    try:
        # Get joke based on user input
        joke_text = await get_random_joke(user_message, lang)
        
        # Update message with joke
        keyboard = [
            [InlineKeyboardButton(translate(TranslationKeys.ANOTHER_JOKE, lang), callback_data='joke'), InlineKeyboardButton(translate(TranslationKeys.MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await loading_message.edit_text(
            joke_text, 
            reply_markup=reply_markup, 
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error creating joke: {e}")
        error_message = "😅 Sorry, I couldn't create a joke right now. Try again later!"
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data='joke'), InlineKeyboardButton("📋 Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await loading_message.edit_text(
            error_message, 
            reply_markup=reply_markup
        )
