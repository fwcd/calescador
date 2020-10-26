from discord.ext import commands

@commands.command(brief='Sends a simple pong message')
async def ping(ctx):
    await ctx.send("Pong!")
