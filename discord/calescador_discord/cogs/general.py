from discord.ext import commands

class General(commands.Cog):
    @commands.command(brief='Sends a simple pong message')
    async def ping(self, ctx):
        await ctx.send('Pong!')
