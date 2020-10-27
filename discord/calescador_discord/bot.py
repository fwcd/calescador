from discord import Activity, ActivityType
from discord.ext.commands import Bot

from calescador_discord.api_client import *
from calescador_discord.cogs.calendaring import *
from calescador_discord.cogs.general import *

def create_bot(command_prefix: str, web_url: str):
    bot = Bot(command_prefix, description='A Discord interface to the Calescador system')

    @bot.event
    async def on_ready():
        activity = Activity(name=f'{command_prefix}help', type=ActivityType.listening)
        await bot.change_presence(activity=activity)

    bot.add_cog(Calendaring(bot, api=APIClient(f'{web_url}/api/v1'), web_url=web_url))
    bot.add_cog(General(bot))

    return bot
