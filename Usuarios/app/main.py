import logging

from bson.errors import InvalidId
from bson.objectid import ObjectId
from fastapi import FastAPI, status, HTTPException, Body
from pydantic import BaseModel, Field
from pymongo import MongoClient
from typing import Optional, Annotated
from bson.objectid import ObjectId
from bson.errors import InvalidId
from app.schemas import userEntity, usersEntity
from passlib.hash import sha256_crypt
from app.events import Emit

app = FastAPI(title=" User APIREST FastAPI & MongoDB", version="0.6.3")

mongodb_client = MongoClient("tarea_u4_service_users_mongodb", 27017)


class User(BaseModel):
    id: Optional[str]  # = Field(default=None)
    name: str  # = Field(examples=["Juan"])
    username: str  # = Field(examples=["juan1010"])
    password: str  # = Field(examples=["password123"])
    email: Optional[str]  # = Field(default=None, examples=["juan@gmail.com"])
    admin: Optional[bool]  # = Field(default=None, examples=["True"])
    phone_number: Optional[int]  # = Field(default=None, examples=["123456789"])
    token: Optional[str] = Field(default="", examples=[""])

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Juan",
                "username": "juan123",
                "password": "asdsad123",
                "email": "email@email.com",
                "admin": True,
                "phone_number": 1234567890,
                "token": "1234567890abcdef"
            }
        }


class UserUpdate(BaseModel):
    name: Optional[str]  # = Field(examples=["Juan"])
    username: Optional[str]  # = Field(examples=["juan1010"])
    password: Optional[str]  # = Field(examples=["password123"])
    email: Optional[str]  # = Field(default=None, examples=["juan@gmail.com"])
    admin: Optional[bool]  # = Field(default=None, examples=["True"])
    phone_number: Optional[int]  # = Field(default=None, examples=["123456789"])
    token: Optional[str] = Field(default="", examples=[""])

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Juan",
                "username": "juan123",
                "password": "asdsad123",
                "email": "email@email.com",
                "admin": True,
                "phone_number": 1234567890,
                "token": "1234567890abcdef"
            }
        }


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)

# logging.basicConfig(level = logging.DEBUG,
#                     format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
#                     encoding='utf-8')

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

emit_events = Emit()

@app.get(
    "/token",
    tags=["User"],
    response_model=str,
    summary="Get token valido",
    response_description="String indicando si hay usuario conectado",
    status_code=status.HTTP_200_OK,
)
def get_token():
    logging.info("Getting token valido")
    dato = mongodb_client.service_users.users.find({"token": {"$ne": ""}})
    #validar token para ver si hay usuario conectado valido
    if(dato == None):
        raise HTTPException(status_code=404, detail="No se encontro usuario conectado")
    else:
        return "Conectado"

@app.get(
    "/users/{username}/{password}",
    tags=["User"],
    response_model=list[str],
    summary="Logging",
    response_description="Token de usuario",
)
def loging(username: str, password: str):
    try:
        user = mongodb_client.service_users.users.find_one({"username": username})
        if(sha256_crypt.verify(password,user["password"])):
            user = userEntity(user)
            return [str(user["id"]),str(user["token"])]
        else:
            return ["Contraseña Incorrecta","Contraseña Incorrecta"]
    except (InvalidId, TypeError):
        return ["No se encontro usuario","No se encontro usuario"]

@app.get(
    "/users",
    tags=["User"],
    response_model=list[User],
    summary="Get all Users",
    response_description="A list of all Users",
    status_code=status.HTTP_200_OK,
)
def get_all_users():
    logging.info("Getting all Users...")
    return usersEntity(mongodb_client.service_users.users.find({}))


@app.get(
    "/users/{id}",
    tags=["User"],
    response_model=User,
    summary="Get an User",
    response_description="The User found",
)
def get_user(id: str):
    try:
        user = mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
        # logging.info("Getting User by id: %s" % id)
        return userEntity(user)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail="User not found")


@app.post(
    "/users",
    tags=["User"],
    response_model=User,
    summary="Create an User",
    response_description="The created User",
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: User):
    """
    Create an User with all the information:
    - **id**: temporal id, just for api-gateway purposes
    - **name**: the User's name
    - **password**: the User's password
    - **email**: optional parameter
    - **admin**: optional parameter, doesn't have an use for now
    - **phone_number**: optional parameter, the User's phone number
    """
    try:
        new_user = dict(user)
        new_user["password"] = sha256_crypt.encrypt(new_user["password"])
        del new_user["id"]
        id = mongodb_client.service_users.users.insert_one(new_user).inserted_id
        user = mongodb_client.service_users.users.find_one({"_id": id})
        logging.info("new user created")
        new_user["id"] = str(id)
        emit_events.send(str(id), "create", new_user)
        return userEntity(user)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Something went wrong")


@app.put("/users/{id}/{token}",
    tags=["User"],
    response_model=User,
    summary="Actualizar token",
    response_description="The ad received",
)
def update_user_token(id: str, token: str):
    user = mongodb_client.service_users.users.find_one({"_id": id})
    try:
        mongodb_client.service_users.users.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": {"token": str(token)}}
        )
        logging.info("User has new token: %s" % token)
        emit_events.send(id, "updatead", user)
        return userEntity(
            mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
        )
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail="User not found")


@app.put(
    "/users/{id}",
    tags=["User"],
    response_model=User,
    summary="Update an User",
    response_description="The updated User",
    deprecated=True,
)
def update_user(id: str, user: UserUpdate):
    try:
        user = UserUpdate.dict(exclude_unset=True)

        mongodb_client.service_users.users.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(user)}
        )
        logging.info("User updated: %s" % id)
        emit_events.send(id, "update", user)
        return userEntity(
            mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
        )
    except (InvalidId, TypeError):
        print(user)
        raise HTTPException(status_code=404, detail="User not found")


@app.patch(
    "/users/{id}",
    tags=["User"],
    response_model=User,
    summary="Update an User",
    response_description="The updated User",
)
def update_user(id: str, user: UserUpdate):
    try:
        user_data = userEntity(
            mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
        )
        stored_user_model = UserUpdate(**user_data)
        update_data = user.dict(exclude_unset=True)
        updated_user = stored_user_model.copy(update=update_data)
        updated_user.password = sha256_crypt.encrypt(updated_user.password)
        mongodb_client.service_users.users.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(updated_user)}
        )
        logging.info("User updated: %s" % id)
        emit_events.send(id, "update", user)
        return userEntity(
            mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
        )
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail="User not found")


@app.delete(
    "/users/{id}",
    tags=["User"],
    response_model=User,
    summary="Delete an User",
    response_description="The Deleted User",
)
def delete_user(id: str):
    try:
        user = mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
        mongodb_client.service_users.users.delete_one({"_id": ObjectId(id)})
        logging.info("User deleted: %s" % id)
        emit_events.send(id, "delete", user)
        return userEntity(user)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail="User not found")


# @app.delete(
#     "/users/{id}/ad",
#     tags=["User"],
#     response_model=User,
#     summary="Delete the ad from the user",
#     response_description="The Deleted ad",
# )
# def delete_user_ad(id: str):
#     try:
#         user = mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
#         user["ad"] = ""
#         mongodb_client.service_users.users.find_one_and_update(
#             {"_id": ObjectId(id)}, {"$set": dict(user)}
#         )
#         logging.info("User ad deleted: %s" % id)
#         emit_events.send(id, "deletead", user)
#         return userEntity(
#             mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
#         )
#     except (InvalidId, TypeError):
#         raise HTTPException(status_code=404, detail="User not found")
