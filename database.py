"""
Database operations for X link moderation bot.
Handles SQLite database initialization and link tracking.
"""

import sqlite3
from datetime import datetime, timedelta, timezone
from typing import List, Optional
import threading


class Database:
    """Thread-safe SQLite database handler for link tracking."""

    def __init__(self, db_path: str = "bot_data.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self.local = threading.local()
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Get thread-local database connection."""
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(self.db_path)
            self.local.connection.row_factory = sqlite3.Row
        return self.local.connection

    def _init_db(self):
        """Create tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS link_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp DATETIME NOT NULL,
                link_url TEXT NOT NULL,
                chat_id INTEGER NOT NULL
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_timestamp
            ON link_history(user_id, timestamp)
        """)

        conn.commit()

    def add_link(self, user_id: int, link_url: str, chat_id: int):
        """Record a new X link posted by a user."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO link_history (user_id, timestamp, link_url, chat_id)
            VALUES (?, ?, ?, ?)
        """, (user_id, datetime.now(timezone.utc), link_url, chat_id))

        conn.commit()

    def get_user_links_last_week(self, user_id: int, chat_id: int) -> List[sqlite3.Row]:
        """Get all links posted by user in the last 7 days for a specific chat."""
        conn = self._get_connection()
        cursor = conn.cursor()

        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

        cursor.execute("""
            SELECT * FROM link_history
            WHERE user_id = ? AND chat_id = ? AND timestamp > ?
            ORDER BY timestamp DESC
        """, (user_id, chat_id, seven_days_ago))

        return cursor.fetchall()

    def count_user_links_last_week(self, user_id: int, chat_id: int) -> int:
        """Count number of links posted by user in last 7 days for a specific chat."""
        conn = self._get_connection()
        cursor = conn.cursor()

        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

        cursor.execute("""
            SELECT COUNT(*) as count FROM link_history
            WHERE user_id = ? AND chat_id = ? AND timestamp > ?
        """, (user_id, chat_id, seven_days_ago))

        result = cursor.fetchone()
        return result['count'] if result else 0

    def cleanup_old_links(self, days: int = 30):
        """Remove link history older than specified days."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        cursor.execute("""
            DELETE FROM link_history
            WHERE timestamp < ?
        """, (cutoff_date,))

        conn.commit()
        deleted = cursor.rowcount
        return deleted

    def close(self):
        """Close database connection."""
        if hasattr(self.local, 'connection'):
            self.local.connection.close()
