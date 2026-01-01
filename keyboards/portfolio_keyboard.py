from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def portfolio_select_keyboard(accounts):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text="📊 Все портфели",
            callback_data="portfolio:all"
        )
    )

    for account in accounts:
        keyboard.add(
            InlineKeyboardButton(
                text=f"💼 {account.name}",
                callback_data=f"portfolio:{account.id}"
            )
        )

    return keyboard
