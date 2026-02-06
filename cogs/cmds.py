import discord
from discord.ext import commands
import random

class Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("[Cog Loaded] Cmds")

    @commands.command()
    async def dm(self, ctx):
        member = ctx.author
        await member.send("hello " + member.display_name)
        await ctx.send("I sent you a dm!")

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Test command works")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello")

    @commands.command()
    async def rps(self, ctx, *, message):
        options = ['paper', 'rock', 'scissors']
        bot_choice = random.choice(options)
        await ctx.send("I choose " + bot_choice + "\n")
        if(message not in options):
            await ctx.send("Invalid pick, either enter rock, paper, or scissors")
        elif(bot_choice == message):
            await ctx.send("We tied")
        elif(message == 'paper' and bot_choice == 'rock') or \
            (message == 'rock' and bot_choice == 'scissors') or \
            (message == 'scissors' and bot_choice == 'paper'):
            await ctx.send("You Win!")
        else:
            await ctx.send("I Win!")

    @commands.command()
    async def pickagame(self, ctx):
        games = ['League', 'Valorant', 'Terraria']
        await ctx.send(random.choice(games))

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

    @commands.command()
    async def commands(self, ctx):
        list_of_commands = ['test', 'hello', 'pickagame', 'say (input)', 'commands', 'dm', 'rps (input)', 'play', 'skip', 'queue']
        all_commands = "List of all commands.\nPut '-' before each to call the command.\n\n"
        for comd in list_of_commands:
            all_commands += (comd + "\n")
        await ctx.send(all_commands)   

async def setup(bot):
    await bot.add_cog(Cmds(bot))