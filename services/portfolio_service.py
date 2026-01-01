from tinkoff.invest import Client
from config import TINKOFF_TOKEN
from services.instruments_cache import InstrumentsCache


TYPE_RU = {
    "share": "Акция",
    "bond": "Облигация",
    "etf": "Фонд",
    "currency": "Валюта",
}


TYPE_TITLE = {
    "share": "🔵 Акция",
    "bond": "🟠 Облигация",
    "etf": "🟢 Фонд",
    "currency": "💱 Валюта",
}


class PortfolioService:
    def __init__(self):
        self.cache = InstrumentsCache()
        self.cache.load()

    def build_portfolio_text(self, account_id: str) -> str:
        with Client(TINKOFF_TOKEN) as client:
            portfolio = client.operations.get_portfolio(account_id=account_id)

        positions = []
        total_assets = 0.0
        margin_rub = 0.0

        for pos in portfolio.positions:
            info = self.cache.get(pos.instrument_uid)

            instrument_type = info.get("type", "instrument")
            type_ru = TYPE_RU.get(instrument_type, "Инструмент")
            title = TYPE_TITLE.get(instrument_type, "⚪ Инструмент")

            name = info.get("name", "")
            ticker = info.get("ticker", "—")

            qty = int(pos.quantity.units)
            price = pos.current_price.units + pos.current_price.nano / 1e9
            value = qty * price

            if qty < 0:
                margin_rub += abs(value)
                continue

            total_assets += value

            positions.append({
                "title": title,
                "name": name,
                "ticker": ticker,
                "type_ru": type_ru,
                "qty": qty,
                "price": price,
                "value": value,
            })

        text = ["📦 Портфель\n"]

        for p in positions:
            share = (p["value"] / total_assets * 100) if total_assets else 0

            text.append(
                f"{p['title']} {p['name']}\n"
                f"Тикер: {p['ticker']}\n"
                f"Тип: {p['type_ru']}\n"
                f"Количество: {p['qty']}\n"
                f"Цена: {p['price']:,.2f} ₽\n"
                f"Стоимость: {p['value']:,.2f} ₽\n"
                f"Доля в портфеле: {share:.2f}%\n"
            )

        if margin_rub > 0:
            text.append(
                "⚠️ Маржинальная задолженность\n"
                f"RUB — {margin_rub:,.2f} ₽\n"
            )

        total = total_assets - margin_rub
        text.append(f"📊 Итого: {total:,.2f} ₽")

        return "\n".join(text)
