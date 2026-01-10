from sqlalchemy.orm import Session
from app.models.client import Client


def create_client(
        db: Session,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        address: str,
        profile_picture: str = None  # Argument opcjonalny
) -> Client:
    """
    Funkcja rejestrująca nowego klienta.
    """
    new_client = Client(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        address=address,
        profile_picture=profile_picture
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client