import os
import asyncio
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Import intents and create the bot here

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?',intents=intents)

# Bot code goes here

# Ready on launch.
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Snipe functionality.
snipe_message = None

@bot.event
async def on_message_delete(message):
    global snipe_message
    snipe_message = message

    await asyncio.sleep(60)

    if message.id == snipe_message.id:
        snipe_message = None

@bot.command(name = 'snipe')
async def snipe(ctx):
    try:
        user = bot.get_user(snipe_message.author.id)
        snipeEmbed = discord.Embed(
            description = snipe_message.content, 
            color = 0x00ff00,
            timestamp=snipe_message.created_at
            )
        snipeEmbed.set_author(name = f'{user.global_name}', icon_url = user.avatar.url)
        await ctx.send(embed = snipeEmbed)
    except:
        await ctx.send(f'There\'s nothing to snipe!')

# Edit functionality.
before_message = None
after_message = None

@bot.event
async def on_message_edit(before, after):
    global before_message
    global after_message
    before_message = before
    after_message = after

    await asyncio.sleep(60)

    if after.id == after_message.id:
        before_message = None
        after_message = None

@bot.command(name = 'editsnipe')
async def editsnipe(ctx):
    try:
        user = bot.get_user(after_message.author.id)
        snipeEmbed = discord.Embed( 
            color = 0x00ff00,
            timestamp=after_message.created_at
            )
        snipeEmbed.add_field(name = 'Before', value = before_message.content, inline = False)
        snipeEmbed.add_field(name = 'After', value = after_message.content, inline = False)
        snipeEmbed.set_author(name = f'{user.global_name}', icon_url = user.avatar.url)
        await ctx.send(embed = snipeEmbed)
    except:
        await ctx.send(f'There\'s nothing to snipe!')

# Test functionality.
@bot.command(name = 'test')
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')

# Reaction messages functionality.
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    match message.content:
        case 'poggers':
            await message.channel.send('https://cdn.discordapp.com/attachments/462268118132064256/1174379584238665838/bajira.png?ex=65676137&is=6554ec37&hm=dc4f5678391d0a440de75f89c731044e01fbdf2414310f150514993fb935f283&')

    await bot.process_commands(message)
        
# Run bot

bot.run(TOKEN)