
import discord
from discord.ext import commands

# custom modules
from discord.commands.user import UserCommands
from discord.commands.farm import FarmCommands
from discord.commands.rendering import RenderingCommands
from discord.commands.marketplace import MarketplaceCommands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    try:
        print(f'{bot.user.name} has connected to Discord!')
        await bot.add_cog(UserCommands(bot))
        await bot.add_cog(FarmCommands(bot))
        await bot.add_cog(RenderingCommands(bot))
        await bot.add_cog(MarketplaceCommands(bot))

    except Exception as e:
        print(e)