import logging
from src.core.config import config

logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self):
        self.max_position_size = config.MAX_POSITION_SIZE
        self.max_drawdown = config.MAX_DRAWDOWN

        # In a real bot, you'd fetch this from a DB tracking daily PnL
        self.current_daily_drawdown = 0.0

    def check_global_risk(self) -> bool:
        """
        Checks if global trading should be halted (e.g., max drawdown reached).
        """
        if self.current_daily_drawdown >= self.max_drawdown:
            logger.critical(f"RISK LIMIT REACHED: Daily drawdown ({self.current_daily_drawdown}) exceeds max ({self.max_drawdown}). Halting trading.")
            return False
        return True

    def calculate_kalshi_size(self, balance_cents: int, confidence: float) -> int:
        """
        Calculates how many Kalshi contracts to buy based on available balance and AI confidence.
        """
        if balance_cents <= 0 or not self.check_global_risk():
            return 0

        # Allocate up to max_position_size of total balance
        max_allocation_cents = balance_cents * self.max_position_size

        # Scale the allocation by confidence (Kelly Criterion lite)
        # e.g., 90% confidence gets full max allocation, 51% gets very little
        scaled_allocation = max_allocation_cents * confidence

        # Kalshi contracts cost money based on limit price. For simplicity in calculating *count*,
        # if max price is 100c, the safest assumption is 100c per contract at worst.
        quantity = int(scaled_allocation // 100)

        if quantity == 0:
            logger.warning(f"Calculated Kalshi size is 0 (Balance: {balance_cents}c, Conf: {confidence})")

        return quantity

    def calculate_crypto_size(self, balance: float, current_price: float) -> float:
        """
        Calculates trade amount for crypto asset based on available balance.
        """
        if balance <= 0 or not self.check_global_risk():
            return 0.0

        # Standard percentage risk allocation
        allocation = balance * self.max_position_size
        quantity = allocation / current_price

        return round(quantity, 4) # Most exchanges limit precision
