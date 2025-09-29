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
from constants import TranslationKeys
from user_states import state_manager, UserState
from localization import translate
from stats import stats_manager
from telegram import InlineKeyboardButton

def _get_main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Get main menu keyboard layout"""
    keyboard = [
        [InlineKeyboardButton(translate(TranslationKeys.STATISTICS, lang), callback_data='stats'), InlineKeyboardButton(translate(TranslationKeys.SETTINGS, lang), callback_data='settings')],
        [InlineKeyboardButton(translate(TranslationKeys.JOKE, lang), callback_data='joke'), InlineKeyboardButton(translate(TranslationKeys.ABOUT, lang), callback_data='info')],
        [InlineKeyboardButton(translate(TranslationKeys.HELP, lang), callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

def _get_error_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Get error keyboard layout"""
    keyboard = [
        [InlineKeyboardButton(translate(TranslationKeys.TRY_AGAIN, lang), callback_data='joke'), InlineKeyboardButton(translate(TranslationKeys.MENU, lang), callback_data='menu')]
    ]
    return InlineKeyboardMarkup(keyboard)


class LanguageCommandHandler(BaseCommandHandler):
    """Language command handler"""

    @property
    def command_name(self) -> str:
        return "language"

    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute language command"""
        lang = stats_manager.get_user_language(user_info.user_id)
        text = translate(TranslationKeys.PLEASE_SELECT_LANGUAGE, lang)
        keyboard = [
            [InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_uk')],
            [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
            [InlineKeyboardButton("🇵🇱 Polski", callback_data='lang_pl')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup)


class StartCommandHandler(BaseCommandHandler):
    """Start command handler"""

    @property
    def command_name(self) -> str:
        return "/start"

    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute start command"""
        from config import Config

        lang = stats_manager.get_user_language(user_info.user_id)
        welcome_message = translate(TranslationKeys.WELCOME, lang).format(
            bot_name=Config.BOT_NAME,
            user_name=user_info.display_name if user_info else translate(TranslationKeys.USER, lang)
        )

        keyboard = _get_main_menu_keyboard(lang)

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
        lang = stats_manager.get_user_language(user_info.user_id)
        help_text = translate(TranslationKeys.HELP_COMMANDS_V2, lang)

        keyboard = _get_main_menu_keyboard(lang)

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

        lang = stats_manager.get_user_language(user_info.user_id)
        info_text = translate(TranslationKeys.BOT_INFO, lang).format(
            bot_name=Config.BOT_NAME,
            bot_version=Config.BOT_VERSION,
            developer=Config.BOT_DEVELOPER
        )

        keyboard = _get_main_menu_keyboard(lang)

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
        await show_menu(update, context, update.message)

class StatsCommandHandler(BaseCommandHandler):
    """Stats command handler"""

    @property
    def command_name(self) -> str:
        return "/stats"

    async def execute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute stats command"""
        from stats import stats_manager

        lang = stats_manager.get_user_language(user_info.user_id)
        stats_text = stats_manager.get_stats_summary(lang)
        keyboard = [
            [InlineKeyboardButton(translate(TranslationKeys.REFRESH, lang), callback_data='stats'), InlineKeyboardButton(translate(TranslationKeys.MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            stats_text,
            reply_markup=reply_markup,
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
            lang = stats_manager.get_user_language(user_info.user_id)
            await update.message.reply_text(translate(TranslationKeys.ERROR_ACCESS_DENIED, lang))
            return

        lang = stats_manager.get_user_language(user_info.user_id)
        users_text = stats_manager.get_users_list(limit=20)
        keyboard = [
            [InlineKeyboardButton(translate(TranslationKeys.REFRESH, lang), callback_data='admin'), InlineKeyboardButton(translate(TranslationKeys.STATISTICS, lang), callback_data='stats')],
            [InlineKeyboardButton(translate(TranslationKeys.MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            users_text,
            reply_markup=reply_markup,
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

        lang = stats_manager.get_user_language(user_info.user_id)
        # Send loading message
        loading_message = await update.message.reply_text(translate(TranslationKeys.FETCHING_JOKE, lang))

        try:
            # Get joke based on user input (if any)
            default_prompt = translate(TranslationKeys.TELL_ME_A_JOKE, lang)
            user_input = context.args[0] if context.args else default_prompt
            joke_text = await get_random_joke(user_input, lang)

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
            self.logger.error(f"Error fetching joke: {e}")
            error_message = translate(TranslationKeys.ERROR_JOKE, lang)
            keyboard = _get_error_keyboard(lang)

            await loading_message.edit_text(
                error_message,
                reply_markup=keyboard
            )

class EchoMessageHandler(BaseMessageHandler):
    """Echo message handler for user messages"""

    async def execute_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_info: Optional[UserInfo]) -> None:
        """Execute echo message with helpful response"""
        from utils import get_random_joke

        lang = stats_manager.get_user_language(user_info.user_id)
        user_message = update.message.text

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
            self.logger.error(f"Error fetching joke: {e}")
            error_message = translate(TranslationKeys.ERROR_JOKE, lang)
            keyboard = _get_error_keyboard(lang)

            await loading_message.edit_text(
                error_message,
                reply_markup=keyboard
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
