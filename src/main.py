import time
import logging
from src.core.config import config
from src.core.risk_manager import RiskManager
from src.api.kalshi_client import KalshiClient
from src.api.crypto_client import CryptoClient
from src.ai.decision_engine import DecisionEngine
from src.execution.order_router import OrderRouter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Trading Bot Initialization...")

    try:
        # Pydantic Config already validated on import, but we can verify it's loaded
        logger.info(f"Loaded config for Kalshi Env: {config.KALSHI_ENV}, Exchange: {config.EXCHANGE_NAME}")

        kalshi = KalshiClient()
        kalshi.authenticate()

        crypto = CryptoClient()
        ai_engine = DecisionEngine()
        risk_manager = RiskManager()

        router = OrderRouter(kalshi, crypto, risk_manager)
    except Exception as e:
        logger.critical(f"Failed to initialize bot components. Shutting down. Error: {e}")
        return

    logger.info("Bot initialized and ready. Starting Event Loop.")

    consecutive_errors = 0
    max_consecutive_errors = 5

    try:
        while True:
            try:
                logger.info("--- Trading Loop Tick ---")

                # --- 1. Kalshi Pipeline ---
                target_kalshi_market = "KXINFL-24-DEC-31"
                kalshi_market_data = kalshi.get_market(target_kalshi_market)

                if kalshi_market_data:
                    kalshi_analysis = ai_engine.analyze_event(
                        kalshi_market_data,
                        news_context="Recent CPI report was unexpectedly high, inflation persists."
                    )

                    if kalshi_analysis.yes_confidence > 0.55:
                        router.execute_kalshi_trade(target_kalshi_market, "yes", kalshi_analysis.yes_confidence)
                    elif kalshi_analysis.no_confidence > 0.55:
                        router.execute_kalshi_trade(target_kalshi_market, "no", kalshi_analysis.no_confidence)

                # --- 2. Crypto Pipeline ---
                target_crypto_symbol = "BTC/USDT"
                crypto_ticker = crypto.fetch_ticker(target_crypto_symbol)
                recent_trades = crypto.fetch_recent_trades(target_crypto_symbol)

                if crypto_ticker and recent_trades:
                    current_price = crypto_ticker.get('last')
                    crypto_analysis = ai_engine.analyze_crypto_trend(target_crypto_symbol, current_price, recent_trades)

                    logger.info(f"AI Signal for {target_crypto_symbol}: {crypto_analysis.action.upper()} - {crypto_analysis.reasoning}")
                    if crypto_analysis.action != "hold":
                        router.execute_crypto_trade(target_crypto_symbol, crypto_analysis.action, current_price)

                consecutive_errors = 0 # Reset error count on successful loop

                logger.info("Tick complete. Sleeping...")
                time.sleep(5)
                # Loop runs continuously

            except Exception as loop_err:
                consecutive_errors += 1
                logger.error(f"Error during main loop tick: {loop_err}")
                if consecutive_errors >= max_consecutive_errors:
                    logger.critical("Max consecutive errors reached. Halting bot to prevent cascading failures.")
                    break
                time.sleep(10 * consecutive_errors) # Backoff loop time

    except KeyboardInterrupt:
        logger.info("Bot stopped cleanly by user.")
    except Exception as fatal_err:
        logger.critical(f"Unrecoverable fatal error in main loop: {fatal_err}")

if __name__ == "__main__":
    main()
