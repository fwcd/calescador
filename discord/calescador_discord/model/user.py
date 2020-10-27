from calescador_discord.utils.general import filter_not_none, map_noneable

class User:
    """
    A user (in the Calescador Web backend). The password
    shall be UNHASHED in User instances sent to the database
    for creation and is HASHED in instances from database
    queries.
    """

    def __init__(
        self,
        id: Optional[int]=None,
        name: str='',
        password: str='',
        discord_user_id: Optional[int]=None
    ):
        self.name = name
        self.password = password
        self.discord_user_id = discord_user_id

    @staticmethod
    def from_dict(d: dict):
        return User(
            name=d['name'],
            password=d['password'],
            discord_user_id=map_noneable(d.get('discord_user_id', None), lambda s: int(s))
        )

    def to_dict(self):
        return filter_not_none({
            'id': str(self.id) if self.id else None,
            'name': self.name,
            'start_dt': self.start_dt.isoformat(),
            'end_dt': self.end_dt.isoformat(),
            'location': self.location,
            'description': self.description,
            'discord_message_id': map_noneable(self.discord_message_id, lambda i: str(i))
        })
