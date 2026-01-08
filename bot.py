"""
Telegram bot for moderating X/Twitter links in group chats.
Enforces rate limits and context requirements.
"""

import re
import logging
import os
from typing import List, Optional
from telegram import Update, Message, Chat
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ChatMemberHandler,
    ContextTypes,
    filters
)
from telegram.error import TelegramError
import asyncio

from database import Database
from config import Config


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class XLinkModerator:
    """Main bot class for X link moderation."""

    # Patterns to detect X/Twitter links
    X_LINK_PATTERNS = [
        r'https?://(?:www\.)?x\.com/\S+(?<![.,?!:;])',
        r'https?://(?:www\.)?twitter\.com/\S+(?<![.,?!:;])',
        r'https?://(?:www\.)?vxtwitter\.com/\S+(?<![.,?!:;])',
        r'https?://(?:www\.)?fxtwitter\.com/\S+(?<![.,?!:;])',
        r'https?://(?:www\.)?fixupx\.com/\S+(?<![.,?!:;])',
    ]

    def __init__(self, config: Config, database: Database):
        """Initialize the bot with configuration and database."""
        self.config = config
        self.db = database
        self.x_link_regex = re.compile('|'.join(self.X_LINK_PATTERNS), re.IGNORECASE)

    def extract_x_links(self, text: str) -> List[str]:
        """Extract all X/Twitter links from text."""
        if not text:
            return []
        return self.x_link_regex.findall(text)

    def get_text_without_links(self, text: str) -> str:
        """Remove all URLs from text to get context."""
        if not text:
            return ""
        # Remove all URLs (not just X links)
        url_pattern = r'https?://\S+'
        text_without_urls = re.sub(url_pattern, '', text)
        # Clean up extra whitespace
        return ' '.join(text_without_urls.split())

    async def check_bot_permissions(self, chat: Chat, bot_id: int) -> bool:
        """Check if bot has admin permissions to delete messages."""
        try:
            member = await chat.get_member(bot_id)
            return member.can_delete_messages if hasattr(member, 'can_delete_messages') else False
        except TelegramError as e:
            logger.error(f"Error checking bot permissions: {e}")
            return False

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages and check for X links."""
        message = update.message
        if not message or not message.text:
            return

        # Only moderate group chats, not DMs
        if message.chat.type not in ['group', 'supergroup']:
            return

        chat_id = message.chat.id
        user_id = message.from_user.id
        text = message.text

        # Extract X links
        x_links = self.extract_x_links(text)
        if not x_links:
            return

        logger.info(f"Found {len(x_links)} X link(s) from user {user_id} in chat {chat_id}")

        # Check if bot has permission to delete messages
        bot_id = (await context.bot.get_me()).id
        has_permission = await self.check_bot_permissions(message.chat, bot_id)

        if not has_permission:
            logger.warning(f"Bot lacks delete permissions in chat {chat_id}")
            # Send helpful setup instructions
            await message.reply_text(
                "⚠️ **I need admin permissions to moderate links!**\n\n"
                "**Quick fix:**\n"
                "1. Tap the group name at the top\n"
                "2. Tap 'Edit' or Settings icon\n"
                "3. Tap 'Administrators'\n"
                "4. Add me as an administrator\n"
                "5. Enable 'Delete Messages' ✓\n\n"
                "After setup, type /diagnose to verify!",
                parse_mode='Markdown'
            )
            return

        # Check context requirement
        if self.config.require_context:
            context_text = self.get_text_without_links(text)
            if len(context_text) < self.config.min_context_length:
                await self._handle_no_context_violation(message)
                return

        # Check rate limit
        current_count = self.db.count_user_links_last_week(user_id, chat_id)
        
        links_to_process = x_links if self.config.count_per_link else [x_links[0]]
        new_count = len(links_to_process)

        if current_count + new_count > self.config.max_links_per_week:
            await self._handle_rate_limit_violation(message, user_id)
            return

        # Links are allowed - record them
        for link in links_to_process:
            self.db.add_link(user_id, link, chat_id)
            
        remaining = self.config.max_links_per_week - (current_count + new_count)

        # Warn if approaching limit
        if remaining <= 1 and remaining >= 0:
            warning_msg = self.config.approaching_limit_message.format(remaining=remaining)
            warning = await message.reply_text(warning_msg)
            # Delete warning after 10 seconds
            await asyncio.sleep(10)
            try:
                await warning.delete()
            except TelegramError:
                pass

        logger.info(f"User {user_id} posted {new_count} link(s). {remaining} remaining this week.")

    async def _handle_rate_limit_violation(self, message: Message, user_id: int):
        """Handle rate limit violation."""
        logger.info(f"Rate limit violation by user {user_id}")

        # Delete the message
        try:
            await message.delete()
        except TelegramError as e:
            logger.error(f"Failed to delete message: {e}")
            return

        # Send warning
        warning_text = self.config.rate_limit_message.format(
            max=self.config.max_links_per_week
        )
        warning = await message.chat.send_message(
            f"{message.from_user.mention_html()}: {warning_text}",
            parse_mode='HTML'
        )

        # Delete warning after 10 seconds
        await asyncio.sleep(10)
        try:
            await warning.delete()
        except TelegramError:
            pass

    async def _handle_no_context_violation(self, message: Message):
        """Handle missing context violation."""
        logger.info(f"No context violation by user {message.from_user.id}")

        # Delete the message
        try:
            await message.delete()
        except TelegramError as e:
            logger.error(f"Failed to delete message: {e}")
            return

        # Send warning
        warning_text = self.config.no_context_message.format(
            min=self.config.min_context_length
        )
        warning = await message.chat.send_message(
            f"{message.from_user.mention_html()}: {warning_text}",
            parse_mode='HTML'
        )

        # Delete warning after 10 seconds
        await asyncio.sleep(10)
        try:
            await warning.delete()
        except TelegramError:
            pass

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "👋 X Link Moderator Bot\n\n"
            f"Rules:\n"
            f"• Max {self.config.max_links_per_week} X links per week\n"
            f"• Links must have {self.config.min_context_length}+ characters of context\n\n"
            "Make me an admin with 'Delete Messages' permission to activate moderation."
        )

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command - show user's current stats."""
        if update.message.chat.type not in ['group', 'supergroup']:
            await update.message.reply_text("This command only works in group chats.")
            return

        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        count = self.db.count_user_links_last_week(user_id, chat_id)
        remaining = max(0, self.config.max_links_per_week - count)

        await update.message.reply_text(
            f"📊 Your Stats:\n"
            f"• Links posted this week: {count}/{self.config.max_links_per_week}\n"
            f"• Remaining: {remaining}"
        )

    async def diagnose_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /diagnose command - check if bot is configured correctly."""
        chat = update.message.chat

        # Check if it's a group
        if chat.type not in ['group', 'supergroup']:
            await update.message.reply_text(
                "❌ This bot only works in groups!\n\n"
                "Please add me to a group first."
            )
            return

        report = "🔍 **Diagnostic Report**\n\n"

        # Check bot permissions
        try:
            bot_id = (await context.bot.get_me()).id
            member = await chat.get_member(bot_id)

            if member.status in ['administrator']:
                if hasattr(member, 'can_delete_messages') and member.can_delete_messages:
                    report += "✅ Bot is admin with delete permissions\n"
                else:
                    report += "❌ Bot is admin but **CANNOT delete messages**\n"
                    report += "   **Fix:** Give bot 'Delete Messages' permission\n"
                    report += "   1. Tap group name → Edit → Administrators\n"
                    report += "   2. Tap the bot → Enable 'Delete Messages'\n"
            else:
                report += "❌ Bot is **NOT an administrator**\n"
                report += "   **Fix:** Make the bot an admin\n"
                report += "   1. Tap group name → Edit → Administrators\n"
                report += "   2. Tap 'Add Administrator' → Select the bot\n"
                report += "   3. Enable 'Delete Messages' permission\n"
        except TelegramError as e:
            report += f"❌ Could not check permissions: {e}\n"

        # Check database
        try:
            test_count = self.db.count_user_links_last_week(update.message.from_user.id, chat.id)
            report += "✅ Database is working\n"
        except Exception as e:
            report += f"❌ Database error: {e}\n"

        # Show current settings
        report += f"\n⚙️ **Current Settings:**\n"
        report += f"• Max links per week: {self.config.max_links_per_week}\n"
        report += f"• Context required: {'Yes' if self.config.require_context else 'No'}\n"
        if self.config.require_context:
            report += f"• Min context length: {self.config.min_context_length} chars\n"
        report += f"• Count each link: {'Yes' if self.config.count_per_link else 'No (one per message)'}\n"

        # Test link detection
        report += f"\n🧪 **Test Link Detection:**\n"
        report += "Try posting this test link with context:\n"
        report += "`This is interesting: https://x.com/test/status/123`\n"

        await update.message.reply_text(report, parse_mode='Markdown')

    async def my_chat_member_updated(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle bot being added to or removed from a group."""
        status_change = update.my_chat_member
        old_status = status_change.old_chat_member.status
        new_status = status_change.new_chat_member.status

        # Bot was added to group
        if old_status not in ['member', 'administrator'] and new_status in ['member', 'administrator']:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    "👋 **Thanks for adding X-Gate!**\n\n"
                    "**Quick Setup (30 seconds):**\n"
                    "1. Make me an admin\n"
                    "2. Enable 'Delete Messages' permission\n"
                    "3. Done! I'll start moderating X links\n\n"
                    "**Commands:**\n"
                    "• /start - View rules\n"
                    "• /stats - Check your usage\n"
                    "• /diagnose - Test configuration\n\n"
                    "**Default Rules:**\n"
                    f"• Max {self.config.max_links_per_week} X links per week per user\n"
                    f"• Links must have {self.config.min_context_length}+ characters of context\n\n"
                    "Type /diagnose to verify I'm set up correctly!"
                ),
                parse_mode='Markdown'
            )


