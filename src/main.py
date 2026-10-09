import time
import logging
from src.api.kalshi_client import KalshiClient
from src.api.crypto_client import CryptoClient
from src.ai.decision_engine import DecisionEngine
from src.execution.order_router import OrderRouter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Trading Bot Initialization...")

    kalshi = KalshiClient()
    kalshi.authenticate()
    crypto = CryptoClient()

    ai_engine = DecisionEngine()
    router = OrderRouter(kalshi, crypto)

    logger.info("Bot initialized and ready. Starting Event Loop.")

    try:
        while True:
            logger.info("--- Trading Loop Tick ---")

            # --- 1. Kalshi Pipeline ---
            target_kalshi_market = "KXINFL-24-DEC-31"
            kalshi_market_data = kalshi.get_market(target_kalshi_market)

            if kalshi_market_data:
                kalshi_analysis = ai_engine.analyze_event(
                    kalshi_market_data,
                    news_context="Recent CPI report was unexpectedly high, inflation persists."
                )

                if kalshi_analysis.get('yes_confidence', 0) > 0.55:
                    router.execute_kalshi_trade(target_kalshi_market, "yes", kalshi_analysis['yes_confidence'])
                elif kalshi_analysis.get('no_confidence', 0) > 0.55:
                    router.execute_kalshi_trade(target_kalshi_market, "no", kalshi_analysis['no_confidence'])

            # --- 2. Crypto Pipeline ---
            target_crypto_symbol = "BTC/USDT"
            crypto_ticker = crypto.fetch_ticker(target_crypto_symbol)
            recent_trades = crypto.fetch_recent_trades(target_crypto_symbol)

            if crypto_ticker and recent_trades:
                current_price = crypto_ticker.get('last')
                crypto_signal = ai_engine.analyze_crypto_trend(target_crypto_symbol, current_price, recent_trades)
                router.execute_crypto_trade(target_crypto_symbol, crypto_signal)

            # Prevent immediate loop in demo to save rate limits
            logger.info("Tick complete. Sleeping...")
            time.sleep(5)
            break # Remove break for infinite loop in production

    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}")

if __name__ == "__main__":
    main()
