"""
Utility functions for Telegram Bot
"""
import logging
import requests
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

def setup_logging(log_level: str = "INFO", log_format: str = None, docker_mode: bool = False) -> None:
    """Setup logging configuration"""
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure handlers based on environment
    handlers = [logging.StreamHandler()]  # Always log to stdout/stderr
    
    # Add file handler only if not in Docker or if explicitly requested
    if not docker_mode:
        try:
            handlers.append(logging.FileHandler('bot.log', encoding='utf-8'))
        except (PermissionError, OSError):
            # If can't write to file, just use stdout
            pass
    
    logging.basicConfig(
        format=log_format,
        level=getattr(logging, log_level.upper()),
        handlers=handlers,
        force=True  # Force reconfiguration
    )

def get_current_time() -> str:
    """Get current time as formatted string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_user_info(user) -> str:
    """Format user information for logging"""
    return f"User: {user.first_name} {user.last_name or ''} (ID: {user.id})"

def validate_message_length(message: str, max_length: int = 4096) -> bool:
    """Validate message length for Telegram limits"""
    return len(message) <= max_length

def truncate_message(message: str, max_length: int = 4096) -> str:
    """Truncate message if it exceeds Telegram limits"""
    if len(message) <= max_length:
        return message
    return message[:max_length-3] + "..."

def escape_markdown(text: str) -> str:
    """Escape special characters for Markdown parsing"""
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

def format_stats(stats: dict) -> str:
    """Format statistics dictionary into readable string"""
    formatted = []
    for key, value in stats.items():
        formatted.append(f"• {key}: {value}")
    return "\n".join(formatted)

def is_admin(user_id: int, admin_ids: list = None) -> bool:
    """Check if user is admin"""
    if admin_ids is None:
        admin_ids = []
    return user_id in admin_ids

def get_user_mention(user) -> str:
    """Get user mention string"""
    if user.username:
        return f"@{user.username}"
    return f"[{user.first_name}](tg://user?id={user.id})"

# Jokes API functions
async def fetch_joke(user_input: str = "Розкажи анекдот") -> Optional[Dict[str, Any]]:
    """Fetch a joke from your custom API using POST request with user input"""
    try:
        # Prepare request data according to API schema
        request_data = {
            "input": user_input  # User input is passed to the API
        }
        
        # Get full API URL with endpoint
        api_url = Config.get_jokes_api_url()
        if not api_url:
            logger.error("Jokes API URL is not configured")
            logger.error("Set JOKES_API_URL environment variable")
            return None
        
        logger.info(f"Making request to: {api_url}")
        logger.info(f"Request data: {request_data}")
        logger.info(f"Headers: {Config.JOKES_API_HEADERS}")
        
        # Use asyncio to run the blocking request in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: requests.post(
                api_url,
                json=request_data,
                timeout=Config.JOKES_API_TIMEOUT,
                headers=Config.JOKES_API_HEADERS
            )
        )
        
        if response.status_code == 200:
            joke_data = response.json()
            logger.info("Successfully fetched joke from custom API")
            return joke_data
        elif response.status_code == 401:
            logger.error("Jokes API authentication failed - check API key")
            return None
        elif response.status_code == 403:
            logger.error("Jokes API access forbidden - check API permissions")
            return None
        elif response.status_code == 404:
            logger.error("Jokes API endpoint not found - check API URL and endpoint")
            return None
        elif response.status_code == 500:
            logger.error("Jokes API internal server error")
            logger.error(f"Response body: {response.text}")
            logger.error("Possible causes: API server not configured, database issues, missing env vars")
            return None
        elif response.status_code >= 500:
            logger.error(f"Jokes API server error: {response.status_code}")
            return None
        else:
            logger.warning(f"Jokes API returned status {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error("Jokes API request timed out")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("Jokes API connection failed - check network and URL")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Jokes API request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching joke: {e}")
        return None

def format_joke(joke_data: Dict[str, Any]) -> str:
    """Format joke data from your custom API into a readable string"""
    if not joke_data:
        return "😅 Sorry, I couldn't fetch a joke right now. Try again later!"
    
    # Extract joke text from API response according to schema
    joke_text = joke_data.get('response')
    
    if joke_text:
        # Format the joke with emoji and markdown
        return f"🎭 **Анекдот**\n\n{joke_text}"
    else:
        # Fallback: try to display any text content
        for key in ['response', 'joke', 'text', 'content', 'message']:
            if joke_data.get(key):
                return f"🎭 **Анекдот**\n\n{joke_data[key]}"
        
        return "😅 Sorry, I couldn't fetch a joke right now. Try again later!"

async def get_random_joke(user_input: str = "Розкажи анекдот") -> str:
    """Get a formatted joke based on user input"""
    joke_data = await fetch_joke(user_input)
    return format_joke(joke_data)
