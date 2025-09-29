#!/usr/bin/env python3
"""
Base classes and interfaces for Telegram Bot
"""
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime, timezone
from constants import BotConstants

logger = logging.getLogger(__name__)

@dataclass
class UserInfo:
    """User information data class"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @property
    def display_name(self) -> str:
        """Get display name for user"""
        name_parts = []
        if self.first_name:
            name_parts.append(self.first_name)
        if self.last_name:
            name_parts.append(self.last_name)
        return " ".join(name_parts) if name_parts else "Без імені"
    
    @property
    def mention(self) -> str:
        """Get user mention string"""
        if self.username:
            return f"@{self.username}"
        elif self.first_name:
            return f"[{self.first_name}](tg://user?id={self.user_id})"
        else:
            return f"[User](tg://user?id={self.user_id})"

class BaseHandler(ABC):
    """Base class for all handlers"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def handle(self, update, context) -> None:
        """Handle the update"""
        pass
    
    def _track_user_interaction(self, user_info: UserInfo, command: str = None) -> None:
        """Track user interaction for statistics"""
        try:
            from utils import track_user_interaction, track_command_usage
            track_user_interaction(
                user_id=user_info.user_id,
                username=user_info.username,
                first_name=user_info.first_name,
                last_name=user_info.last_name
            )
            if command:
                track_command_usage(user_info.user_id, command)
        except Exception as e:
            self.logger.error(f"Error tracking user interaction: {e}")
    
    def _get_user_info(self, update) -> Optional[UserInfo]:
        """Extract user info from update"""
        try:
            user = update.effective_user or update.message.from_user if update.message else None
            if not user:
                return None
            
            return UserInfo(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
        except Exception as e:
            self.logger.error(f"Error extracting user info: {e}")
            return None

class BaseCommandHandler(BaseHandler):
    """Base class for command handlers"""
    
    async def handle(self, update, context) -> None:
        """Handle command with common logic"""
        try:
            # Check if update.message exists
            if not update.message:
                self.logger.error(f"Update.message is None in {self.__class__.__name__}")
                return
            
            # Get user info
            user_info = self._get_user_info(update)
            if user_info:
                self._track_user_interaction(user_info, self.command_name)
            
            # Execute specific command logic
            await self.execute_command(update, context, user_info)
            
        except Exception as e:
            self.logger.error(f"Error in {self.__class__.__name__}: {e}")
            await self.handle_error(update, context, e)
    
    @abstractmethod
    async def execute_command(self, update, context, user_info: Optional[UserInfo]) -> None:
        """Execute the specific command logic"""
        pass
    
    async def handle_error(self, update, context, error: Exception) -> None:
        """Handle command errors"""
        if update.message:
            await update.message.reply_text("😅 Sorry, something went wrong. Please try again!")
    
    @property
    @abstractmethod
    def command_name(self) -> str:
        """Get the command name"""
        pass

class BaseCallbackHandler(BaseHandler):
    """Base class for callback handlers"""
    
    async def handle(self, update, context) -> None:
        """Handle callback with common logic"""
        try:
            query = update.callback_query
            await query.answer()
            
            # Get user info
            user_info = self._get_user_info(update)
            if user_info:
                self._track_user_interaction(user_info, f"{self.callback_data}_callback")
            
            # Execute specific callback logic
            await self.execute_callback(query, context, user_info)
            
        except Exception as e:
            self.logger.error(f"Error in {self.__class__.__name__}: {e}")
            await self.handle_error(update, context, e)
    
    @abstractmethod
    async def execute_callback(self, query, context, user_info: Optional[UserInfo]) -> None:
        """Execute the specific callback logic"""
        pass
    
    async def handle_error(self, update, context, error: Exception) -> None:
        """Handle callback errors"""
        try:
            query = update.callback_query
            error_text = "😅 Sorry, something went wrong. Please try again!"
            from constants import KeyboardLayouts
            reply_markup = KeyboardLayouts.get_error_keyboard()
            await query.edit_message_text(error_text, reply_markup=reply_markup)
        except Exception as e:
            self.logger.error(f"Error handling callback error: {e}")
    
    @property
    @abstractmethod
    def callback_data(self) -> str:
        """Get the callback data"""
        pass

class BaseMessageHandler(BaseHandler):
    """Base class for message handlers"""
    
    async def handle(self, update, context) -> None:
        """Handle message with common logic"""
        try:
            # Check if update.message exists
            if not update.message:
                self.logger.error(f"Update.message is None in {self.__class__.__name__}")
                return
            
            # Get user info
            user_info = self._get_user_info(update)
            if user_info:
                self._track_user_interaction(user_info, "message")
            
            # Execute specific message logic
            await self.execute_message(update, context, user_info)
            
        except Exception as e:
            self.logger.error(f"Error in {self.__class__.__name__}: {e}")
            await self.handle_error(update, context, e)
    
    @abstractmethod
    async def execute_message(self, update, context, user_info: Optional[UserInfo]) -> None:
        """Execute the specific message logic"""
        pass
    
    async def handle_error(self, update, context, error: Exception) -> None:
        """Handle message errors"""
        if update.message:
            await update.message.reply_text("😅 Sorry, something went wrong. Please try again!")

class BaseStatsManager(ABC):
    """Base class for statistics managers"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def track_user(self, user_info: UserInfo) -> None:
        """Track user interaction"""
        pass
    
    @abstractmethod
    def track_command(self, user_id: int, command: str) -> None:
        """Track command usage"""
        pass
    
    @abstractmethod
    def get_stats_summary(self, lang: str = "uk") -> str:
        """Get formatted statistics summary"""
        pass
    
    @abstractmethod
    def get_users_list(self, lang: str = "uk", limit: int = BotConstants.DEFAULT_USERS_LIMIT) -> str:
        """Get formatted users list"""
        pass

class BaseAPIClient(ABC):
    """Base class for API clients"""
    
    def __init__(self, base_url: str, timeout: int = 10, headers: Dict[str, str] = None):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers or {}
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def make_request(self, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make API request"""
        pass
    
    @abstractmethod
    def format_response(self, response_data: Dict[str, Any]) -> str:
        """Format API response for display"""
        pass

class BaseConfig(ABC):
    """Base class for configuration"""
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate configuration"""
        pass
    
    @abstractmethod
    def get_required_vars(self) -> list:
        """Get list of required environment variables"""
        pass
    
    @abstractmethod
    def get_optional_vars(self) -> Dict[str, Any]:
        """Get dictionary of optional environment variables with defaults"""
        pass
