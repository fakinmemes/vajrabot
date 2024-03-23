import pandas as pd

import discord
from discord.ext import commands
from discord import app_commands

class Characters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = self.bot.client

    async def get_character(self, character:str):
        # Access the database
        db = self.client['genshinDB']
        collection = db['characters']
        character = character.lower()

        # Find the character in the database
        result = collection.aggregate([
            {
                "$search": {
                    "index": "characterSearch",
                    "text": {
                        "query": character,
                        "path": {
                        "wildcard": "*"
                        }
                    }
                }
            }
        ])
        result = list(result)

        if len(result) == 0:
            return None
        result = result[0]
        
        # Async only during testing because private server. Should be get_user in actual setting.
        if result["player"]: player = await self.bot.fetch_user(result["player"])
        else: player = None

        if result["updated"]: time = result["updated"]
        else: time = None

        return result, player, time
    

    @app_commands.command(name="character", description="View a character, their status, and who claimed them.")
    @app_commands.describe(character="The character to view.")
    async def view(self, interaction: discord.Interaction, character: str):
        # Get the character from the database, async only for testing.
        result, player, time = await self.get_character(character)

        if result == None:
            return await interaction.response.send_message("Character not found.", ephemeral=True)
        
        if result["status"] == "Open":
            status = result["status"]  
        elif result["status"] == "Reserved":
            time = discord.utils.format_dt(time)
            status = f'{result["status"]} by {player.mention} starting from {time}.' 
        else:
            status = f'{result["status"]} by {player.mention}.'

        if result["sheet"]:
            sheet = f'[Sheet]({result["sheet"]})'
        else:
            sheet = "No sheet available."

        # Make the embed
        embed = discord.Embed(
            title = result["name"],
            color = discord.Colour.random(),
            description = f'''Tier: {result["tier"]}\nRegion: {result["region"]}\nStatus: {status}\nType: {result["type"]}\n{sheet}'''
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="reserve", description="Reserve a character.")
    @app_commands.describe(character="The character being reserved.")
    async def reserve(self, interaction: discord.Interaction, character: str):
        # Get the character from the database
        result, player, time = await self.get_character(character)

        if result == None:
            return await interaction.response.send_message("Character not found.", ephemeral=True)
        time = interaction.created_at
        dt = discord.utils.format_dt(time)
        
        # Check if the character is reserved or claimed
        if result["status"] == "Reserved":
            return await interaction.response.send_message(f"Character is already reserved by {player.mention} starting from {dt}.", ephemeral=True)
        elif result["status"] == "Claimed" or result["status"] == "Submitted":
            return await interaction.response.send_message(f"Character is already claimed or submitted by {player.mention}.", ephemeral=True)
        
        # Reserve the character
        db = self.client['genshinDB']
        collection = db['characters']
        time = discord.utils.utcnow()

        collection.update_one(
            {"name": result["name"]},
            {"$set": {"status": "Reserved", "player": interaction.user.id, "updated": time}}
        )

        await interaction.response.send_message(f"Character {result['name']} has been reserved by {interaction.user.mention} at {dt}.")


    @app_commands.command(name="submit", description="Submit a character.")
    @app_commands.describe(character="The character being submitted.", sheet="The link to the character sheet.")
    async def submit(self, interaction: discord.Interaction, character: str, sheet: str):
        # Get the character from the database
        result, player, time = await self.get_character(character)

        if result == None:
            return await interaction.response.send_message("Character not found.", ephemeral=True)
        time = interaction.created_at
        dt = discord.utils.format_dt(time)
        
        # Check if the character is reserved or claimed
        if result["status"] == "Reserved" and player != interaction.user:
            return await interaction.response.send_message(f"Character is already reserved by {player.mention} starting from {dt}.", ephemeral=True)
        elif result["status"] == "Claimed" or result["status"] == "Submitted":
            return await interaction.response.send_message(f"Character is already claimed or submitted by {player.mention}.", ephemeral=True)
        
        # Reserve the character
        db = self.client['genshinDB']
        collection = db['characters']
        time = discord.utils.utcnow()

        collection.update_one(
            {"name": result["name"]},
            {"$set": {"status": "Submitted", "player": interaction.user.id, "updated": time}}
        )

        await interaction.response.send_message(f"Character {result['name']} has been reserved by {interaction.user.mention} at {dt}.\nLink to sheet: [Sheet]({sheet})")

    
    @app_commands.command(name="drop", description="Drop a character.")
    @app_commands.describe(character="The character being dropped.")
    async def drop(self, interaction: discord.Interaction, character: str):
        # Get the character from the database
        result, player, time = await self.get_character(character)

        if result == None:
            return await interaction.response.send_message("Character not found.", ephemeral=True)
        time = interaction.created_at
        dt = discord.utils.format_dt(time)
        
        # Check if the character belongs to the user
        if player != interaction.user:
            return await interaction.response.send_message(f"Character does not belong to you, is not trialed by you, submitted by you, or reserved by you.", ephemeral=True)
        
        # Drop the character
        db = self.client['genshinDB']
        collection = db['characters']
        time = discord.utils.utcnow()

        collection.update_one(
            {"name": result["name"]},
            {"$set": {"status": "Open", "player": None, "sheet": None, "updated": time}}
        )

        await interaction.response.send_message(f"Character {result['name']} has been dropped by {interaction.user.mention} at {dt}.")
        



async def setup(bot):
    await bot.add_cog(Characters(bot))