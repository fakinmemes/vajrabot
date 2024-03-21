from colorama import Fore, Back, Style
import time

import discord
from discord.ext import commands
from discord import app_commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S") + Back.RESET + Fore.WHITE + Style.BRIGHT)

    # Cogs
    @app_commands.command(name="reload", description="Reloads a cog.")
    @app_commands.describe(cog="The cog to reload.")
    async def reload(self, interaction: discord.Interaction, cog: str):
        if interaction.user.id == 140026874804830208:
            try:
                await self.bot.reload_extension(f'cogs.{cog}')
                print(f"{self.prfx} Reloaded {Fore.YELLOW}cog")
                await interaction.response.send_message(f"Reloaded {cog}.")
            except commands.ExtensionNotLoaded:
                await interaction.response.send_message(f"{cog} is not loaded or does not exist.")
        else:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)

    @app_commands.command(name="load", description="Loads a cog.")
    @app_commands.describe(cog="The cog to load.")
    async def load(self, interaction: discord.Interaction, cog: str):
        if interaction.user.id == 140026874804830208:
            try:
                await self.bot.load_extension(f'cogs.{cog}')
                print(f"{self.prfx} Loaded {Fore.YELLOW}cog")
                await interaction.response.send_message(f"Loaded {cog}.")
            except commands.ExtensionAlreadyLoaded:
                await interaction.response.send_message(f"{cog} is already loaded.")
            except commands.ExtensionNotFound:
                await interaction.response.send_message(f"{cog} does not exist.")

            
        else:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Basic(bot))