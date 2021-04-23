import os

import discord
from discord import utils
from discord.ext import commands
from dotenv import load_dotenv

from clonedncopied_bot.constants import DOTENV_PATH

load_dotenv(dotenv_path=DOTENV_PATH)
TOKEN = os.getenv('DISCORD_TOKEN')

class ClonedNCopiedBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        commands.Bot.__init__(self, command_prefix="!", intents=intents)

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hi(self, ctx):
        await ctx.send('hey')

def start():
    print(f"Launching bot")
    bot = ClonedNCopiedBot()
    bot.add_cog(AdminCog(bot))
    print("Running...")
    bot.run(TOKEN)