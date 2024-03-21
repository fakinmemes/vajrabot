import asyncio

import discord
from discord.ext import commands

class SnipeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipe_message = None
        self.before_message = None
        self.after_message = None

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.snipe_message = message

        await asyncio.sleep(60)

        if message.id == self.snipe_message.id:
            self.snipe_message = None

    @commands.command(name='snipe')
    async def snipe(self, ctx):
        try:
            user = self.bot.get_user(self.snipe_message.author.id)
            snipeEmbed = discord.Embed(
                description = self.snipe_message.content, 
                color = discord.Colour.random(),
                timestamp = self.snipe_message.created_at
                )
            snipeEmbed.set_author(name = f'{user.global_name}', icon_url = user.avatar.url)
            await ctx.send(embed = snipeEmbed)
        except:
            await ctx.send(f'There\'s nothing to snipe!')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.before_message = before
        self.after_message = after

        await asyncio.sleep(60)

        if after.id == self.after_message.id and self.after_message:
            self.before_message = None
            self.after_message = None

    @commands.command(name='editsnipe')
    async def editsnipe(self, ctx):
        try:
            user = self.bot.get_user(self.after_message.author.id)
            snipeEmbed = discord.Embed( 
                color = discord.Colour.random(),
                timestamp = self.after_message.created_at
                )
            snipeEmbed.add_field(name = 'Before', value = self.before_message.content, inline = False)
            snipeEmbed.add_field(name = 'After', value = self.after_message.content, inline = False)
            snipeEmbed.set_author(name = f'{user.global_name}', icon_url = user.avatar.url)
            await ctx.send(embed = snipeEmbed)
        except:
            await ctx.send(f'There\'s nothing to snipe!')

async def setup(bot):
    await bot.add_cog(SnipeCommands(bot))