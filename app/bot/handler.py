import json
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    CallbackContext,
    ExtBot,
    filters,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from .app import application
from loguru import logger
from ..model import get_channel

async def on_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != constants.ChatType.SUPERGROUP and update.effective_chat.type != constants.ChatType.GROUP:
        return
    group_id = update.effective_chat.id
    channel = get_channel(group_id)
    if not channel:
        return
    for ws in channel:
        if ws.state == "connecting":
            continue
        await ws.send_json({"type": "text", "data": update.message.text})


async def on_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理用户发送的id"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    await update.message.reply_text(f"你的id是:{user_id}\n 群组id是:{chat_id}")

logger.info("handler bot")
application.add_handler(MessageHandler(filters.TEXT, on_text_message, False))
application.add_handler(CommandHandler("id", on_id))

from .error_handler import error_handler

application.add_error_handler(error_handler)
