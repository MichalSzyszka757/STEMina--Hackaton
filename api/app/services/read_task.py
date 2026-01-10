from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Any


class TaskBudget(str, Enum):
    BUDGET = "BUDGET"
    STANDARD = "STANDARD"


class TaskCriteria(BaseModel):
    category: str
    budget: TaskBudget
    deadline: datetime
    distance: int


def process_task_criteria(criteria: TaskCriteria) -> Any:
    print(f"--- Logika biznesowa: Przetwarzanie kategorii {criteria.category} ---")

    return {
        "status": "success",
        "found_results": 5,
        "summary": f"Zlecenie {criteria.category} w budżecie {criteria.budget.value} do dnia {criteria.deadline.date()}",
        "is_urgent": (criteria.deadline - datetime.now()).days < 3
    }


# # --- TESTOWANIE DLA PRZYKŁADOWYCH DANYCH ---
# if __name__ == "__main__":
#     # Przykładowe dane wejściowe
#     test_data = {
#         "category": "Hydraulik",
#         "budget": "STANDARD",
#         "deadline": "2026-05-20T15:00:00",  # String zostanie zamieniony na datetime automatycznie
#         "distance": 15
#     }
#
#     try:
#         # Tworzenie obiektu struktury
#         criteria_obj = TaskCriteria(**test_data)
#
#         # Wywołanie metody
#         wynik = process_task_criteria(criteria_obj)
#
#         print("Dane wejściowe (obiekt):", criteria_obj)
#         print("Wynik metody:", wynik)
#
#     except Exception as e:
#         print(f"Błąd walidacji danych: {e}")