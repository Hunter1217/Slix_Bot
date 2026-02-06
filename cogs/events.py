import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      print("[Cog Loaded] Events")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await before.channel.send("Message edited: " + before.content)
        await before.channel.send("Message after edit: " + after.content)        

async def setup(bot):
    await bot.add_cog(Events(bot))
    print("setup worked")