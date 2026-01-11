from enum import Enum

class PriceTier(str, Enum):
    BUDGET = "BUDGET"
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"

class LeadTime(str, Enum):
    ONE_WEEK = "week"
    TWO_WEEKS = "2week"
    THREE_WEEKS = "3week"

def get_days_from_lead_time(lead_time: str) -> int:
    """Funkcja pomocnicza zamieniająca enum na liczbę dni"""
    if lead_time == LeadTime.ONE_WEEK:
        return 7
    elif lead_time == LeadTime.TWO_WEEKS:
        return 14
    elif lead_time == LeadTime.THREE_WEEKS:
        return 21
    return 30