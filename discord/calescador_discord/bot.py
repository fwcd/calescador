from discord import Activity, ActivityType
from discord.ext.commands import Bot

from calescador_discord.commands.ping import *

def create_bot(command_prefix):
    bot = Bot(command_prefix, description='A Discord interface to the Calescador system')

    @bot.event
    async def on_ready():
        activity = Activity(name=f'{command_prefix}help', type=ActivityType.listening)
        await bot.change_presence(activity=activity)

    bot.add_command(ping)

    return bot