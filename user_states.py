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
    def __init__(self):
        self.user_states = {}  # Now stores {user_id: (state, context_data)}
        self.last_joke_input = {}

    def set_last_joke_input(self, user_id: int, joke_input: str):
        self.last_joke_input[user_id] = joke_input

    def get_last_joke_input(self, user_id: int):
        return self.last_joke_input.get(user_id)

    def set_user_state(self, user_id: int, state: UserState, context_data=None):
        self.user_states[user_id] = (state, context_data)

    def get_user_state(self, user_id: int):
        return self.user_states.get(user_id, (None, None))

    def is_waiting_for_joke_input(self, user_id: int) -> bool:
        state, _ = self.get_user_state(user_id)
        return state == UserState.WAITING_FOR_JOKE_INPUT

    def get_joke_prompt_message_id(self, user_id: int):
        state, context_data = self.get_user_state(user_id)
        if state == UserState.WAITING_FOR_JOKE_INPUT:
            return context_data
        return None

    def clear_user_state(self, user_id: int):
        if user_id in self.user_states:
            del self.user_states[user_id]

# Global state manager instance
state_manager = UserStateManager()
