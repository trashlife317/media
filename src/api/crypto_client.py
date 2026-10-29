import ccxt
import logging
from src.core.config import config
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class CryptoClient:
    def __init__(self):
        try:
            exchange_class = getattr(ccxt, config.EXCHANGE_NAME.lower())

            self.exchange = exchange_class({
                'apiKey': config.EXCHANGE_API_KEY,
                'secret': config.EXCHANGE_SECRET,
                'enableRateLimit': True, # CCXT's built in rate limiter
            })

            if config.EXCHANGE_API_KEY and hasattr(self.exchange, 'set_sandbox_mode'):
                self.exchange.set_sandbox_mode(True)

            self.is_authenticated = bool(config.EXCHANGE_API_KEY and config.EXCHANGE_SECRET)

            if not self.is_authenticated:
                logger.warning(f"Crypto credentials not found. {config.EXCHANGE_NAME} client is read-only.")

        except AttributeError:
             logger.error(f"Exchange {config.EXCHANGE_NAME} not found in CCXT.")
             self.exchange = None
             self.is_authenticated = False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def fetch_ticker(self, symbol: str):
        if not self.exchange: return None
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            raise e

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def fetch_recent_trades(self, symbol: str, limit: int = 10):
        if not self.exchange: return []
        try:
             trades = self.exchange.fetch_trades(symbol, limit=limit)
             return [{"price": t['price'], "side": t['side']} for t in trades]
        except Exception as e:
             logger.error(f"Error fetching trades for {symbol}: {e}")
             raise e

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def get_balance(self, asset: str = config.BASE_CURRENCY) -> float:
         """Fetches the available free balance for a specific asset (e.g., USDT)"""
         if not self.is_authenticated or not self.exchange:
             return 0.0
         try:
             balance = self.exchange.fetch_balance()
             return float(balance.get(asset, {}).get('free', 0.0))
         except Exception as e:
             logger.error(f"Error fetching balance for {asset}: {e}")
             raise e
