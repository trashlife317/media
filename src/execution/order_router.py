import logging
import uuid
from typing import Dict, Any
from src.api.kalshi_client import KalshiClient
from src.api.crypto_client import CryptoClient
from src.core.risk_manager import RiskManager

logger = logging.getLogger(__name__)

class OrderRouter:
    def __init__(self, kalshi_client: KalshiClient, crypto_client: CryptoClient, risk_manager: RiskManager):
        self.kalshi = kalshi_client
        self.crypto = crypto_client
        self.risk_manager = risk_manager

    def execute_kalshi_trade(self, ticker: str, side: str, confidence: float):
        if not self.kalshi.is_authenticated:
            logger.warning(f"Cannot execute Kalshi trade for {ticker}: Not authenticated")
            return

        try:
            # 1. Fetch live balance
            balance_cents = self.kalshi.get_balance()

            # 2. Risk Manager calculates safe size
            quantity = self.risk_manager.calculate_kalshi_size(balance_cents, confidence)

            if quantity <= 0:
                logger.info(f"Risk manager rejected trade or calculated size 0 for {ticker}")
                return

            limit_price = int(confidence * 100)
            client_order_id = str(uuid.uuid4())

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
            logger.info(f"Successfully placed order for {ticker}: {quantity} contracts at {limit_price}c")
            return response

        except Exception as e:
             logger.error(f"Failed to place Kalshi order for {ticker}: {e}")
             return None

    def execute_crypto_trade(self, symbol: str, signal: str, current_price: float):
        if signal not in ["buy", "sell"]:
             return None

        if not self.crypto.is_authenticated:
             logger.warning(f"Cannot execute Crypto trade for {symbol}: Not authenticated")
             return None

        try:
             # 1. Fetch live balance of base asset (e.g. USDT)
             balance = self.crypto.get_balance()

             # 2. Risk Manager calculates safe size
             amount = self.risk_manager.calculate_crypto_size(balance, current_price)

             if amount <= 0:
                 logger.info(f"Risk manager rejected crypto trade or calculated size 0 for {symbol}")
                 return None

             if signal == "buy":
                  response = self.crypto.exchange.create_market_buy_order(symbol, amount)
             else:
                  # If selling, you need the balance of the asset itself (e.g. BTC)
                  # For simplicity in this mock, we assume 'sell' sells the calculated amount.
                  response = self.crypto.exchange.create_market_sell_order(symbol, amount)

             logger.info(f"Successfully executed crypto trade: {response.get('id', 'Unknown ID')} for {amount} {symbol}")
             return response

        except Exception as e:
             logger.error(f"Failed to execute crypto trade for {symbol}: {e}")
             return None
