"""
Configuration module for Telegram Bot
"""
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

from base import BaseConfig
from constants import BotConstants, APIConstants

# Load environment variables from config.env file (only if file exists)
if os.path.exists('config.env'):
    load_dotenv('config.env')

class Config(BaseConfig):
    """Bot configuration class"""
    
    # Bot credentials from environment variable
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # Bot information
    BOT_NAME = os.getenv('BOT_NAME', BotConstants.DEFAULT_BOT_NAME)
    BOT_VERSION = os.getenv('BOT_VERSION', BotConstants.DEFAULT_BOT_VERSION)
    BOT_DEVELOPER = os.getenv('BOT_DEVELOPER', BotConstants.DEFAULT_BOT_DEVELOPER)
    BOT_EMAIL = os.getenv('BOT_EMAIL', BotConstants.DEFAULT_BOT_EMAIL)
    BOT_GITHUB = os.getenv('BOT_GITHUB', BotConstants.DEFAULT_BOT_GITHUB)
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', BotConstants.DEFAULT_LOG_LEVEL)
    LOG_FORMAT = os.getenv('LOG_FORMAT', BotConstants.DEFAULT_LOG_FORMAT)
    
    # Docker-specific settings
    IS_DOCKER = os.getenv('DOCKER', 'false').lower() == 'true'
    
    # Database configuration (for future use)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # Custom Jokes API configuration
    JOKES_API_URL = os.getenv('JOKES_API_URL')
    JOKES_API_KEY = os.getenv('JOKES_API_KEY')
    JOKES_API_TIMEOUT = int(os.getenv('JOKES_API_TIMEOUT', str(APIConstants.DEFAULT_TIMEOUT)))
    JOKES_API_ENDPOINT = os.getenv('JOKES_API_ENDPOINT', '/api/getJoke')
    JOKES_API_HEADERS = APIConstants.DEFAULT_HEADERS.copy()
    
    # Add API key to headers if provided
    if JOKES_API_KEY:
        JOKES_API_HEADERS['Authorization'] = f'Bearer {JOKES_API_KEY}'
    
    # Admin configuration
    ADMIN_USER_IDS = []
    _admin_ids_str = os.getenv('ADMIN_USER_IDS', '')
    if _admin_ids_str:
        try:
            ADMIN_USER_IDS = [int(uid.strip()) for uid in _admin_ids_str.split(',') if uid.strip()]
        except ValueError:
            pass
    
    # Statistics configuration
    STATS_DATA_DIR = os.getenv('STATS_DATA_DIR', BotConstants.DEFAULT_STATS_DATA_DIR)
    
    # Full API URL with endpoint
    @classmethod
    def get_jokes_api_url(cls):
        """Get full API URL with endpoint"""
        if not cls.JOKES_API_URL:
            return None
        return f"{cls.JOKES_API_URL.rstrip('/')}{cls.JOKES_API_ENDPOINT}"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.BOT_TOKEN:
            raise ValueError(
                "BOT_TOKEN is required. Set it as environment variable or Docker secret."
            )
        if not cls.JOKES_API_URL:
            raise ValueError(
                "JOKES_API_URL is required for joke functionality. Set it as environment variable."
            )
        return True
    
    @classmethod
    def get_required_vars(cls) -> List[str]:
        """Get list of required environment variables"""
        return ['BOT_TOKEN', 'JOKES_API_URL']
    
    @classmethod
    def get_optional_vars(cls) -> Dict[str, Any]:
        """Get dictionary of optional environment variables with defaults"""
        return {
            'BOT_NAME': BotConstants.DEFAULT_BOT_NAME,
            'BOT_VERSION': BotConstants.DEFAULT_BOT_VERSION,
            'BOT_DEVELOPER': BotConstants.DEFAULT_BOT_DEVELOPER,
            'BOT_EMAIL': BotConstants.DEFAULT_BOT_EMAIL,
            'BOT_GITHUB': BotConstants.DEFAULT_BOT_GITHUB,
            'LOG_LEVEL': BotConstants.DEFAULT_LOG_LEVEL,
            'LOG_FORMAT': BotConstants.DEFAULT_LOG_FORMAT,
            'JOKES_API_TIMEOUT': APIConstants.DEFAULT_TIMEOUT,
            'STATS_DATA_DIR': BotConstants.DEFAULT_STATS_DATA_DIR
        }
    
    @classmethod
    def get_bot_info(cls):
        """Get bot information for logging"""
        return {
            'name': cls.BOT_NAME,
            'version': cls.BOT_VERSION,
            'developer': cls.BOT_DEVELOPER,
            'docker': cls.IS_DOCKER
        }

# Validate configuration on import
Config.validate()
