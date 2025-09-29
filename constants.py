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
    DEFAULT_USER_AGENT = "Telegram Bot/1.0.0"
    
    # Logging defaults
    DEFAULT_LOG_LEVEL = LogLevel.INFO.value
    DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Statistics defaults
    DEFAULT_STATS_DATA_DIR = "data"
    DEFAULT_USERS_LIMIT = 20
    DEFAULT_LANG = "uk"
    SUPPORTED_LANGUAGES = ["uk", "en", "pl"]

class MainConstants:
    """Main constants"""
    DEFAULT_RECENT_HOURS = 24
    
    # API defaults
    DEFAULT_API_TIMEOUT = 10

class TranslationKeys:
    """Translation keys for gettext"""
    WELCOME = "🤖 Welcome to {bot_name}, {user_name}!\n\nI'm your personal assistant bot with the following features:\n• 🎭 Personalized jokes based on your input\n• 📊 Bot statistics and analytics\n• 🎛️ Interactive menu system\n• ⚙️ Admin panel for administrators\n\nUse /help to see all available commands!"
    MAIN_MENU = "Main menu"
    LANGUAGE_SELECTION = "Language selection"
    PLEASE_SELECT_LANGUAGE = "Please select your language:"
    LANGUAGE_CHANGED = "Language has been changed to {language}."
    JOKE = "Joke"
    STATISTICS = "Statistics"
    ADMIN_PANEL = "Admin Panel"
    BOT_INFO = "ℹ️ **Bot Information**\n\n**Bot Name:** {bot_name}\n**Version:** {bot_version}\n**Status:** ✅ Online\n**Features:** \n• Personalized Jokes API\n• User Statistics\n• Admin Panel\n• Interactive Menus\n\n**Developer:** {developer}\n**Created:** 2025"
    SETTINGS = "⚙️ Settings"
    ABOUT = "ℹ️ About"
    HELP = "❓ Help"
    SETTINGS_MENU = "⚙️ **Settings**\n\n**Available Settings:**\n• Language: {language}\n• Notifications: Enabled\n• Privacy: Standard\n\n**Coming Soon:**\n• Custom themes\n• Advanced preferences\n• User profiles"
    BACK_TO_MENU = "🔙 Back to Menu"
    CHANGE_LANGUAGE = "Change Language"
    HELP_COMMANDS = "🆘 **Help & Commands**\n\n**Basic Commands:**\n/start - Start the bot and see welcome message\n/help - Show this help message\n/info - Get bot information\n/menu - Show interactive menu\n/joke - Get a random joke\n/stats - Show bot statistics\n/admin - Admin panel (admin only)\n\n**Features:**\n• Interactive buttons and menus\n• Personalized jokes from external API\n• User input processing\n• User-friendly interface\n• Error handling\n\n**How to use:**\n1. Use the buttons below for quick actions\n2. Send any text message to get a personalized joke\n3. Use /menu to access all features"
    YOU_SAID = "📝 You said: {user_message}"
    CREATING_JOKE = "🎭 Creating a joke for you..."
    FETCHING_JOKE = "🎭 Fetching a joke for you..."
    TELL_ME_A_JOKE = "Tell me a joke"
    JOKE_BOT_HELP = "🤖 I'm a joke bot! Here's what I can do:\n\n• Send me any text and I'll create a personalized joke\n• Use /joke to get a random joke\n• Use /menu to see all available commands\n• Use /help for more information\n\nTry sending me something like \"Tell me a programming joke\" or \"I want a dad joke\"!"
    CREATE_JOKE = "🎭 Create Joke"
    MENU = "📋 Menu"
    ANOTHER_JOKE = "🎭 Another Joke"
    ERROR_GENERIC = "😅 Sorry, something went wrong. Please try again!"
    ERROR_STATS = "😅 Sorry, couldn't get statistics right now. Try again later!"
    ERROR_ADMIN = "😅 Sorry, couldn't get admin data right now. Try again later!"
    ERROR_JOKE = "😅 Sorry, I couldn't fetch a joke right now. Try again later!"
    ERROR_ACCESS_DENIED = "❌ Access denied. This command is for administrators only."
    STATS_UNAVAILABLE = "Statistics unavailable"
    UNKNOWN = "Unknown"
    DAY_UNIT = "d"
    HOUR_UNIT = "h"
    MINUTE_UNIT = "m"
    SECOND_UNIT = "s"
    STATS_HEADER = "📊 <b>Bot Statistics</b>"
    LAST_RESTART = "🕐 <b>Last Restart:</b>"
    UPTIME = "⏱️ <b>Uptime:</b>"
    USERS = "👥 <b>Users:</b>"
    TOTAL = "• Total:"
    LAST_24H = "• Last 24h:"
    MESSAGES = "📨 <b>Messages:</b>"
    COMMANDS = "• Commands:"
    TOP_COMMANDS = "🔥 <b>Top Commands:</b>"
    NO_DATA = "• No data"
    USERS_NOT_FOUND = "Users not found"
    USERS_LIST = "👥 <b>Users List:</b>"
    NO_USERNAME = "No username"
    USER_ID = "ID:"
    LAST_VISIT = "Last visit:"
    MESSAGES_COUNT = "Messages:"
    AND_MORE_USERS = "... and {count} more users"
    NO_NAME = "No name"
    JOKE_GENERATOR_PROMPT = "🎭 **Joke Generator**\n\nSend me any text and I'll create a personalized joke for you!\n\n**Examples:**\n• \"Tell me a programming joke\"\n• \"I want a dad joke\"\n• \"Make me laugh about cats\"\n• Or just send any text!\n\nI'll create a personalized joke for you! 😄"
    TRY_AGAIN = "🔄 Try Again"
    REFRESH = "🔄 Refresh"
    USER = "User"
    CONTACT = "📞 **Contact**\n\n**Get in Touch:**\n• Developer: {developer}\n• Email: {email}\n• GitHub: {github}\n• Support: Available 24/7\n\n**Report Issues:**\n• Use /help for assistance\n• Send feedback via messages\n• Report bugs directly"


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
