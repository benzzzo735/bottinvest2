MARKERS = ["🟢", "🔵", "🟡", "🟣", "🟠", "🔴"]


def format_portfolio(assets, currency_positions) -> str:
    text = "💼 <b>Портфель</b>\n\n"

    total_assets_value = sum(a["value"] for a in assets)
    marker_index = 0

    for asset in assets:
        marker = MARKERS[marker_index % len(MARKERS)]
        marker_index += 1

        name = asset["name"]
        if asset["type"] == "etf":
            name = f"Фонд {name}"

        share = (
            asset["value"] / total_assets_value * 100
            if total_assets_value > 0 else 0
        )

        text += (
            f"{marker} <b>{name}</b>\n"
            f"Тикер: <code>{asset['ticker']}</code>\n"
            f"Количество: {asset['quantity']} шт.\n"
            f"Цена: {asset['price']:.2f} ₽\n"
            f"Общая стоимость: {asset['value']:.2f} ₽\n"
            f"Доля в портфеле: {share:.2f}%\n\n"
        )

    text += f"📊 <b>Инвестиции всего:</b> {total_assets_value:.2f} ₽\n\n"

    for pos, value in currency_positions:
        if value < 0:
            text += (
                "⚠️ <b>Заемные средства (маржинальная позиция)</b>\n"
                f"{pos.currency.upper()}: {value:.2f} ₽\n"
            )
        else:
            text += (
                "💰 <b>Денежные средства</b>\n"
                f"{pos.currency.upper()}: {value:.2f} ₽\n"
            )

    return text
