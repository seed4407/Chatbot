import os
from httpx import AsyncClient
from discord.ext import commands
import logging

# custom modules
from discord.command_parser import command_parser
from discord.cache import cache_get

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
)

user_host = os.getenv('USER_HOST')


class FarmCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def harvest(self, ctx):
        user = ctx.message.author.name
        action_item, action_amount = command_parser(ctx.message.content)
        logging.info(f'harvest: user: {user}, action_item: {action_item}, action_amount: {action_amount}')
        auth_token = cache_get(user)
        async with AsyncClient() as client:
            res = await client.post(
                f'{user_host}/farm',
                json={
                    'auth_token': auth_token,
                    'action': 'harvest',
                    'action_item': action_item,
                    'action_amount': action_amount
                }
            )
            await ctx.send(f'harvesting...')
    
    @commands.command()
    async def plant(self, ctx):
        user = ctx.message.author.name
        action_item, action_amount = command_parser(ctx.message.content)
        logging.info(f'plant: user: {user}, action_item: {action_item}, action_amount: {action_amount}')
        auth_token = cache_get(user)
        async with AsyncClient() as client:
            res = await client.post(
                f'{user_host}/farm',
                json={
                    'auth_token': auth_token,
                    'action': 'plant',
                    'action_item': action_item,
                    'action_amount': action_amount
                }
            )
            await ctx.send(f'planting...')

    @commands.command()
    async def water(self, ctx):
        user = ctx.message.author.name
        action_item, action_amount = command_parser(ctx.message.content)
        logging.info(f'water: user: {user}, action_item: {action_item}, action_amount: {action_amount}')
        auth_token = cache_get(user)
        async with AsyncClient() as client:
            res = await client.post(
                f'{user_host}/farm',
                json={
                    'auth_token': auth_token,
                    'action': 'water',
                    'action_item': action_item,
                    'action_amount': action_amount
                }
            )
            await ctx.send(f'watering..')