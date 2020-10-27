import re
from datetime import datetime, timedelta
from discord import Embed
from discord.ext import commands

from calescador_discord.api_client import APIClient
from calescador_discord.model.event import Event
from calescador_discord.utils.datetime import parse_date, parse_time, next_weekday, format_datetime_span
from calescador_discord.utils.discord import error_embed

class Calendaring(commands.Cog):
    """A collection of calendaring commands."""

    def __init__(self, api: APIClient):
        self.api = api

    def parse_event(self, raw):
        """Parses an event from the syntax `[day/date], [time(s)], [name]`."""

        split = [s.strip() for s in raw.split(',')]

        if len(split) < 3:
            raise ValueError('Please use a comma as separator!')

        day = parse_date(split[0])
        times = [parse_time(s.strip()) for s in split[1].split('-')]
        name = split[2]

        if len(times) not in [1, 2]:
            raise ValueError('Please provide a start (and optionally an end) time!')

        start_dt = datetime.combine(day, times[0])
        end_dt = datetime.combine(day, times[1]) if len(times) > 1 else start_dt + timedelta(hours=2)

        return Event(
            name=name,
            start_dt=start_dt,
            end_dt=end_dt
        )

    @commands.command(brief='Creates a new event')
    async def create(self, ctx, *args):
        event = self.parse_event(' '.join(args))
        event = self.api.create_event(event)

        await ctx.send(embed=Embed(
            title=f':calendar_spiral: New Event `{event.name}`',
            description=format_datetime_span(event.start_dt, event.end_dt)
        ))

    @create.error
    async def create_error(self, ctx, error):
        await ctx.send(embed=error_embed('\n'.join([
            'Please use the syntax: `[day/date], [time(s)], [name]`',
            '',
            'For example:',
            '`monday, 19:00, Some event`',
            '`28.10.2020, 16:00-17:00, Another event`'
        ]), error))
        raise error
