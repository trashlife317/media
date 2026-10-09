import ccxt
import logging
from src.core.config import config

logger = logging.getLogger(__name__)

class CryptoClient:
    def __init__(self):
        exchange_class = getattr(ccxt, config.EXCHANGE_NAME)
        self.exchange = exchange_class({
            'apiKey': config.EXCHANGE_API_KEY,
            'secret': config.EXCHANGE_SECRET,
            'enableRateLimit': True,
        })
        # Use testnet if available
        self.exchange.set_sandbox_mode(True)

    def fetch_ticker(self, symbol: str):
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            return None
