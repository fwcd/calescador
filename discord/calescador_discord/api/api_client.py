import json
import requests

from calescador_discord.model.event import Event

class APIClient:
    """A wrapper around the Calescador web API."""

    def __init__(self, url):
        self.url = url

    def create_event(self, event):
        requests.post(f'{self.url}/events', data=event.to_dict())

    def events(self):
        response = requests.get(f'{self.url}/events').json()
        return [Event.from_dict(e) for e in response]

    def event(self, id):
        response = requests.get(f'{self.url}/events/{id}').json()
        return Event.from_dict(response)