def main():
    """Main function to run the bot."""
    try:
        # Load environment variables from .env file if it exists
        from dotenv import load_dotenv
        load_dotenv()

        # Load configuration
        config = Config()
        logger.info("Configuration loaded successfully")

        # Initialize database (support env variable for Railway)
        db_path = os.environ.get('DB_PATH', 'bot_data.db')
        db = Database(db_path)
        logger.info(f"Database initialized successfully at {db_path}")

        # Clean up old links on startup
        deleted = db.cleanup_old_links(days=30)
        if deleted > 0:
            logger.info(f"Cleaned up {deleted} old link records")

        # Initialize bot
        moderator = XLinkModerator(config, db)

        # Create application
        application = Application.builder().token(config.bot_token).build()

        # Add handlers
        application.add_handler(CommandHandler("start", moderator.start_command))
        application.add_handler(CommandHandler("stats", moderator.stats_command))
        application.add_handler(CommandHandler("diagnose", moderator.diagnose_command))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, moderator.handle_message)
        )
        # Handle bot being added to groups
        application.add_handler(ChatMemberHandler(moderator.my_chat_member_updated, ChatMemberHandler.MY_CHAT_MEMBER))

        logger.info("Bot started successfully. Press Ctrl+C to stop.")

        # Run the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
    except ValueError as e:
        logger.error(f"Configuration validation error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)


if __name__ == '__main__':
    main()
