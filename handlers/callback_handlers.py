"""
Callback handlers for Telegram Bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import Config
from utils import get_random_joke

logger = logging.getLogger(__name__)

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the main menu."""
    menu_text = """
🎛️ **Main Menu**

Choose an option below:
    """
    
    keyboard = [
        [InlineKeyboardButton("📊 Statistics", callback_data='stats'), InlineKeyboardButton("⚙️ Settings", callback_data='settings')],
        [InlineKeyboardButton("🎭 Joke", callback_data='joke'), InlineKeyboardButton("ℹ️ About", callback_data='info')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.callback_query.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'menu':
        await show_menu(update, context)
    elif query.data == 'info':
        await handle_info_callback(query)
    elif query.data == 'help':
        await handle_help_callback(query)
    elif query.data == 'stats':
        await handle_stats_callback(query)
    elif query.data == 'settings':
        await handle_settings_callback(query)
    elif query.data == 'contact':
        await handle_contact_callback(query)
    elif query.data == 'echo_again':
        await query.edit_message_text("🔄 Send me any message and I'll echo it back to you!")
    elif query.data == 'joke':
        await handle_joke_callback(query)

async def handle_info_callback(query):
    """Handle info button callback."""
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
**Created:** 2024
    """
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(info_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_help_callback(query):
    """Handle help button callback."""
    help_text = """
🆘 **Help & Commands**

**Basic Commands:**
/start - Start the bot and see welcome message
/help - Show this help message
/info - Get bot information
/menu - Show interactive menu

**Features:**
• Interactive buttons and menus
• Echo messages back to you
• User-friendly interface
• Error handling
    """
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_stats_callback(query):
    """Handle stats button callback."""
    stats_text = """
📊 **Statistics**

**Bot Stats:**
• Total Users: 1
• Messages Processed: 1
• Uptime: Active
• Commands Used: 1

**Your Stats:**
• Messages Sent: 1
• Commands Used: 1
    """
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(stats_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_settings_callback(query):
    """Handle settings button callback."""
    settings_text = """
⚙️ **Settings**

**Available Settings:**
• Language: English
• Notifications: Enabled
• Privacy: Standard

**Coming Soon:**
• Custom themes
• Advanced preferences
• User profiles
    """
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(settings_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def handle_contact_callback(query):
    """Handle contact button callback."""
    contact_text = f"""
📞 **Contact**

**Get in Touch:**
• Developer: {Config.BOT_DEVELOPER}
• Email: {Config.BOT_EMAIL}
• GitHub: {Config.BOT_GITHUB}
• Support: Available 24/7

**Report Issues:**
• Use /help for assistance
• Send feedback via messages
• Report bugs directly
    """
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(contact_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_joke_callback(query):
    """Handle joke button callback - ask user for input."""
    try:
        # Ask user for joke input
        joke_prompt = """
🎭 **Tell me what kind of joke you want!**

Send me a message with your request, for example:
• "Tell me a programming joke"
• "I want a dad joke"
• "Make me laugh about cats"
• Or just send any text!

I'll create a personalized joke for you! 😄
        """
        
        keyboard = [
            [InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            joke_prompt, 
            reply_markup=reply_markup, 
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in joke callback: {e}")
        error_text = "😅 Sorry, something went wrong. Please try again!"
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data='joke'), InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            error_text, 
            reply_markup=reply_markup
        )
