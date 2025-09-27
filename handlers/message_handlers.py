"""
Message handlers for Telegram Bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils import get_random_joke, track_user_interaction, track_command_usage
from base import UserInfo
from constants import MessageTemplates, KeyboardLayouts, ButtonTexts
from user_states import state_manager, UserState

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
    # Echo the message back to the user
    echo_response = f"📝 You said: {user_message}"
    
    # Add helpful message
    help_text = """
🤖 I'm a joke bot! Here's what I can do:

• Send me any text and I'll create a personalized joke
• Use /joke to get a random joke
• Use /menu to see all available commands
• Use /help for more information

Try sending me something like "Tell me a programming joke" or "I want a dad joke"!
    """
    
    # Create keyboard with options
    keyboard = [
        [InlineKeyboardButton("🎭 Create Joke", callback_data='joke'), InlineKeyboardButton("📋 Menu", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{echo_response}\n\n{help_text}",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_joke_creation(update: Update, user_message: str) -> None:
    """Handle joke creation from user input"""
    # Send loading message
    loading_message = await update.message.reply_text("🎭 Creating a joke for you...")
    
    try:
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
