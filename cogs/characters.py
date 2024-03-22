import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient

import discord
from discord.ext import commands
from discord import app_commands

uri = "mongodb+srv://admin:N0P@ssw0rd@vajrabot.eqvlech.mongodb.net/?retryWrites=true&w=majority&appName=vajrabot"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

class Characters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Characters(bot))