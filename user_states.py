#!/usr/bin/env python3
"""
User states management for Telegram Bot
"""
from typing import Dict, Optional
from enum import Enum

class UserState(Enum):
    """User states"""
    NORMAL = "normal"
    WAITING_FOR_JOKE_INPUT = "waiting_for_joke_input"

class UserStateManager:
    """Manages user states"""
    
    def __init__(self):
        self.user_states: Dict[int, UserState] = {}
    
    def set_user_state(self, user_id: int, state: UserState) -> None:
        """Set user state"""
        self.user_states[user_id] = state
    
    def get_user_state(self, user_id: int) -> UserState:
        """Get user state"""
        return self.user_states.get(user_id, UserState.NORMAL)
    
    def clear_user_state(self, user_id: int) -> None:
        """Clear user state"""
        if user_id in self.user_states:
            del self.user_states[user_id]
    
    def is_waiting_for_joke_input(self, user_id: int) -> bool:
        """Check if user is waiting for joke input"""
        return self.get_user_state(user_id) == UserState.WAITING_FOR_JOKE_INPUT

# Global state manager instance
state_manager = UserStateManager()
