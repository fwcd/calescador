from typing import Optional

from calescador_discord.utils.general import filter_not_none, map_noneable

class User:
    """
    A user (in the Calescador Web backend). The password
    shall be *unhashed* in User instances sent to the database
    for creation and is *hashed* in instances from database
    queries.
    """

    def __init__(
        self,
        id: Optional[int]=None,
        name: str='',
        password: Optional[str]=None,
        discord_user_id: Optional[int]=None
    ):
        self.id = id
        self.name = name
        self.password = password
        self.discord_user_id = discord_user_id

    @staticmethod
    def from_dict(d: dict):
        return User(
            id=d.get('id', None),
            name=d['name'],
            password=d.get('password', None),
            discord_user_id=map_noneable(d.get('discord_user_id', None), lambda s: int(s))
        )

    def to_dict(self):
        return filter_not_none({
            'id': self.id,
            'name': self.name,
            'password': self.password
        })
