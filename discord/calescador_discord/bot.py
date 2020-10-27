from discord import Activity, ActivityType
from discord.ext.commands import Bot

from calescador_discord.api_client import *
from calescador_discord.cogs.calendaring import *
from calescador_discord.cogs.general import *

def create_bot(command_prefix, api_url):
    bot = Bot(command_prefix, description='A Discord interface to the Calescador system')

    @bot.event
    async def on_ready():
        activity = Activity(name=f'{command_prefix}help', type=ActivityType.listening)
        await bot.change_presence(activity=activity)

    bot.add_cog(Calendaring(APIClient(api_url)))
    bot.add_cog(General())

    return bot
