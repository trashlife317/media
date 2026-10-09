import logging
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from src.core.config import config

logger = logging.getLogger(__name__)

class DecisionEngine:
    def __init__(self):
        logger.info("Initializing AI Decision Engine (OpenAI)")
        self.api_key = config.OPENAI_API_KEY
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            logger.warning("OPENAI_API_KEY not found. AI Engine will run in mock mode.")

    def analyze_event(self, event_data: Any, news_context: str) -> Dict[str, float]:
        """
        Analyzes an event (e.g., a Kalshi market) using an LLM.
        Returns a dictionary with confidence scores for 'yes' and 'no'.
        """
        if not self.client:
            logger.info(f"[MOCK AI] Analyzing event data: {getattr(event_data, 'ticker', 'unknown')}")
            return {"yes_confidence": 0.60, "no_confidence": 0.40}

        ticker = getattr(event_data, 'ticker', str(event_data))
        title = getattr(event_data, 'title', 'Unknown Event Title')

        prompt = f"""
        You are an expert financial quantitative analyst trading event contracts.
        Analyze the following event contract and context, and determine the probability of it resolving 'Yes'.

        Event Ticker: {ticker}
        Event Title: {title}
        Current News Context: {news_context}

        Provide your analysis in strictly valid JSON format with no markdown formatting.
        Return ONLY a JSON object with two keys: "yes_confidence" and "no_confidence", representing floats between 0.0 and 1.0 that sum to 1.0.

        Example output:
        {{"yes_confidence": 0.75, "no_confidence": 0.25}}
        """

        try:
            logger.info(f"Sending prompt to OpenAI for event: {ticker}")
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Can use a smaller/faster model like gpt-4o-mini depending on latency needs
                messages=[
                    {"role": "system", "content": "You are a quantitative AI trading system."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" },
                temperature=0.2 # Low temperature for more deterministic/logical outputs
            )

            content = response.choices[0].message.content
            if content:
                 result = json.loads(content)
                 logger.info(f"OpenAI analysis complete: {result}")
                 return result
            else:
                 raise ValueError("Empty response from OpenAI")

        except Exception as e:
            logger.error(f"Failed to analyze event with OpenAI: {e}")
            # Fallback to neutral
            return {"yes_confidence": 0.50, "no_confidence": 0.50}

    def analyze_crypto_trend(self, symbol: str, current_price: float, recent_trades: list) -> str:
        """
        Analyzes numerical price data to predict trend.
        Could use an LLM for sentiment/basic quant or a dedicated Time-Series ML model.
        Here we implement a basic LLM prompt for demonstration.
        """
        if not self.client:
            logger.info(f"[MOCK AI] Analyzing crypto trend for {symbol}")
            return "hold"

        prompt = f"""
        Analyze the current state of {symbol}.
        Current Price: {current_price}
        Recent Trades (Sample): {recent_trades[:5]}

        Based on this limited data and your general knowledge of the crypto market, should we buy, sell, or hold?
        Return ONLY a JSON object with the key "action" set to "buy", "sell", or "hold".
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            content = response.choices[0].message.content
            if content:
                 result = json.loads(content)
                 return result.get("action", "hold").lower()
            return "hold"
        except Exception as e:
            logger.error(f"Failed to analyze crypto trend: {e}")
            return "hold"
