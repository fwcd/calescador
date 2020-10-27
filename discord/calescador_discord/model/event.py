import json
import dateutil.parser
from datetime import datetime, timedelta
from typing import Optional

from calescador_discord.utils.general import filter_not_none, map_noneable

class Event:
    """A calendar event."""

    def __init__(
        self,
        id: Optional[int]=None,
        name: str='',
        start_dt: datetime=datetime.now(),
        end_dt: datetime=datetime.now() + timedelta(hours=1),
        location: Optional[str]=None,
        description: Optional[str]=None,
        discord_message_id: Optional[int]=None
    ):
        self.id = id
        self.name = name
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.location = location
        self.description = description
        self.discord_message_id = discord_message_id

    @staticmethod
    def from_dict(d: dict):
        return Event(
            id=d.get('id', None),
            name=d['name'],
            start_dt=dateutil.parser.parse(d['start_dt']),
            end_dt=dateutil.parser.parse(d['end_dt']),
            location=d['location'],
            description=d['description'],
            discord_message_id=map_noneable(d.get('discord_message_id', None), lambda s: int(s))
        )

    def to_dict(self):
        return filter_not_none({
            'id': self.id,
            'name': self.name,
            'start_dt': self.start_dt.isoformat(),
            'end_dt': self.end_dt.isoformat(),
            'location': self.location,
            'description': self.description,
            'discord_message_id': map_noneable(self.discord_message_id, lambda i: str(i))
        })
