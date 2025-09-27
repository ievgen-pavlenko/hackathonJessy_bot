#!/usr/bin/env python3
"""
Statistics module for Telegram bot
Handles user tracking, bot statistics, and data persistence
"""
import json
import os
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path

from base import BaseStatsManager, UserInfo
from constants import StatsConstants, BotConstants

logger = logging.getLogger(__name__)

@dataclass
class UserStats:
    """User statistics data structure"""
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    first_seen: str
    last_seen: str
    message_count: int
    commands_used: Dict[str, int]

@dataclass
class BotStats:
    """Bot statistics data structure"""
    start_time: str
    last_restart: str
    total_users: int
    total_messages: int
    total_commands: int
    commands_breakdown: Dict[str, int]

class StatsManager(BaseStatsManager):
    """Manages bot and user statistics"""
    
    def __init__(self, data_dir: str = BotConstants.DEFAULT_STATS_DATA_DIR):
        super().__init__(data_dir)
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.users_file = self.data_dir / "users.json"
        self.stats_file = self.data_dir / "bot_stats.json"
        
        self.users: Dict[int, UserStats] = {}
        self.bot_stats: Optional[BotStats] = None
        
        self._load_data()
        self._update_bot_start_time()
    
    def _load_data(self):
        """Load existing data from files"""
        try:
            # Load users
            if self.users_file.exists():
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    for user_id_str, user_data in users_data.items():
                        user_id = int(user_id_str)
                        self.users[user_id] = UserStats(**user_data)
                logger.info(f"Loaded {len(self.users)} users from storage")
            
            # Load bot stats
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    stats_data = json.load(f)
                    self.bot_stats = BotStats(**stats_data)
                logger.info("Loaded bot statistics from storage")
            else:
                self._initialize_bot_stats()
                
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            self._initialize_bot_stats()
    
    def _initialize_bot_stats(self):
        """Initialize bot statistics"""
        now = datetime.now(timezone.utc).isoformat()
        self.bot_stats = BotStats(
            start_time=now,
            last_restart=now,
            total_users=0,
            total_messages=0,
            total_commands=0,
            commands_breakdown={}
        )
    
    def _update_bot_start_time(self):
        """Update bot start time on restart"""
        now = datetime.now(timezone.utc).isoformat()
        if self.bot_stats:
            self.bot_stats.last_restart = now
    
    def _save_data(self):
        """Save data to files"""
        try:
            # Save users
            users_data = {str(user_id): asdict(user_stats) for user_id, user_stats in self.users.items()}
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2, ensure_ascii=False)
            
            # Save bot stats
            if self.bot_stats:
                with open(self.stats_file, 'w', encoding='utf-8') as f:
                    json.dump(asdict(self.bot_stats), f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def track_user(self, user_info: UserInfo) -> None:
        """Track user interaction"""
        now = datetime.now(timezone.utc).isoformat()
        
        if user_info.user_id in self.users:
            # Update existing user
            user = self.users[user_info.user_id]
            old_last_seen = user.last_seen
            user.last_seen = now
            user.message_count += 1
            if user_info.username:
                user.username = user_info.username
            if user_info.first_name:
                user.first_name = user_info.first_name
            if user_info.last_name:
                user.last_name = user_info.last_name
            
            self.logger.debug(f"Updated user {user_info.user_id}: last_seen {old_last_seen} -> {now}")
        else:
            # Create new user
            user = UserStats(
                user_id=user_info.user_id,
                username=user_info.username,
                first_name=user_info.first_name,
                last_name=user_info.last_name,
                first_seen=now,
                last_seen=now,
                message_count=1,
                commands_used={}
            )
            self.users[user_info.user_id] = user
            self.logger.info(f"New user tracked: {user_info.user_id} (@{user_info.username or 'unknown'})")
        
        # Update bot stats
        if self.bot_stats:
            self.bot_stats.total_users = len(self.users)
            self.bot_stats.total_messages += 1
        
        self._save_data()
    
    def track_user_legacy(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Legacy method for backward compatibility"""
        user_info = UserInfo(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        self.track_user(user_info)
    
    def track_command(self, user_id: int, command: str):
        """Track command usage"""
        if user_id in self.users:
            user = self.users[user_id]
            if command not in user.commands_used:
                user.commands_used[command] = 0
            user.commands_used[command] += 1
        
        # Update bot stats
        if self.bot_stats:
            self.bot_stats.total_commands += 1
            if command not in self.bot_stats.commands_breakdown:
                self.bot_stats.commands_breakdown[command] = 0
            self.bot_stats.commands_breakdown[command] += 1
        
        self._save_data()
    
    def get_user_stats(self, user_id: int) -> Optional[UserStats]:
        """Get user statistics"""
        return self.users.get(user_id)
    
    def get_all_users(self) -> List[UserStats]:
        """Get all users sorted by last seen"""
        return sorted(self.users.values(), key=lambda x: x.last_seen, reverse=True)
    
    def get_bot_stats(self) -> Optional[BotStats]:
        """Get bot statistics"""
        return self.bot_stats
    
    def get_stats_summary(self) -> str:
        """Get formatted statistics summary"""
        if not self.bot_stats:
            return "Статистика недоступна"
        
        # Calculate uptime
        try:
            start_time = datetime.fromisoformat(self.bot_stats.start_time.replace('Z', '+00:00'))
            uptime = datetime.now(timezone.utc) - start_time
            uptime_str = self._format_duration(uptime)
        except:
            uptime_str = "Невідомо"
        
        # Get recent users (last 24 hours)
        recent_users = self._get_recent_users_count()
        
        # Format last restart
        try:
            last_restart = datetime.fromisoformat(self.bot_stats.last_restart.replace('Z', '+00:00'))
            last_restart_str = last_restart.strftime(StatsConstants.DATETIME_FORMAT)
        except:
            last_restart_str = "Невідомо"
        
        # Top commands
        commands_text = self._format_top_commands()
        
        return f"""{StatsConstants.STATS_HEADER}

{StatsConstants.LAST_RESTART} {last_restart_str}
{StatsConstants.UPTIME} {uptime_str}

{StatsConstants.USERS_TOTAL}
• Всього: {self.bot_stats.total_users}
• За останні 24 год: {recent_users}

{StatsConstants.MESSAGES_TOTAL}
• Всього: {self.bot_stats.total_messages}
• Команд: {self.bot_stats.total_commands}

{StatsConstants.TOP_COMMANDS}
{commands_text if commands_text else StatsConstants.NO_DATA}"""
    
    def _get_recent_users_count(self) -> int:
        """Get count of users active in last 24 hours"""
        recent_users = 0
        try:
            now = datetime.now(timezone.utc)
            cutoff_time = now - timedelta(hours=24)
            
            for user in self.users.values():
                try:
                    # Parse last_seen timestamp
                    last_seen_str = user.last_seen
                    # Handle different datetime formats
                    if last_seen_str.endswith('+00:00'):
                        last_seen_dt = datetime.fromisoformat(last_seen_str)
                    elif last_seen_str.endswith('Z'):
                        last_seen_dt = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
                    else:
                        last_seen_dt = datetime.fromisoformat(last_seen_str)
                        if last_seen_dt.tzinfo is None:
                            last_seen_dt = last_seen_dt.replace(tzinfo=timezone.utc)
                    
                    if last_seen_dt > cutoff_time:
                        recent_users += 1
                        
                except Exception as e:
                    self.logger.error(f"Error parsing last_seen for user {user.user_id}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error calculating recent users: {e}")
        return recent_users
    
    def _format_top_commands(self) -> str:
        """Format top commands for display"""
        if not self.bot_stats or not self.bot_stats.commands_breakdown:
            return ""
        
        top_commands = sorted(
            self.bot_stats.commands_breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return "\n".join([f"• {cmd}: {count}" for cmd, count in top_commands])
    
    def _format_duration(self, duration) -> str:
        """Format duration in human readable format"""
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}{StatsConstants.DURATION_DAYS} {hours}{StatsConstants.DURATION_HOURS} {minutes}{StatsConstants.DURATION_MINUTES}"
        elif hours > 0:
            return f"{hours}{StatsConstants.DURATION_HOURS} {minutes}{StatsConstants.DURATION_MINUTES}"
        else:
            return f"{minutes}{StatsConstants.DURATION_MINUTES} {seconds}{StatsConstants.DURATION_SECONDS}"
    
    def get_users_list(self, limit: int = BotConstants.DEFAULT_USERS_LIMIT) -> str:
        """Get formatted users list for admin"""
        users = self.get_all_users()[:limit]
        
        if not users:
            return StatsConstants.NO_USERS
        
        lines = [f"{StatsConstants.USERS_HEADER}\n"]
        
        for i, user in enumerate(users, 1):
            # Format user info
            name = self._format_user_name(user)
            username = f"@{user.username}" if user.username else "Без username"
            
            # Format last seen
            last_seen_str = self._format_last_seen(user.last_seen)
            
            lines.append(f"{i}. <b>{name}</b> ({username})")
            lines.append(f"   {StatsConstants.USER_ID} <code>{user.user_id}</code> | {StatsConstants.LAST_VISIT} {last_seen_str}")
            lines.append(f"   {StatsConstants.MESSAGES_COUNT} {user.message_count}")
            lines.append("")
        
        if len(self.users) > limit:
            lines.append(f"... та ще {len(self.users) - limit} користувачів")
        
        return "\n".join(lines)
    
    def _format_user_name(self, user: UserStats) -> str:
        """Format user name for display"""
        name_parts = []
        if user.first_name:
            name_parts.append(user.first_name)
        if user.last_name:
            name_parts.append(user.last_name)
        return " ".join(name_parts) if name_parts else "Без імені"
    
    def _format_last_seen(self, last_seen: str) -> str:
        """Format last seen timestamp for display"""
        try:
            last_seen_dt = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
            return last_seen_dt.strftime(StatsConstants.DATE_FORMAT)
        except:
            return "Невідомо"

# Global stats manager instance
stats_manager = StatsManager()
