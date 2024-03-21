import discord
from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Reaction messages functionality.
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author == self.bot.user:
    #         return
    #     match message.content:
    #         case 'poggers':
    #             await message.channel.send('https://cdn.discordapp.com/attachments/462268118132064256/1174379584238665838/bajira.png?ex=65676137&is=6554ec37&hm=dc4f5678391d0a440de75f89c731044e01fbdf2414310f150514993fb935f283&')

    #     await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Reactions(bot))