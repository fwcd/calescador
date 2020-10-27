import json
import requests
from typing import List

from calescador_discord.model.event import Event

class APIClient:
    """A wrapper around the Calescador web API."""

    def __init__(self, url):
        self.url = url

    def create_event(self, event: Event) -> Event:
        """Creates a new calendar event on the server."""

        response = requests.post(f'{self.url}/events', data=event.to_dict()).json()
        return Event.from_dict(response)

    def events(self) -> List[Event]:
        """Fetches all calendar events from the server."""

        response = requests.get(f'{self.url}/events').json()
        return [Event.from_dict(e) for e in response]

    def upcoming_events(self) -> List[Event]:
        """Fetches upcoming calendar events from the server."""

        response = requests.get(f'{self.url}/events/upcoming').json()
        return [Event.from_dict(e) for e in response]

    def event(self, id) -> Event:
        """Fetches a single event from the server."""

        response = requests.get(f'{self.url}/events/{id}').json()
        return Event.from_dict(response)
