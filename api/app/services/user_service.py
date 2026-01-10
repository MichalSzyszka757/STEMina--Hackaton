from app.schemas.user import UserInDB, User, UserType

# Nasza udawana baza
# Hasło: tajnehaslo123
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$/P6XgLgNNxa6oVL8NuUPhg$YeOm7vdhbHOSht0NzlBqWvdLUZpv0cYZxQJ6ik34XEI",
        "disabled": False,
    }
}

def get_user_by_username(username: str) -> UserInDB | None:
    if username in fake_users_db:
        return UserInDB(**fake_users_db[username])
    return None

def create_user(user: User, type: UserType) -> UserInDB | None:
    return None