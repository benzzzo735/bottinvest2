from decimal import Decimal
from dataclasses import dataclass


@dataclass
class PortfolioAsset:
    figi: str
    ticker: str
    name: str
    quantity: Decimal
    price: Decimal | None
    currency: str
    value: Decimal | None
    asset_type: str
    account_id: str

    @property
    def is_currency(self) -> bool:
        return self.asset_type == "currency"
