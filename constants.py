#!/usr/bin/env python3
"""
Constants and configuration values for Telegram Bot
"""
from typing import Dict, List, Optional
from enum import Enum

class LogLevel(Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ParseMode(Enum):
    """Message parse modes"""
    HTML = "HTML"
    MARKDOWN = "Markdown"
    MARKDOWN_V2 = "MarkdownV2"

# Bot configuration constants
class BotConstants:
    """Bot configuration constants"""
    
    # Default values
    DEFAULT_BOT_NAME = "Hackathon Jessy Bot"
    DEFAULT_BOT_VERSION = "1.0.0"
    DEFAULT_BOT_DEVELOPER = "@EvOwl"
    DEFAULT_BOT_EMAIL = "evgen.sova@outlook.com"
    DEFAULT_BOT_GITHUB = "https://github.com/EvOwl/hackathonJessy_bot.git"
    
    # Logging defaults
    DEFAULT_LOG_LEVEL = LogLevel.INFO.value
    DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Statistics defaults
    DEFAULT_STATS_DATA_DIR = "data"
    DEFAULT_USERS_LIMIT = 50
    DEFAULT_RECENT_HOURS = 24
    
    # API defaults
    DEFAULT_API_TIMEOUT = 10
    DEFAULT_USER_AGENT = "Telegram Bot/1.0.0"

# Message templates
class MessageTemplates:
    """Message templates for bot responses"""
    
    # Welcome messages
    WELCOME = """🤖 Welcome to {bot_name}, {user_name}!

I'm your personal assistant bot with the following features:
• 🎭 Personalized jokes based on your input
• 📊 Bot statistics and analytics
• 🎛️ Interactive menu system
• ⚙️ Admin panel for administrators

Use /help to see all available commands!"""
    
    # Help messages
    HELP_HEADER = """🆘 **Help & Commands**

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
• Personalized jokes from external API
• User input processing
• User-friendly interface
• Error handling

**How to use:**
1. Use the buttons below for quick actions
2. Send any text message to get a personalized joke
3. Use /menu to access all features"""
    
    # Info messages
    INFO_TEMPLATE = """ℹ️ **Bot Information**

**Bot Name:** {bot_name}
**Version:** {bot_version}
**Status:** ✅ Online
**Features:** 
• Personalized Jokes API
• User Statistics
• Admin Panel
• Interactive Menus

**Developer:** {developer}
**Created:** 2025"""
    
    # Error messages
    ERROR_GENERIC = "😅 Sorry, something went wrong. Please try again!"
    ERROR_STATS = "😅 Sorry, couldn't get statistics right now. Try again later!"
    ERROR_ADMIN = "😅 Sorry, couldn't get admin data right now. Try again later!"
    ERROR_JOKE = "😅 Sorry, I couldn't fetch a joke right now. Try again later!"
    ERROR_ACCESS_DENIED = "❌ Access denied. This command is for administrators only."
    
    # Loading messages
    LOADING_JOKE = "🎭 Fetching a joke for you..."
    LOADING_CREATING_JOKE = "🎭 Creating a joke for you..."

# Button texts
class ButtonTexts:
    """Button text constants"""
    
    # Main menu
    STATISTICS = "📊 Statistics"
    SETTINGS = "⚙️ Settings"
    JOKE = "🎭 Joke"
    ABOUT = "ℹ️ About"
    HELP = "❓ Help"
    MENU = "📋 Menu"
    
    # Actions
    REFRESH = "🔄 Refresh"
    TRY_AGAIN = "🔄 Try Again"
    ANOTHER_JOKE = "🎭 Another Joke"
    BACK_TO_MENU = "🔙 Back to Menu"
    
    # Admin
    ADMIN_PANEL = "👥 Admin Panel"

# Keyboard layouts
class KeyboardLayouts:
    """Keyboard layout constants"""
    
    @staticmethod
    def get_main_menu():
        """Get main menu keyboard layout"""
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(ButtonTexts.STATISTICS, callback_data='stats'), 
             InlineKeyboardButton(ButtonTexts.SETTINGS, callback_data='settings')],
            [InlineKeyboardButton(ButtonTexts.JOKE, callback_data='joke'), 
             InlineKeyboardButton(ButtonTexts.ABOUT, callback_data='info')],
            [InlineKeyboardButton(ButtonTexts.HELP, callback_data='help')]
        ])
    
    @staticmethod
    def get_stats_keyboard():
        """Get stats keyboard layout"""
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(ButtonTexts.REFRESH, callback_data='stats'), 
             InlineKeyboardButton(ButtonTexts.MENU, callback_data='menu')]
        ])
    
    @staticmethod
    def get_admin_keyboard():
        """Get admin keyboard layout"""
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(ButtonTexts.REFRESH, callback_data='admin'), 
             InlineKeyboardButton(ButtonTexts.STATISTICS, callback_data='stats')],
            [InlineKeyboardButton(ButtonTexts.MENU, callback_data='menu')]
        ])
    
    @staticmethod
    def get_joke_keyboard():
        """Get joke keyboard layout"""
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(ButtonTexts.ANOTHER_JOKE, callback_data='joke'), 
             InlineKeyboardButton(ButtonTexts.MENU, callback_data='menu')]
        ])
    
    @staticmethod
    def get_error_keyboard():
        """Get error keyboard layout"""
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(ButtonTexts.TRY_AGAIN, callback_data='joke'), 
             InlineKeyboardButton(ButtonTexts.MENU, callback_data='menu')]
        ])

# File paths
class FilePaths:
    """File path constants"""
    
    # Data files
    USERS_JSON = "users.json"
    BOT_STATS_JSON = "bot_stats.json"
    
    # Log files
    LOG_FILE = "bot.log"
    
    # Config files
    CONFIG_ENV = "config.env"
    ENV_FILE = ".env"

# API constants
class APIConstants:
    """API related constants"""
    
    # Headers
    DEFAULT_HEADERS = {
        'Content-Type': 'application/json',
        'User-Agent': BotConstants.DEFAULT_USER_AGENT
    }
    
    # Timeouts
    DEFAULT_TIMEOUT = 10
    MAX_TIMEOUT = 30
    
    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1

# Statistics constants
class StatsConstants:
    """Statistics related constants"""
    
    # Time formats
    DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S UTC"
    DATE_FORMAT = "%d.%m %H:%M"
    
    # Duration units
    DURATION_DAYS = "д"
    DURATION_HOURS = "г"
    DURATION_MINUTES = "хв"
    DURATION_SECONDS = "с"
    
    # Stats text templates
    STATS_HEADER = "📊 <b>Статистика бота</b>"
    USERS_HEADER = "👥 <b>Список користувачів:</b>"
    
    # Stats labels
    LAST_RESTART = "🕐 <b>Останній запуск:</b>"
    UPTIME = "⏱️ <b>Час роботи:</b>"
    USERS_TOTAL = "👥 <b>Користувачі:</b>"
    MESSAGES_TOTAL = "📨 <b>Повідомлення:</b>"
    TOP_COMMANDS = "🔥 <b>Топ команд:</b>"
    
    # User info labels
    USER_ID = "ID:"
    LAST_VISIT = "Останній візит:"
    MESSAGES_COUNT = "Повідомлень:"
    NO_DATA = "• Немає даних"
    NO_USERS = "Користувачі не знайдені"
