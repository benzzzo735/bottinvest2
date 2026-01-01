from tinkoff.invest import MoneyValue, Quotation


def quotation_to_float(q: Quotation) -> float:
    return q.units + q.nano / 1_000_000_000


def money_to_float(m: MoneyValue) -> float:
    return m.units + m.nano / 1_000_000_000
