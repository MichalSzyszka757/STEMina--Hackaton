from typing import List
from sqlalchemy.orm import Session
from app.models.provider import Provider


def create_provider(
        db: Session,
        name: str,
        payment: int,
        deadlines: int,
        location: str,
        starting_year: int,
        owner: str,
        description: str,
        specializations: List[str],
        rating: float = 0.0,  # Argument opcjonalny
        is_active: bool = True  # Argument opcjonalny
) -> Provider:
    """
    Funkcja tworząca profil dostawcy.
    """
    new_provider = Provider(
        name=name,
        payment=payment,
        deadlines=deadlines,
        location=location,
        starting_year=starting_year,
        owner=owner,
        description=description,
        specializations=specializations,
        rating=rating,
        is_active=is_active
    )

    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)

    return new_provider