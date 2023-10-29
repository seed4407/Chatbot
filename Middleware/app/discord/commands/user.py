import os
from discord.ext import commands
from httpx import AsyncClient
import logging

# custom modules
from discord.command_parser import command_parser
from discord.cache import cache_save, cache_get

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
)

user_host = os.getenv('USER_HOST')

class UserCommands(commands.Cog):
    cache = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def signup(self, ctx):
        user = ctx.message.author.name
        password, = command_parser(ctx.message.content)
        async with AsyncClient() as client:
            res = await client.post(f'{user_host}/users/signup', json={ 'user_id': user, 'password': password, 'platform': 'discord' })
            if res.status_code == 201:
                logging.info(f'signup successful for: user: {user}. data: {res.json()}')
                await ctx.send(f'Hey `{user}`!, you have been signed up.')
            else:
                logging.info(f'signup failed for: user: {user}.')
                await ctx.send(f'Hey `{user}`!, we could not sign you up. Please try again later.')

    @commands.command()
    async def login(self, ctx):
        user = ctx.message.author.name
        password, = command_parser(ctx.message.content)

        async with AsyncClient() as client:
            res = await client.post(f'{user_host}/users/login', json={ 'user_id': user, 'password': password, 'platform': 'discord' })
            if res.status_code == 200:
                logging.info(f'login successful for: user: {user}. data: {res.json()}')
                await ctx.send(f'Hey `{user}`!, you have been logged in.')
                cache_save(user, res.json()['auth_token'])
            else:
                logging.info(f'login failed for: user: {user}.')
                await ctx.send(f'Hey `{user}`!, we could not log you in. Please try again later.')

    @commands.command()
    async def permission(self, ctx):
        print("add permission")
        user = ctx.message.author.name
        permission, = command_parser(ctx.message.content)
        auth_token = cache_get(user)
        print(f'permission: {permission}, auth_token: {auth_token}')
        async with AsyncClient() as client:
            res = await client.post(f'{user_host}/users/permission', json={ 'auth_token': auth_token, 'permission': permission, 'platform': 'discord' })
            if res.status_code == 200:
                logging.info(f'permission added for: user: {user}. data: {res.json()}')
                await ctx.send(f'Hey `{user}`!, you have been granted permission.')
            else:
                logging.info(f'permission failed for: user: {user}.')
                await ctx.send(f'Hey `{user}`!, we could not grant you permission. Please try again later.')
