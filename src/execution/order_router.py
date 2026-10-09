import logging
import uuid
from typing import Dict, Any
from src.api.kalshi_client import KalshiClient
from src.api.crypto_client import CryptoClient

logger = logging.getLogger(__name__)

class OrderRouter:
    def __init__(self, kalshi_client: KalshiClient, crypto_client: CryptoClient):
        self.kalshi = kalshi_client
        self.crypto = crypto_client

    def execute_kalshi_trade(self, ticker: str, side: str, confidence: float):
        """
        Translates an AI confidence score into a concrete Kalshi order.
        """
        logger.info(f"Routing Kalshi trade for {ticker}: {side} based on confidence {confidence}")

        if not self.kalshi.is_authenticated:
            logger.warning(f"Cannot execute Kalshi trade for {ticker}: Not authenticated")
            return

        limit_price = int(confidence * 100)
        quantity = 1
        client_order_id = str(uuid.uuid4())

        try:
             from kalshi_python import CreateOrderRequest

             req = CreateOrderRequest(
                 ticker=ticker,
                 action="buy",
                 side=side,
                 count=quantity,
                 type="limit",
                 yes_price=limit_price if side == "yes" else None,
                 no_price=limit_price if side == "no" else None,
                 client_order_id=client_order_id
             )

             response = self.kalshi.kalshi.create_order(req)
             logger.info(f"Successfully placed order for {ticker}: {response}")
             return response
        except Exception as e:
             logger.error(f"Failed to place Kalshi order for {ticker}: {e}")
             return None

    def execute_crypto_trade(self, symbol: str, signal: str, amount: float = 0.01):
        """
        Executes a basic market order on the configured crypto exchange.
        """
        logger.info(f"Routing crypto trade: {symbol} -> {signal}")

        if signal not in ["buy", "sell"]:
             logger.info(f"Signal is {signal}, taking no action.")
             return None

        if not self.crypto.is_authenticated:
             logger.warning(f"Cannot execute Crypto trade for {symbol}: Not authenticated")
             return None

        try:
             # Using CCXT's unified create_market_order method
             if signal == "buy":
                  response = self.crypto.exchange.create_market_buy_order(symbol, amount)
             else:
                  response = self.crypto.exchange.create_market_sell_order(symbol, amount)

             logger.info(f"Successfully executed crypto trade: {response.get('id', 'Unknown ID')}")
             return response
        except Exception as e:
             logger.error(f"Failed to execute crypto trade for {symbol}: {e}")
             return None
