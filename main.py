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
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(prfx + " Loaded " + Fore.YELLOW + filename[:-3])

async def main():
    await load_cogs()
    await bot.start(TOKEN)

# Sync
    
@bot.tree.command(name="sync", description="Syncs all the latest commands.")
async def sync(interaction: discord.Interaction):
    print(prfx + " Attempting to Sync Commands...")
    if interaction.user.id == 140026874804830208:
        await bot.tree.sync()
        print(prfx + " synced " + Fore.YELLOW + len(bot.commands) + " commands")
    else:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)

@bot.command(name="sync")
async def sync(ctx):
    print(prfx + " Attempting to Sync Commands...")
    if ctx.author.id == 140026874804830208:
        await bot.tree.sync(guild=ctx.guild)
        print(prfx + " synced " + Fore.YELLOW + len(bot.commands) + " commands")
        await ctx.send("Synced " + len(bot.commands) + " commands.")
    else:
        await ctx.send("You are not allowed to use this command.")

@bot.tree.command(name="reload", description="Reloads a cog.")
@app_commands.describe(cog="The cog to reload.")
async def reload(interaction: discord.Interaction, cog: str):
    if interaction.user.id == 140026874804830208:
        bot.reload_extension(f'cogs.{cog}')
        print(prfx + " Reloaded " + Fore.YELLOW + cog)
    else:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)

# Ready on launch.
@bot.event
async def on_ready():
    print(prfx + " Logged in as " + Fore.YELLOW + bot.user.name)
    print(prfx + " Bot ID " + Fore.YELLOW + str(bot.user.id))
    print(prfx + " Discord.py Version " + Fore.YELLOW + discord.__version__)
    print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))    
        
# Run bot
asyncio.run(main())