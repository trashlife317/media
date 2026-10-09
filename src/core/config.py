import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Kalshi Configuration
    KALSHI_EMAIL = os.getenv("KALSHI_EMAIL", "")
    KALSHI_PASSWORD = os.getenv("KALSHI_PASSWORD", "")
    KALSHI_ENV = os.getenv("KALSHI_ENV", "demo") # demo or prod

    # Generic Crypto Configuration (e.g., Binance)
    EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY", "")
    EXCHANGE_SECRET = os.getenv("EXCHANGE_SECRET", "")
    EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "binance")

    # AI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Risk Management
    MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "0.05")) # 5% of portfolio
    MAX_DRAWDOWN = float(os.getenv("MAX_DRAWDOWN", "0.10")) # 10% max daily drawdown

config = Config()
