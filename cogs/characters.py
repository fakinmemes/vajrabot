import os
import urllib.parse
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient

import discord
from discord.ext import commands
from discord import app_commands

load_dotenv()
username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
username = urllib.parse.quote_plus(username)
password = urllib.parse.quote_plus(password)

uri = f"mongodb+srv://{username}:{password}@vajrabot.eqvlech.mongodb.net/?retryWrites=true&w=majority&appName=vajrabot"

# Create a new client and connect to the server
client = MongoClient(uri)

# Access the database
db = client['genshinDB']
collection = db['canons']

class Characters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="character", description="View a character, their status, and who claimed them.")
    @app_commands.describe(character="The character to view.")
    async def view(self, interaction: discord.Interaction, character: str):
        character = character.lower()
        
        # Find the character in the database
        result = collection.aggregate([{"$search": {
                                                "index": "characterSearch",
                                                "text": {
                                                    "query": character,
                                                    "path": {
                                                    "wildcard": "*"
                                                    }}}}])
        result = list(result)
        if len(result) == 0:
            return await interaction.response.send_message("Character not found.", ephemeral=True)
        result = result[0]
        status = result["status"] if result["status"] == "Open" else f'{result["status"]} by {self.bot.get_user(result["player"]).mention}.' 

        # Make the embed
        embed = discord.Embed(
            title = result["name"],
            color = discord.Colour.random(),
            description = f'''Tier: {result["tier"]}\nRegion: {result["region"]}\nStatus: {status}\nType: {result["type"]}'''
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Characters(bot))