import re
import itertools
from datetime import datetime, timedelta
from discord import Embed
from discord.ext import commands
from typing import List

from calescador_discord.api_client import APIClient
from calescador_discord.model.event import Event
from calescador_discord.utils.datetime import parse_date, parse_time, next_weekday, format_date, format_time, format_datetime_span
from calescador_discord.utils.discord import error_embed

class Calendaring(commands.Cog):
    """A collection of calendaring commands."""

    def __init__(self, bot, api: APIClient):
        self.bot = bot
        self.api = api

    def parse_event(self, raw):
        """Parses an event from the syntax `[day/date], [time(s)], [name]`."""

        split = [s.strip() for s in raw.split(',')]

        if len(split) < 3:
            raise ValueError('Please use a comma as separator!')

        day = parse_date(split[0])
        times = [parse_time(s.strip()) for s in split[1].split('-')]
        name = split[2]

        if name == "":
            raise ValueError('Name should not be empty!')

        if len(times) not in [1, 2]:
            raise ValueError('Please provide a start (and optionally an end) time!')

        start_dt = datetime.combine(day, times[0])
        end_dt = datetime.combine(day, times[1]) if len(times) > 1 else start_dt + timedelta(hours=2)

        return Event(
            name=name.capitalize(),
            start_dt=start_dt,
            end_dt=end_dt
        )

    @commands.command(brief='Creates a new event')
    async def create(self, ctx, *args):
        event = self.parse_event(' '.join(args))
        event = await self.api.create_event(event)

        embed = Embed(
            title=f':calendar_spiral: New Event: {event.name}',
            description=format_datetime_span(event.start_dt, event.end_dt)
        )
        embed.set_footer(text='React with the number of people you want to bring!')

        await ctx.send(embed=embed)

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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        my_id = self.bot.user.id

        if payload.user_id != my_id and message.author.id == my_id:
            print('Got reaction on my own message!')

    def events_embed(self, events: List[Event]) -> Embed:
        embed = Embed(title=':calendar_spiral: All Events')

        for (date, events) in itertools.groupby(events, lambda e: e.start_dt.date()):
            lines = [f'{format_time(e.start_dt.time())} - {format_time(e.end_dt.time())}: {e.name} (ID: {e.id})' for e in events]
            embed.add_field(name=format_date(date), value='\n'.join(lines), inline=False)

        return embed

    @commands.command(brief='Fetches upcoming events in the calendar')
    async def upcoming(self, ctx):
        events = await self.api.upcoming_events()
        await ctx.send(embed=self.events_embed(events))

    @commands.command(brief='Fetches all events in the calendar')
    async def events(self, ctx):
        events = await self.api.events()
        await ctx.send(embed=self.events_embed(events))

    @events.error
    async def events_error(self, ctx, error):
        await ctx.send(embed=error_embed('Could not fetch all events!', error))
        raise error
