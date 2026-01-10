from app.schemas.client import ClientCreate
from app.schemas.provider import ProviderCreate

UserRegister = Union[ClientCreate, ProviderCreate]

@app.post("/users", status_code=201)
def register_user(user_data: UserRegister):
    # user_data będzie albo instancją ClientCreate, albo ProviderCreate
    
    # 1. Haszowanie hasła (pseudokod)
    # hashed_pw = hash(user_data.password)
    
    # 2. Zapis do bazy
    # Tutaj zapisujemy do tabeli Users.
    # Jeśli masz osobne tabele na profile, rozdzielasz dane tutaj.
    
    if user_data.role == "PROVIDER":
        return {"msg": f"Zarejestrowano firmę: {user_data.company_name}", "id": "new-uuid"}
    else:
        return {"msg": f"Zarejestrowano klienta: {user_data.first_name}", "id": "new-uuid"}