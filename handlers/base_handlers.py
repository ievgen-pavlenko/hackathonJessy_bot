#!/usr/bin/env python3
"""
Base handlers for Telegram Bot
"""
import logging
from typing import Optional
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from base import BaseCommandHandler, BaseCallbackHandler, BaseMessageHandler, UserInfo
from constants import MessageTemplates, KeyboardLayouts, ButtonTexts
from user_states import state_manager, UserState

logger = logging.getLogger(__name__)

class StartCommandHandler(BaseCommandHandler):
    """Start command handler"""
    
    @property
    def command_name(self) -> str:
        return "/start"
    
    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute start command"""
        from config import Config
        
        welcome_message = MessageTemplates.WELCOME.format(
            bot_name=Config.BOT_NAME,
            user_name=user_info.display_name if user_info else "User"
        )
        
        keyboard = KeyboardLayouts.get_main_menu()
        
        await update.message.reply_text(
            welcome_message, 
            reply_markup=keyboard, 
            parse_mode=ParseMode.MARKDOWN
        )

class HelpCommandHandler(BaseCommandHandler):
    """Help command handler"""
    
    @property
    def command_name(self) -> str:
        return "/help"
    
    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute help command"""
        help_text = MessageTemplates.HELP_HEADER
        
        keyboard = KeyboardLayouts.get_main_menu()
        
        await update.message.reply_text(
            help_text, 
            reply_markup=keyboard, 
            parse_mode=ParseMode.MARKDOWN
        )

class InfoCommandHandler(BaseCommandHandler):
    """Info command handler"""
    
    @property
    def command_name(self) -> str:
        return "/info"
    
    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute info command"""
        from config import Config
        
        info_text = MessageTemplates.INFO_TEMPLATE.format(
            bot_name=Config.BOT_NAME,
            bot_version=Config.BOT_VERSION,
            developer=Config.BOT_DEVELOPER
        )
        
        keyboard = KeyboardLayouts.get_main_menu()
        
        await update.message.reply_text(
            info_text, 
            reply_markup=keyboard, 
            parse_mode=ParseMode.MARKDOWN
        )

class MenuCommandHandler(BaseCommandHandler):
    """Menu command handler"""
    
    @property
    def command_name(self) -> str:
        return "/menu"
    
    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute menu command"""
        from handlers.callback_handlers import show_menu
        await show_menu(update, context)

class StatsCommandHandler(BaseCommandHandler):
    """Stats command handler"""
    
    @property
    def command_name(self) -> str:
        return "/stats"
    
    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute stats command"""
        from stats import stats_manager
        
        stats_text = stats_manager.get_stats_summary()
        keyboard = KeyboardLayouts.get_stats_keyboard()
        
        await update.message.reply_text(
            stats_text, 
            reply_markup=keyboard, 
            parse_mode=ParseMode.HTML
        )

class AdminCommandHandler(BaseCommandHandler):
    """Admin command handler"""
    
    @property
    def command_name(self) -> str:
        return "/admin"
    
    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute admin command"""
        from utils import is_admin
        from stats import stats_manager
        
        # Check if user is admin
        if not user_info or not is_admin(user_info.user_id):
            await update.message.reply_text(MessageTemplates.ERROR_ACCESS_DENIED)
            return
        
        users_text = stats_manager.get_users_list(limit=20)
        keyboard = KeyboardLayouts.get_admin_keyboard()
        
        await update.message.reply_text(
            users_text, 
            reply_markup=keyboard, 
            parse_mode=ParseMode.HTML
        )

class JokeCommandHandler(BaseCommandHandler):
    """Joke command handler"""
    
    @property
    def command_name(self) -> str:
        return "/joke"
    
    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute joke command"""
        from utils import get_random_joke
        from telegram import InlineKeyboardMarkup, InlineKeyboardButton
        
        # Send loading message
        loading_message = await update.message.reply_text(MessageTemplates.LOADING_JOKE)
        
        try:
            # Get joke based on user input (if any)
            user_input = context.args[0] if context.args else "Розкажи анекдот"
            joke_text = await get_random_joke(user_input)
            
            # Update message with joke
            keyboard = KeyboardLayouts.get_joke_keyboard()
            
            await loading_message.edit_text(
                joke_text, 
                reply_markup=keyboard, 
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            self.logger.error(f"Error fetching joke: {e}")
            error_message = MessageTemplates.ERROR_JOKE
            keyboard = KeyboardLayouts.get_error_keyboard()
            
            await loading_message.edit_text(
                error_message, 
                reply_markup=keyboard
            )

class EchoMessageHandler(BaseMessageHandler):
    """Echo message handler for user messages"""
    
    async def execute_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute echo message with helpful response"""
        user_message = update.message.text
        
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
        keyboard = KeyboardLayouts.get_joke_keyboard()
        
        await update.message.reply_text(
            f"{echo_response}\n\n{help_text}",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )

class StatsCallbackHandler(BaseCallbackHandler):
    """Stats callback handler"""
    
    @property
    def callback_data(self) -> str:
        return "stats"
    
    async def execute_callback(self, query, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute stats callback"""
        from stats import stats_manager
        
        stats_text = stats_manager.get_stats_summary()
        keyboard = KeyboardLayouts.get_stats_keyboard()
        
        await query.edit_message_text(
            stats_text, 
            reply_markup=keyboard, 
            parse_mode=ParseMode.HTML
        )

class AdminCallbackHandler(BaseCallbackHandler):
    """Admin callback handler"""
    
    @property
    def callback_data(self) -> str:
        return "admin"
    
    async def execute_callback(self, query, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute admin callback"""
        from utils import is_admin
        from stats import stats_manager
        
        # Check if user is admin
        if not user_info or not is_admin(user_info.user_id):
            await query.edit_message_text(MessageTemplates.ERROR_ACCESS_DENIED)
            return
        
        users_text = stats_manager.get_users_list(limit=20)
        keyboard = KeyboardLayouts.get_admin_keyboard()
        
        await query.edit_message_text(
            users_text, 
            reply_markup=keyboard, 
            parse_mode=ParseMode.HTML
        )

class JokeCallbackHandler(BaseCallbackHandler):
    """Joke callback handler"""
    
    @property
    def callback_data(self) -> str:
        return "joke"
    
    async def execute_callback(self, query, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute joke callback - ask user for input"""
        if user_info:
            # Set user state to waiting for joke input
            state_manager.set_user_state(user_info.user_id, UserState.WAITING_FOR_JOKE_INPUT)
        
        joke_prompt = """
🎭 **Joke Generator**

Send me any text and I'll create a personalized joke for you!

**Examples:**
• "Tell me a programming joke"
• "I want a dad joke"
• "Make me laugh about cats"
• Or just send any text!

I'll create a personalized joke for you! 😄
        """
        
        keyboard = [[InlineKeyboardButton(ButtonTexts.BACK_TO_MENU, callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            joke_prompt, 
            reply_markup=reply_markup, 
            parse_mode=ParseMode.MARKDOWN
        )
