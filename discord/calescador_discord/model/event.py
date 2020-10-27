import json

class Event:
    def __init__(self, name, start_dt, end_dt, location=None, description=None):
        self.name = name
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.location = location
        self.description = description

    @staticmethod
    def from_dict(d):
        return Event(
            name=d['name'],
            start_dt=d['start_dt'],
            end_dt=d['end_dt'],
            location=d['location'],
            description=d['description']
        )

    def to_dict(self):
        return {
            'name': self.name,
            'start_dt': self.start_dt,
            'end_dt': self.end_dt,
            'location': self.location,
            'description': self.description
        }
