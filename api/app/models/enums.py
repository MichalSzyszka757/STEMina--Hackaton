# app/models/enums.py
from enum import Enum

class PriceTier(str, Enum):
    BUDGET = "BUDGET"
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"

class LeadTime(str, Enum):
    ONE_WEEK = "week"     # < 7 dni
    TWO_WEEKS = "2week"   # < 14 dni
    THREE_WEEKS = "3week" # < 21 dni