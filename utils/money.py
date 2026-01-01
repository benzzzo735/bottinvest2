def money_to_float(money) -> float:
    if money is None:
        return 0.0
    return money.units + money.nano / 1_000_000_000
