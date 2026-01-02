# ================== HARD FIX ENUM (CRITICAL) ==================
import sys
import os

sys.path.insert(0, os.path.abspath("invest-python"))
import enum

_original_enum_call = enum.EnumMeta.__call__


def safe_enum_call(cls, value, *args, **kwargs):
    try:
        return _original_enum_call(cls, value, *args, **kwargs)
    except ValueError:
        # 🔥 неизвестное значение enum — игнорируем
        return None


enum.EnumMeta.__call__ = safe_enum_call
# =============================================================

from tinkoff.invest import Client
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import TELEGRAM_TOKEN, TINKOFF_TOKEN
from services.portfolio_service import PortfolioService


portfolio_service = PortfolioService()


async def portfolio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with Client(TINKOFF_TOKEN) as client:
            accounts = client.users.get_accounts().accounts

        if not accounts:
            await update.message.reply_text("❌ Счета не найдены")
            return

        account_id = accounts[0].id
        text = portfolio_service.build_portfolio_text(account_id)
        await update.message.reply_text(text)

    except Exception as e:
        await update.message.reply_text(
            "❌ Ошибка получения портфеля\n"
            f"{type(e).__name__}: {e}"
        )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("portfolio", portfolio_command))
    app.run_polling()


if __name__ == "__main__":
    main()
