from discord.ext import commands

class Calendaring(commands.Cog):
    """A collection of calendaring commands."""

    def __init__(self, api):
        self.api = api

    @commands.command(brief='Creates a new event')
    async def create(self, ctx):
        pass
