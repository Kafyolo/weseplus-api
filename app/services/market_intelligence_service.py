import random
from datetime import datetime

class MarketIntelligenceService:
    def get_market_outlook(self):
        # ELITE VETERAN NOTE: In a full production env, this would call 
        # the EWURA public notices or a Tanzanian news API.
        # We then pipe that text to Gemini PRO to get the "Insight".
        
        current_prices = {
            "Dar es Salaam": 3254,
            "Arusha": 3310,
            "Mwanza": 3350,
            "Dodoma": 3290
        }
        
        outlooks = [
            "Stability expected. Prices likely to remain unchanged for the next 14 days due to stable global crude inventory.",
            "Upward pressure detected. Anticipate a 2-3% increase in the next price cycle based on recent EWURA cap-price trends.",
            "Market optimism. Potential price drop in mid-May as supply chain bottlenecks in Dar Port are resolving."
        ]
        
        return {
            "average_price": 3254,
            "currency": "TZS",
            "trend": random.choice(["STABLE", "UPWARD", "DOWNWARD"]),
            "intelligence_note": random.choice(outlooks),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "source": "WesePlus Gemini Intelligence"
        }

market_intelligence = MarketIntelligenceService()
