from tinkoff.invest import Client
from config import TINKOFF_TOKEN


class TinkoffClient:
    def __init__(self):
        self.token = TINKOFF_TOKEN

    def get_accounts(self):
        with Client(self.token) as client:
            return client.users.get_accounts().accounts

    def get_portfolio(self, account_id: str):
        with Client(self.token) as client:
            return client.operations.get_portfolio(account_id=account_id)

    def get_withdraw_limits(self, account_id: str):
        with Client(self.token) as client:
            return client.operations.get_withdraw_limits(account_id=account_id)

    def get_instrument_by_uid(self, uid: str):
        with Client(self.token) as client:
            try:
                return client.instruments.get_instrument_by(uid=uid).instrument
            except Exception:
                return None
