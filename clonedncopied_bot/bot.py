import os
from datetime import datetime

import discord
from discord import utils
from discord.ext import commands
from dotenv import load_dotenv
import pandas as pd

from clonedncopied_bot import constants

load_dotenv(dotenv_path=constants.DOTENV_PATH)
TOKEN = os.getenv("DISCORD_TOKEN")


class ClonedNCopiedBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        self.data_dir = constants.DATA_DIR
        self.data_dir.mkdir(exist_ok=True)
        commands.Bot.__init__(self, command_prefix="!", intents=intents)


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hi(self, ctx):
        await ctx.send("hey")

    @commands.command()
    async def get_message_history(self, ctx):
        print("Getting all messages")
        all_messages = []
        for channel in ctx.guild.text_channels:
            messages = await channel.history().flatten()
            all_messages.append(messages)
        all_messages_flat = [i for s in all_messages for i in s]
        amfd = [
            {
                "author": message.author,
                "channel": message.channel,
                "created_at": message.created_at,
                "content": message.content,
                "type": message.type,
            }
            for message in all_messages_flat
        ]
        df = pd.DataFrame(amfd)
        df.to_csv(
            self.bot.data_dir
            / f"{ctx.guild.id}_{round(datetime.now().timestamp())}_messages.csv",
            index=False,
        )
        print("finished getting messages")


def start():
    print(f"Launching bot")
    bot = ClonedNCopiedBot()
    bot.add_cog(AdminCog(bot))
    print("Running...")
    bot.run(TOKEN)