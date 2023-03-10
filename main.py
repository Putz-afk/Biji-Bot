import asyncio
import os
import discord
from discord.ext import commands
import json

# Get configuration
# Get configuration.json
with open("config.json", "r") as config:
    data = json.load(config)
    token = data["TOKEN"]
    prefix = data["PREFIX"]
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} logged in")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"))
    print(discord.__version__)


async def start():
    # Load cogs
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"Cogs.{filename[:-3]}")
            except Exception as e:
                print(e)
                print(f"Failed to load {filename[:-3]} cog")

    # Start Bot
    await bot.start(token)


if __name__ == '__main__':
    asyncio.run(start())
