import aiohttp
from typing import List

from calescador_discord.model.event import Event

class APIClient:
    """A wrapper around the Calescador web API."""

    def __init__(self, url):
        self.url = url

    async def request(self, method: str, route: str, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, f'{self.url}{route}', *args, **kwargs) as r:
                if (r.status // 100) == 2:
                    return await r.json()
                else:
                    raise IOError(f'Got HTTP {r.status} from API!')

    async def create_event(self, event: Event) -> Event:
        """Creates a new calendar event on the server."""

        response = await self.request('POST', f'/events', data=event.to_dict())
        return Event.from_dict(response)

    async def events(self) -> List[Event]:
        """Fetches all calendar events from the server."""

        response = await self.request('GET', f'/events')
        return [Event.from_dict(e) for e in response]

    async def upcoming_events(self) -> List[Event]:
        """Fetches upcoming calendar events from the server."""

        response = await self.request('GET', f'/events/upcoming')
        return [Event.from_dict(e) for e in response]

    async def event(self, id) -> Event:
        """Fetches a single event by its id from the server."""

        response = await self.request('GET', f'/events/{id}')
        return Event.from_dict(response)

    async def event_by_discord_message_id(self, discord_message_id) -> Event:
        """Fetches a single event by Discord message id from the server."""

        response = await self.request('GET', f'/events/discord/{discord_message_id}')
        return Event.from_dict(response)

    async def user(self, id) -> User:
        """Creates a new user on the server. Note that the password should be *unhashed*."""

        response = await self.request('POST', f'/users')
        return Event.from_dict(response)

    async def user(self, id) -> User:
        """Fetches a single user by his id from the server."""

        response = await self.request('GET', f'/users/{id}')
        return Event.from_dict(response)

    async def user_by_discord_user_id(self, discord_user_id) -> User:
        """Fetches a single user by his Discord user id from the server."""

        response = await self.request('GET', f'/users/discord/{discord_user_id}')
        return Event.from_dict(response)
