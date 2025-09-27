"""
Command handlers for Telegram Bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import Config
from utils import get_random_joke, track_user_interaction, track_command_usage, is_admin
from stats import stats_manager
from base import UserInfo
from constants import MessageTemplates, KeyboardLayouts, ButtonTexts

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    try:
        # Check if update.message exists
        if not update.message:
            logger.error("Update.message is None in start command")
            return
        
        # Track user interaction
        user = update.message.from_user
        track_user_interaction(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        track_command_usage(user.id, '/start')
            
        user = update.effective_user
        welcome_message = f"""
🤖 Welcome to {Config.BOT_NAME}, {user.first_name}!

I'm here to help you with various tasks. Here are some commands you can use:

/start - Show this welcome message
/help - Get help and available commands
/info - Get information about the bot
/menu - Show interactive menu

Feel free to send me any message and I'll respond!
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Menu", callback_data='menu'), InlineKeyboardButton("ℹ️ Info", callback_data='info')],
            [InlineKeyboardButton("❓ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        if update.message:
            await update.message.reply_text("😅 Sorry, something went wrong. Please try again!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    try:
        # Check if update.message exists
        if not update.message:
            logger.error("Update.message is None in help command")
            return
        
        # Track user interaction
        user = update.message.from_user
        track_user_interaction(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        track_command_usage(user.id, '/help')
            
        help_text = """
🆘 **Help & Commands**

**Basic Commands:**
/start - Start the bot and see welcome message
/help - Show this help message
/info - Get bot information
/menu - Show interactive menu
/joke - Get a random joke
/stats - Show bot statistics
/admin - Admin panel (admin only)

**Features:**
• Interactive buttons and menus
• Random jokes from external API
• Echo messages back to you
• User-friendly interface
• Error handling

**How to use:**
1. Use the buttons below for quick actions
2. Send any text message to get an echo response
3. Use /menu to access the main menu
4. Use /joke to get a random joke

Need more help? Just send me a message!
        """
        
        keyboard = [
            [InlineKeyboardButton("🏠 Main Menu", callback_data='menu'), InlineKeyboardButton("📞 Contact", callback_data='contact')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        if update.message:
            await update.message.reply_text("😅 Sorry, something went wrong. Please try again!")

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send bot information."""
    try:
        # Check if update.message exists
        if not update.message:
            logger.error("Update.message is None in info command")
            return
        
        # Track user interaction
        user = update.message.from_user
        track_user_interaction(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        track_command_usage(user.id, '/info')
            
        info_text = f"""
ℹ️ **Bot Information**

**Bot Name:** {Config.BOT_NAME}
**Version:** {Config.BOT_VERSION}
**Status:** ✅ Online
**Features:** 
• Interactive menus
• Message echo
• Command handling
• User-friendly interface

**Developer:** {Config.BOT_DEVELOPER}
**Created:** 2025

This bot is built with python-telegram-bot library.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(info_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Error in info command: {e}")
        if update.message:
            await update.message.reply_text("😅 Sorry, something went wrong. Please try again!")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the main menu."""
    try:
        # Check if update.message exists
        if not update.message:
            logger.error("Update.message is None in menu command")
            return
        
        # Track user interaction
        user = update.message.from_user
        track_user_interaction(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        track_command_usage(user.id, '/menu')
            
        from handlers.callback_handlers import show_menu
        await show_menu(update, context)
        
    except Exception as e:
        logger.error(f"Error in menu command: {e}")
        if update.message:
            await update.message.reply_text("😅 Sorry, something went wrong. Please try again!")

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random joke to the user."""
    try:
        # Check if update.message exists
        if not update.message:
            logger.error("Update.message is None in joke command")
            return
        
        # Track user interaction
        user = update.message.from_user
        track_user_interaction(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        track_command_usage(user.id, '/joke')
        
        # Send loading message
        loading_message = await update.message.reply_text("🎭 Fetching a joke for you...")
        
        # Get joke based on user input (if any)
        user_input = context.args[0] if context.args else "Розкажи анекдот"
        joke_text = await get_random_joke(user_input)
        
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
        logger.error(f"Error in joke command: {e}")
        error_message = "😅 Sorry, I couldn't fetch a joke right now. Try again later!"
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data='joke'), InlineKeyboardButton("📋 Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Check if update.message exists before trying to reply
        if update.message:
            await update.message.reply_text(
                error_message, 
                reply_markup=reply_markup
            )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show bot statistics."""
    try:
        # Check if update.message exists
        if not update.message:
            logger.error("Update.message is None in stats command")
            return
        
        # Track user interaction
        user = update.message.from_user
        track_user_interaction(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        track_command_usage(user.id, '/stats')
        
        # Get statistics
        stats_text = stats_manager.get_stats_summary()
        
        # Create keyboard
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data='stats'), InlineKeyboardButton("📋 Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            stats_text, 
            reply_markup=reply_markup, 
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        logger.error(f"Error in stats command: {e}")
        if update.message:
            await update.message.reply_text("😅 Sorry, couldn't get statistics right now. Try again later!")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin-only command for user management."""
    try:
        # Check if update.message exists
        if not update.message:
            logger.error("Update.message is None in admin command")
            return
        
        user = update.message.from_user
        
        # Check if user is admin
        if not is_admin(user.id):
            await update.message.reply_text("❌ Access denied. This command is for administrators only.")
            return
        
        # Track user interaction
        track_user_interaction(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        track_command_usage(user.id, '/admin')
        
        # Get users list
        users_text = stats_manager.get_users_list(limit=20)
        
        # Create keyboard
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data='admin'), InlineKeyboardButton("📊 Stats", callback_data='stats')],
            [InlineKeyboardButton("📋 Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            users_text, 
            reply_markup=reply_markup, 
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        logger.error(f"Error in admin command: {e}")
        if update.message:
            await update.message.reply_text("😅 Sorry, couldn't get admin data right now. Try again later!")
        else:
            logger.error("Cannot send error message: update.message is None")
