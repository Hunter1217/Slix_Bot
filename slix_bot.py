import sys
import discord
from discord.ext import commands

TOKEN = "hidden for github"
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        await bot.load_extension("cogs.events")
    except Exception as e:
        print(f"Failed to load a cog {e}")

async def main():
    await bot.load_extension("cogs.cmds")
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.music")
    await bot.start(TOKEN)

import asyncio
asyncio.run(main())
