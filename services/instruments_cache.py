from tinkoff.invest import Client, InstrumentStatus
from config import TINKOFF_TOKEN


class InstrumentsCache:
    def __init__(self):
        self._cache = {}

    def load(self):
        with Client(TINKOFF_TOKEN) as client:
            self._load_shares(client)
            self._load_etfs(client)
            self._load_bonds(client)

    def _save(self, instrument, instrument_type: str):
        self._cache[instrument.uid] = {
            "ticker": instrument.ticker,
            "name": instrument.name,
            "type": instrument_type,
        }

    def _load_shares(self, client):
        response = client.instruments.shares(
            instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE
        )
        for item in response.instruments:
            self._save(item, "share")

    def _load_etfs(self, client):
        response = client.instruments.etfs(
            instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE
        )
        for item in response.instruments:
            self._save(item, "etf")

    def _load_bonds(self, client):
        response = client.instruments.bonds(
            instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE
        )
        for item in response.instruments:
            self._save(item, "bond")

    def get(self, instrument_uid: str) -> dict:
        return self._cache.get(instrument_uid, {})
