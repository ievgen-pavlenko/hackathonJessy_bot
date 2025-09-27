"""
Configuration module for Telegram Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables from config.env file (only if file exists)
if os.path.exists('config.env'):
    load_dotenv('config.env')

class Config:
    """Bot configuration class"""
    
    # Bot credentials - can come from environment or Docker secrets
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # Try to read from Docker secret if BOT_TOKEN is not set
    if not BOT_TOKEN:
        try:
            with open('/run/secrets/bot_token', 'r') as f:
                BOT_TOKEN = f.read().strip()
        except (FileNotFoundError, IOError):
            pass
    
    # Bot information
    BOT_NAME = os.getenv('BOT_NAME', 'Telegram Bot')
    BOT_VERSION = os.getenv('BOT_VERSION', '1.0.0')
    BOT_DEVELOPER = os.getenv('BOT_DEVELOPER', 'Your Name')
    BOT_EMAIL = os.getenv('BOT_EMAIL', 'your.email@example.com')
    BOT_GITHUB = os.getenv('BOT_GITHUB', 'github.com/yourusername')
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Docker-specific settings
    IS_DOCKER = os.getenv('DOCKER', 'false').lower() == 'true'
    
    # Database configuration (for future use)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # API keys (for future integrations)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    
    # Custom Jokes API configuration
    JOKES_API_URL = os.getenv('JOKES_API_URL')
    JOKES_API_KEY = os.getenv('JOKES_API_KEY')
    JOKES_API_TIMEOUT = int(os.getenv('JOKES_API_TIMEOUT', '10'))
    JOKES_API_ENDPOINT = os.getenv('JOKES_API_ENDPOINT', '/api/getJoke')
    JOKES_API_HEADERS = {
        'Content-Type': 'application/json',
        'User-Agent': f'{Config.BOT_NAME}/{Config.BOT_VERSION}'
    }
    
    # Add API key to headers if provided
    if JOKES_API_KEY:
        JOKES_API_HEADERS['Authorization'] = f'Bearer {JOKES_API_KEY}'
    
    # Full API URL with endpoint
    @classmethod
    def get_jokes_api_url(cls):
        """Get full API URL with endpoint"""
        if not cls.JOKES_API_URL:
            return None
        return f"{cls.JOKES_API_URL.rstrip('/')}{cls.JOKES_API_ENDPOINT}"
    
    @classmethod
    def validate(cls):
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
