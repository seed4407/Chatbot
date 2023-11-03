import time
import logging
import requests

from ariadne import QueryType
from ariadne import MutationType
from ariadne import ObjectType
from ariadne import make_executable_schema
from ariadne import load_schema_from_path

from ariadne.asgi import GraphQL

from graphql.type import GraphQLResolveInfo

from starlette.middleware.cors import CORSMiddleware

type_defs = load_schema_from_path("./app/schema.graphql")

query = QueryType()
mutation = MutationType()

user = ObjectType("User")

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)


@query.field("getUser")
def resolve_get_user(obj, resolve_info: GraphQLResolveInfo, id):
    response = requests.get(f"http://tarea_u4_service_users/users/{id}")

    if response.status_code == 200:
        return response.json()


@query.field("listUsers")
def resolve_list_users(obj, resolve_info: GraphQLResolveInfo):
    # Make it slow
    time.sleep(3)

    response = requests.get(f"http://tarea_u4_service_users/users")

    if response.status_code == 200:
        return response.json()


@mutation.field("createUser")
def resolve_create_user(
    obj,
    resolve_info: GraphQLResolveInfo,
    id,
    name,
    username,
    password,
    email,
    admin,
    phone_number,
    ad
):
    payload = dict(
        id=id,
        name=name,
        username=username,
        password=password,
        email=email,
        admin=admin,
        phone_number=phone_number,
        ad=ad
    )

    return requests.post(f"http://tarea_u4_service_users/users", json=payload).json()

@mutation.field("updateUser")
def resolve_update_user(
    obj,
    resolve_info: GraphQLResolveInfo,
    id,
    name=None,
    username=None,
    password=None,
    email=None,
    admin=None,
    phone_number=None,
    ad=None
):
    payload = dict()
    if id is not None:
        payload["id"]=id
    if name is not None:
        payload["name"]=name
    if username is not None:
        payload["username"]=username
    if password is not None:
        payload["password"]=password
    if email is not None:
        payload["email"]=email
    if admin is not None:
        payload["admin"]=admin
    if phone_number is not None:
        payload["phone_number"]=phone_number
    if ad is not None:
        payload["ad"]=ad
    return requests.patch(f"http://tarea_u4_service_users/users/{id}",json=payload).json()

@mutation.field("deleteUser")
def resolve_delete_user(
    obj,
    resolve_info: GraphQLResolveInfo,
    id
):
    return requests.delete(f"http://tarea_u4_service_users/users/{id}").json()

@mutation.field("updateUserAd")
def resolve_update_user_ad(
    obj,
    resolve_info: GraphQLResolveInfo,
    id,
    ad
):
    return requests.put(f"http://tarea_u4_service_users/users/{id}/{ad}").json()

@mutation.field("deleteUserAd")
def resolve_delete_user_ad(
    obj,
    resolve_info: GraphQLResolveInfo,
    id
):
    return requests.delete(f"http://tarea_u4_service_users/users/{id}/ad").json()

schema = make_executable_schema(type_defs, query, mutation, user)
app = CORSMiddleware(
    GraphQL(schema, debug=True),
    allow_origins=["*"],
    allow_methods=("GET", "POST", "OPTIONS"),
)
