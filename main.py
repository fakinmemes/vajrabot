import os
import asyncio
from dotenv import load_dotenv
from colorama import Fore, Back, Style
import time
import platform

import discord
from discord.ext import commands
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S") + Back.RESET + Fore.WHITE + Style.BRIGHT)

# Import intents and create the bot here
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='?',intents=intents)

# Load Cogs goes here
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"{prfx} Loaded {Fore.YELLOW}{filename[:-3]}")

async def main():
    await load_cogs()
    discord.utils.setup_logging()
    await bot.start(TOKEN)

# Sync
    
@bot.tree.command(name="sync", description="Syncs all the latest commands.")
async def sync(interaction: discord.Interaction):
    print(prfx + " Attempting to Sync Commands...")
    if interaction.user.id == 140026874804830208:
        await bot.tree.sync()
        print(f"{prfx} synced {Fore.YELLOW}{len(bot.commands)} commands")
        await interaction.response.send_message(f"Synced {len(bot.commands)} commands.")
    else:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)

@bot.command(name="sync")
async def sync(ctx):
    print(prfx + " Attempting to Sync Commands...")
    if ctx.author.id == 140026874804830208:
        await bot.tree.sync()
        print(f"{prfx} synced {Fore.YELLOW}{len(bot.commands)} commands")
        await ctx.send(f"Synced {len(bot.commands)} commands.")
    else:
        await ctx.send("You are not allowed to use this command.")

# Ready on launch.
@bot.event
async def on_ready():
    print(f"{prfx} Logged in as {Fore.YELLOW}{bot.user.name}")
    print(f"{prfx} Bot ID {Fore.YELLOW}{bot.user.id}")
    print(f"{prfx} Discord.py Version {Fore.YELLOW}{discord.__version__}")
    print(f"{prfx} Python Version {Fore.YELLOW}{platform.python_version()}")    
        
# Run bot
asyncio.run(main())