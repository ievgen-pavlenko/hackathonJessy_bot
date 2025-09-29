"""
Callback handlers for Telegram Bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import Config
from utils import get_random_joke, track_user_interaction, track_command_usage, is_admin
from stats import stats_manager
from base import UserInfo
from constants import TranslationKeys
from user_states import state_manager, UserState
from localization import translate

logger = logging.getLogger(__name__)


async def handle_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language selection callback."""
    query = update.callback_query
    user_id = query.from_user.id
    lang_code = query.data.split('_')[1]

    stats_manager.set_user_language(user_id, lang_code)

    language_names = {"uk": "Українська", "en": "English", "pl": "Polski"}
    confirmation_text = translate(TranslationKeys.LANGUAGE_CHANGED, lang_code).format(language=language_names[lang_code])

    await query.answer(confirmation_text)
    await show_menu(update, context, query.message)

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message=None) -> None:
    """Display the main menu."""
    # Track user interaction
    user = update.effective_user
    lang = stats_manager.get_user_language(user.id)
    if user:
        track_user_interaction(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        track_command_usage(user.id, 'menu_callback')

        # Clear user state when returning to menu
        state_manager.clear_user_state(user.id)

    menu_text = translate(TranslationKeys.MAIN_MENU, lang)

    keyboard = [
        [InlineKeyboardButton(translate(TranslationKeys.STATISTICS, lang), callback_data='stats'), InlineKeyboardButton(translate(TranslationKeys.SETTINGS, lang), callback_data='settings')],
        [InlineKeyboardButton(translate(TranslationKeys.JOKE, lang), callback_data='joke'), InlineKeyboardButton(translate(TranslationKeys.ABOUT, lang), callback_data='info')],
        [InlineKeyboardButton(translate(TranslationKeys.HELP, lang), callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if message:
        await message.reply_text(menu_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.callback_query.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()

    if query.data.startswith('lang_'):
        await handle_language_callback(update, context)
        return

    if query.data == 'menu':
        await show_menu(update, context, query.message)
    elif query.data == 'info':
        await handle_info_callback(update, context)
    elif query.data == 'help':
        await handle_help_callback(update, context)
    elif query.data == 'stats':
        await handle_stats_callback(update, context)
    elif query.data == 'settings':
        await handle_settings_callback(update, context)
    elif query.data == 'change_language':
        await handle_change_language_callback(update, context)
    elif query.data == 'contact':
        await handle_contact_callback(update, context)
    elif query.data == 'echo_again':
        await query.edit_message_text("🔄 Send me any message and I'll echo it back to you!")
    elif query.data == 'joke':
        await handle_joke_callback(update, context)
    elif query.data == 'admin':
        await handle_admin_callback(update, context)

async def handle_info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle info button callback."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = stats_manager.get_user_language(user_id)

    info_text = translate(TranslationKeys.BOT_INFO, lang).format(
        bot_name=Config.BOT_NAME,
        bot_version=Config.BOT_VERSION,
        developer=Config.BOT_DEVELOPER
    )
    keyboard = [[InlineKeyboardButton(translate(TranslationKeys.BACK_TO_MENU, lang), callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(info_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle help button callback."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = stats_manager.get_user_language(user_id)

    help_text = translate(TranslationKeys.HELP_COMMANDS, lang)

    keyboard = [[InlineKeyboardButton(translate(TranslationKeys.BACK_TO_MENU, lang), callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle stats button callback."""
    query = update.callback_query
    try:
        # Track user interaction
        user = query.from_user
        if user:
            track_user_interaction(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            track_command_usage(user.id, 'stats_callback')

        lang = stats_manager.get_user_language(user.id)
        # Get statistics
        stats_text = stats_manager.get_stats_summary(lang)

        # Create keyboard
        keyboard = [
            [InlineKeyboardButton(translate("🔄 Refresh", lang), callback_data='stats'), InlineKeyboardButton(translate(TranslationKeys.MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            stats_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        logger.error(f"Error in stats callback: {e}")
        lang = stats_manager.get_user_language(query.from_user.id)
        error_text = translate(TranslationKeys.ERROR_STATS, lang)
        keyboard = [
            [InlineKeyboardButton(translate(TranslationKeys.TRY_AGAIN, lang), callback_data='stats'), InlineKeyboardButton(translate(TranslationKeys.BACK_TO_MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            error_text,
            reply_markup=reply_markup
        )

async def handle_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle settings button callback."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = stats_manager.get_user_language(user_id)

    language_names = {"uk": "Українська", "en": "English", "pl": "Polski"}
    current_language_name = language_names.get(lang, lang)

    settings_text = translate(TranslationKeys.SETTINGS_MENU, lang).format(language=current_language_name)

    keyboard = [
        [InlineKeyboardButton(translate(TranslationKeys.CHANGE_LANGUAGE, lang), callback_data='change_language')],
        [InlineKeyboardButton(translate(TranslationKeys.BACK_TO_MENU, lang), callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(settings_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def handle_contact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle contact button callback."""
    query = update.callback_query
    lang = stats_manager.get_user_language(query.from_user.id)
    contact_text = translate(TranslationKeys.CONTACT, lang).format(
        developer=Config.BOT_DEVELOPER,
        email=Config.BOT_EMAIL,
        github=Config.BOT_GITHUB
    )
    keyboard = [[InlineKeyboardButton(translate(TranslationKeys.BACK_TO_MENU, lang), callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(contact_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_joke_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle joke button callback - ask user for input."""
    query = update.callback_query
    try:
        # Track user interaction
        user = query.from_user
        if user:
            track_user_interaction(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            track_command_usage(user.id, 'joke_callback')

            # Set user state to waiting for joke input
            state_manager.set_user_state(user.id, UserState.WAITING_FOR_JOKE_INPUT)

        lang = stats_manager.get_user_language(user.id)
        # Ask user for joke input
        joke_prompt = translate(TranslationKeys.JOKE_GENERATOR_PROMPT, lang)

        keyboard = [
            [InlineKeyboardButton(translate(TranslationKeys.BACK_TO_MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            joke_prompt,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception as e:
        logger.error(f"Error in joke callback: {e}")
        lang = stats_manager.get_user_language(query.from_user.id)
        error_text = translate(TranslationKeys.ERROR_JOKE, lang)
        keyboard = [
            [InlineKeyboardButton(translate(TranslationKeys.TRY_AGAIN, lang), callback_data='joke'), InlineKeyboardButton(translate(TranslationKeys.BACK_TO_MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            error_text,
            reply_markup=reply_markup
        )

async def handle_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle stats button callback."""
    query = update.callback_query
    try:
        # Track user interaction
        user = query.from_user
        if user:
            track_user_interaction(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            track_command_usage(user.id, 'stats_callback')

        lang = stats_manager.get_user_language(user.id)
        # Get statistics
        stats_text = stats_manager.get_stats_summary(lang)

        # Create keyboard
        keyboard = [
            [InlineKeyboardButton(translate("🔄 Refresh", lang), callback_data='stats'), InlineKeyboardButton(translate(TranslationKeys.MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            stats_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        logger.error(f"Error in stats callback: {e}")
        lang = stats_manager.get_user_language(query.from_user.id)
        error_text = translate(TranslationKeys.ERROR_STATS, lang)
        keyboard = [
            [InlineKeyboardButton(translate(TranslationKeys.TRY_AGAIN, lang), callback_data='stats'), InlineKeyboardButton(translate(TranslationKeys.BACK_TO_MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            error_text,
            reply_markup=reply_markup
        )

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin button callback."""
    query = update.callback_query
    try:
        # Check if user is admin
        user = query.from_user
        lang = stats_manager.get_user_language(user.id)
        if not is_admin(user.id):
            await query.edit_message_text(translate(TranslationKeys.ERROR_ACCESS_DENIED, lang))
            return

        # Track user interaction
        if user:
            track_user_interaction(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            track_command_usage(user.id, 'admin_callback')

        # Get users list
        users_text = stats_manager.get_users_list(lang, limit=20)

        # Create keyboard
        keyboard = [
            [InlineKeyboardButton(translate(TranslationKeys.REFRESH, lang), callback_data='admin'), InlineKeyboardButton(translate(TranslationKeys.STATISTICS, lang), callback_data='stats')],
            [InlineKeyboardButton(translate(TranslationKeys.MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            users_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        logger.error(f"Error in admin callback: {e}")
        lang = stats_manager.get_user_language(query.from_user.id)
        error_text = translate(TranslationKeys.ERROR_ADMIN, lang)
        keyboard = [
            [InlineKeyboardButton(translate(TranslationKeys.TRY_AGAIN, lang), callback_data='admin'), InlineKeyboardButton(translate(TranslationKeys.BACK_TO_MENU, lang), callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            error_text,
            reply_markup=reply_markup
        )

async def handle_change_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle change_language button callback."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = stats_manager.get_user_language(user_id)

    text = translate(TranslationKeys.PLEASE_SELECT_LANGUAGE, lang)
    keyboard = [
        [InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_uk')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇵🇱 Polski", callback_data='lang_pl')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)
