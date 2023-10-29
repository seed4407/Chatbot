import os
from httpx import AsyncClient
from discord.ext import commands
import logging

# custom modules
from discord.cache import cache_get

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
)

user_host = os.getenv('USER_HOST')

class RenderingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def render(self, ctx):
        user = ctx.message.author.name
        auth_token = cache_get(user)
        logging.info(f'render: user: {user}, auth_token: {auth_token}')
        async with AsyncClient() as client:
            res = await client.post(f'{user_host}/render', json={ 'user_id': user, 'auth_token': auth_token })
            await ctx.send(f'Hey `{user}`!, your farm is being render.')