import json
import requests

from calescador_discord.model.event import Event

class APIClient:
    """A wrapper around the Calescador web API."""

    def __init__(self, url):
        self.url = url

    def create_event(self, event):
        """Creates a new calendar event on the server."""

        requests.post(f'{self.url}/events', data=event.to_dict())

    def events(self):
        """Fetches all calendar events from the server."""

        response = requests.get(f'{self.url}/events').json()
        return [Event.from_dict(e) for e in response]

    def event(self, id):
        """Fetches a single event from the server."""

        response = requests.get(f'{self.url}/events/{id}').json()
        return Event.from_dict(response)
