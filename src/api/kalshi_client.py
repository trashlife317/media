import logging
from kalshi_python import Configuration, ApiClient, KalshiClient as KalshiSDKClient
from src.core.config import config

logger = logging.getLogger(__name__)

class KalshiClient:
    def __init__(self):
        env_url = "https://demo-api.kalshi.co/trade-api/v2" if config.KALSHI_ENV == 'demo' else "https://trading-api.kalshi.com/trade-api/v2"
        self.configuration = Configuration(host=env_url)
        self.api_client = ApiClient(self.configuration)

        # The main SDK client class which includes all the APIs
        self.kalshi = KalshiSDKClient(self.configuration)
        self.is_authenticated = False

    def authenticate(self):
        # Implementation of login/auth using credentials or private key
        logger.info("Authenticating with Kalshi...")
        if not config.KALSHI_EMAIL or not config.KALSHI_PASSWORD:
            logger.warning("Kalshi credentials not found in config. Kalshi client will be unauthenticated.")
            return False

        try:
            # Login to the Kalshi API. Note: Depending on SDK version, login method might vary.
            # Using standard username/password for demo/v2.
            login_response = self.kalshi.login(
                {"email": config.KALSHI_EMAIL, "password": config.KALSHI_PASSWORD}
            )

            # Usually the SDK manages the token after login, or we have to set it.
            # Let's set the access token if provided in response.
            if hasattr(login_response, 'member_id'):
                 logger.info(f"Successfully authenticated as {login_response.member_id}")
            self.is_authenticated = True
            return True
        except Exception as e:
            logger.error(f"Failed to authenticate with Kalshi: {e}")
            return False

    def get_market(self, ticker: str):
        try:
            response = self.kalshi.get_market(ticker)
            logger.info(f"Fetched market {ticker}")
            return response
        except Exception as e:
            logger.error(f"Failed to fetch market {ticker}: {e}")
            return None

    def get_balance(self):
        if not self.is_authenticated:
             logger.warning("Cannot fetch balance: Not authenticated")
             return None

        try:
             response = self.kalshi.get_balance()
             return response
        except Exception as e:
             logger.error(f"Failed to fetch balance: {e}")
             return None
