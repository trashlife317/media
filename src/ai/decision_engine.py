import logging
from typing import Any, Literal
from openai import OpenAI
from pydantic import BaseModel, Field
from src.core.config import config

logger = logging.getLogger(__name__)

# --- Strict Pydantic Schemas for AI Responses ---
class KalshiAnalysis(BaseModel):
    yes_confidence: float = Field(..., ge=0.0, le=1.0, description="Probability of event resolving Yes")
    no_confidence: float = Field(..., ge=0.0, le=1.0, description="Probability of event resolving No")

class CryptoAnalysis(BaseModel):
    action: Literal["buy", "sell", "hold"] = Field(..., description="The trading action to take")
    reasoning: str = Field(..., description="Brief 1-sentence reasoning for the action")

class DecisionEngine:
    def __init__(self):
        logger.info("Initializing AI Decision Engine (OpenAI Structured Outputs)")
        self.api_key = config.OPENAI_API_KEY
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            logger.warning("OPENAI_API_KEY not found. AI Engine will run in mock mode.")

    def analyze_event(self, event_data: Any, news_context: str) -> KalshiAnalysis:
        if not self.client:
            return KalshiAnalysis(yes_confidence=0.60, no_confidence=0.40)

        ticker = getattr(event_data, 'ticker', str(event_data))
        title = getattr(event_data, 'title', 'Unknown Event Title')

        prompt = f"""
        You are an expert quantitative analyst trading event contracts.
        Analyze the following event contract and context, and determine the probability of it resolving 'Yes'.

        Event Ticker: {ticker}
        Event Title: {title}
        Current News Context: {news_context}
        """

        try:
            logger.info(f"Sending prompt to OpenAI for event: {ticker}")
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",  # Must use a model that supports strict structured outputs
                messages=[
                    {"role": "system", "content": "You are a quantitative AI trading system."},
                    {"role": "user", "content": prompt}
                ],
                response_format=KalshiAnalysis,
                temperature=0.2
            )

            parsed_result = response.choices[0].message.parsed
            logger.info(f"OpenAI analysis complete: {parsed_result}")
            return parsed_result

        except Exception as e:
            logger.error(f"Failed to analyze event with OpenAI: {e}")
            return KalshiAnalysis(yes_confidence=0.50, no_confidence=0.50)

    def analyze_crypto_trend(self, symbol: str, current_price: float, recent_trades: list) -> CryptoAnalysis:
        if not self.client:
            return CryptoAnalysis(action="hold", reasoning="Mock mode active.")

        prompt = f"""
        Analyze the current state of {symbol}.
        Current Price: {current_price}
        Recent Trades (Sample): {recent_trades[:5]}

        Based on this limited data and your general knowledge of the crypto market, should we buy, sell, or hold?
        """

        try:
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini-2024-07-18",
                messages=[{"role": "user", "content": prompt}],
                response_format=CryptoAnalysis,
                temperature=0.2
            )
            return response.choices[0].message.parsed
        except Exception as e:
            logger.error(f"Failed to analyze crypto trend: {e}")
            return CryptoAnalysis(action="hold", reasoning=f"Error occurred: {e}")
