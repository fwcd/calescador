import json
from datetime import datetime
from typing import Optional

class Event:
    def __init__(self, name: str, start_dt: datetime, end_dt: datetime, location: Optional[str]=None, description: Optional[str]=None):
        self.name = name
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.location = location
        self.description = description

    @staticmethod
    def from_dict(d: dict):
        return Event(
            name=d['name'],
            start_dt=datetime.fromisoformat(d['start_dt']),
            end_dt=datetime.fromisoformat(d['end_dt']),
            location=d['location'],
            description=d['description']
        )

    def to_dict(self):
        return {
            'name': self.name,
            'start_dt': self.start_dt.isoformat(),
            'end_dt': self.end_dt.isoformat(),
            'location': self.location,
            'description': self.description
        }
