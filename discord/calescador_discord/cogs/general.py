from discord.ext import commands

class General(commands.Cog):
    """A collection of general commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Sends a simple pong message')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(brief='Removes my last messages from the current channel')
    async def clear(self, ctx):
        async for message in ctx.channel.history(limit=50):
            if message.author.id == self.bot.user.id:
                await message.delete()
