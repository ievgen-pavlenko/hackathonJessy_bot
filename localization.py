#!/usr/bin/env python3
"""
Localization module for the Telegram bot.
Handles multi-language support using polib.
"""
import os
import polib
from typing import Dict

from constants import BotConstants

LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'locales')

# Dictionary to hold PO file objects
po_files: Dict[str, polib.POFile] = {}

def load_translations():
    """Load all available translations from .po files"""
    for lang in BotConstants.SUPPORTED_LANGUAGES:
        po_file_path = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'bot.po')
        if os.path.exists(po_file_path):
            try:
                po_files[lang] = polib.pofile(po_file_path)
            except Exception as e:
                print(f"Error loading translation file for language '{lang}': {e}")
        else:
            print(f"Translation file for language '{lang}' not found.")

def translate(text: str, lang: str) -> str:
    """Translate a given text to the specified language"""
    if lang in po_files:
        entry = po_files[lang].find(text)
        if entry and entry.msgstr:
            return entry.msgstr
    # Fallback to default language if translation not found
    if BotConstants.DEFAULT_LANG in po_files:
        entry = po_files[BotConstants.DEFAULT_LANG].find(text)
        if entry and entry.msgstr:
            return entry.msgstr
    # Fallback to msgid if no translation is found at all
    return text

# Load translations on module import
load_translations()