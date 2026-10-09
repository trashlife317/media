import time
import logging
from src.api.kalshi_client import KalshiClient
from src.api.crypto_client import CryptoClient
from src.ai.decision_engine import DecisionEngine
from src.execution.order_router import OrderRouter

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Trading Bot Initialization...")

    # 1. Initialize API Clients
    kalshi = KalshiClient()
    # Kalshi client authentication using standard email and password.
    # It will use the configuration stored in `.env`
    # Warning: Without correct auth credentials, orders will fail
    kalshi.authenticate()

    crypto = CryptoClient()

    # 2. Initialize AI Engine
    ai_engine = DecisionEngine()

    # 3. Initialize Execution Router
    router = OrderRouter(kalshi, crypto)

    logger.info("Bot initialized and ready.")

    # 4. Main Event Loop (Simplified)
    try:
        while True:
            logger.info("--- Trading Loop Tick ---")

            # Example Kalshi Workflow
            target_market = "KXINFL-24-DEC-31" # Example ticker
            market_data = kalshi.get_market(target_market)

            if market_data:
                # Get AI analysis
                analysis = ai_engine.analyze_event(market_data, news_context="Recent CPI report was high.")

                # Make decision
                if analysis['yes_confidence'] > 0.55:
                    router.execute_kalshi_trade(target_market, "yes", analysis['yes_confidence'])

            # Sleep to prevent rate limits
            time.sleep(10)
            break # Break out of loop immediately for testing

    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}")

if __name__ == "__main__":
    main()
