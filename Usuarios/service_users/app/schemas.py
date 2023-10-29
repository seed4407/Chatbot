def userEntity(User) -> dict:
    return {
        "id": str(User["_id"]),
        "name": User["name"],
        "username": User["username"],
        "password": User["password"],
        "email": User["email"],
        "admin": User["admin"],
        "phone_number": User["phone_number"],
        "ad": User["ad"],
    }


def usersEntity(Users) -> list:
    return [userEntity(User) for User in Users]