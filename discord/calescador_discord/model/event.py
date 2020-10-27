import json
from datetime import datetime, timedelta
from typing import Optional

class Event:
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
        start_dt = datetime.fromisoformat(d['start_dt'])
        end_dt = datetime.fromisoformat(d['end_dt'])
        id = d.get('id', None)
        discord_message_id = d.get('discord_message_id', None)

        return Event(
            id=int(id) if id else None,
            name=d['name'],
            start_dt=start_dt,
            end_dt=end_dt,
            location=d['location'],
            description=d['description'],
            discord_message_id=int(discord_message_id) if discord_message_id else None
        )

    def to_dict(self):
        return {
            'id': str(self.id) if self.id else None,
            'name': self.name,
            'start_dt': self.start_dt.isoformat(),
            'end_dt': self.end_dt.isoformat(),
            'location': self.location,
            'description': self.description,
            'discord_message_id': str(self.discord_message_id) if self.discord_message_id else self.discord_message_id
        }
