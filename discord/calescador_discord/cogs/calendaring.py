import re
import itertools
from datetime import datetime, timedelta
from discord import Embed
from discord.ext import commands
from passgen import passgen
from typing import List

from calescador_discord.api_client import APIClient
from calescador_discord.model.event import Event
from calescador_discord.model.user import User
from calescador_discord.utils.datetime import parse_date, parse_time, next_weekday, format_date, format_time, format_datetime_span
from calescador_discord.utils.discord import error_embed
from calescador_discord.utils.emoji import number_to_emoji, emoji_to_number

class Calendaring(commands.Cog):
    """A collection of calendaring commands."""

    def __init__(self, bot, api: APIClient, web_url: str):
        self.bot = bot
        self.api = api
        self.web_url = web_url

    def parse_event(self, raw: str, discord_message_id):
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
            end_dt=end_dt,
            discord_message_id=discord_message_id
        )

    @commands.command(brief='Creates a new event')
    async def create(self, ctx, *args):
        event = self.parse_event(' '.join(args), ctx.message.id)

        embed = Embed(
            title=f':calendar_spiral: New Event: {event.name}',
            description=format_datetime_span(event.start_dt, event.end_dt)
        )
        embed.set_footer(text='React with the number of people you want to bring!')
        sent = await ctx.send(embed=embed)

        event.discord_message_id = sent.id
        await self.api.create_event(event)

        for i in range(1, 5):
            await sent.add_reaction(number_to_emoji(i))

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

    # TODO: Add option to reset user accounts on the server without deleting them?

    async def add_attendance(self, discord_user, event_id, count):
        """Adds a user with the given attendance count to the event, creating the necessary user if it not already exists."""

        try:
            user = await self.api.user_by_discord_user_id(discord_user.id)
        except:
            # User seems to be unregistered, create him
            new_user = User(
                name=f'{discord_user.name}#{discord_user.discriminator}',
                password=passgen(), # plaintext
                discord_user_id=discord_user.id
            )

            user = await self.api.create_user(new_user)
            await discord_user.send('\n'.join([
                'Hey! Since you recently reacted on an event, I thought it might be a good idea to make you an account, so here goes.',
                '```',
                f'Username: {new_user.name}',
                f'Password: {new_user.password}',
                '```',
                f'You can use these credentials to log in on <{self.web_url}>! Just a final note: Please make sure to save the password, I cannot show it to you again.',
                '',
                'Have fun! :D'
            ]))

        try:
            # If a previous attendance exists, replace it
            current_attendance = await self.api.attendance(user.id, event_id)
            current_count = current_attendance.count
            await self.api.unattend(user.id, event_id)
        except:
            current_count = 0

        new_count = current_count + count
        await self.api.attend(user.id, event_id, new_count)

        print(f"Successfully {'added' if current_count == 0 else 'updated'} attendance of {discord_user.name} with {new_count} people to event {event_id}!")

    async def remove_attendance(self, discord_user, event_id, count):
        user = await self.api.user_by_discord_user_id(discord_user.id)
        current_attendance = await self.api.attendance(user.id, event_id)
        current_count = current_attendance.count

        new_count = current_count - count
        await self.api.unattend(user.id, event_id)

        if new_count <= 0:
            print(f'Successfully removed attendance of {discord_user.name} to event {event_id}!')
        else:
            await self.api.attend(user.id, event_id, new_count)
            print(f'Successfully updated attendance of {discord_user.name} with {new_count} people to event {event_id}!')

    async def extract_reaction_payload(self, payload):
        count = emoji_to_number(payload.emoji.name)

        if count == None:
            # Ignore other emojis
            return None

        channel = self.bot.get_channel(payload.channel_id)
        user = await self.bot.fetch_user(payload.user_id)
        message = await channel.fetch_message(payload.message_id)
        my_id = self.bot.user.id

        if channel == None:
            print("Warning: No channel found from reaction payload!")
            return None
        if user == None:
            print("Warning: No user found from reaction payload!")
            return None
        if message == None:
            print("Warning: No message found from reaction payload!")
            return None

        if user.id == my_id or message.author.id != my_id:
            # Ignore own reactions and reactions to other messages
            return None

        return (count, channel, user, message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        extracted = await self.extract_reaction_payload(payload)

        if extracted != None:
            (count, channel, user, message) = extracted
            event = await self.api.event_by_discord_message_id(message.id)
            await self.add_attendance(user, event.id, count)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        extracted = await self.extract_reaction_payload(payload)

        if extracted != None:
            (count, channel, user, message) = extracted
            event = await self.api.event_by_discord_message_id(message.id)
            await self.remove_attendance(user, event.id, count)

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
