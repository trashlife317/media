import logging
from kalshi_python import Configuration, ApiClient, KalshiClient as KalshiSDKClient
from src.core.config import config
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class KalshiClient:
    def __init__(self):
        env_url = "https://demo-api.kalshi.co/trade-api/v2" if config.KALSHI_ENV == 'demo' else "https://trading-api.kalshi.com/trade-api/v2"
        self.configuration = Configuration(host=env_url)
        self.api_client = ApiClient(self.configuration)

        self.kalshi = KalshiSDKClient(self.configuration)
        self.is_authenticated = False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def authenticate(self):
        logger.info("Authenticating with Kalshi...")
        if not config.KALSHI_EMAIL or not config.KALSHI_PASSWORD:
            logger.warning("Kalshi credentials not found in config. Kalshi client will be unauthenticated.")
            return False

        try:
            login_response = self.kalshi.login(
                {"email": config.KALSHI_EMAIL, "password": config.KALSHI_PASSWORD}
            )
            self.is_authenticated = True
            logger.info("Successfully authenticated with Kalshi.")
            return True
        except Exception as e:
            logger.error(f"Failed to authenticate with Kalshi: {e}")
            raise e # Raise to trigger tenacity retry

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
    def get_market(self, ticker: str):
        try:
            response = self.kalshi.get_market(ticker)
            return response
        except Exception as e:
            logger.error(f"Failed to fetch market {ticker}: {e}")
            raise e

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=5))
    def get_balance(self) -> int:
        if not self.is_authenticated:
             return 0
        try:
             response = self.kalshi.get_balance()
             # Returns available balance in cents
             return getattr(response, 'balance', 0)
        except Exception as e:
             logger.error(f"Failed to fetch balance: {e}")
             raise e
