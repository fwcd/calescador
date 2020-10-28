from calescador_discord.utils.general import filter_not_none

class Attendance:
    """An attendance of a user to an event."""

    def __init__(
        self,
        user_id: int,
        event_id: int,
        count: int
    ):
        self.user_id = user_id
        self.event_id = event_id
        self.count = count

    @staticmethod
    def from_dict(d: dict):
        return Attendance(
            id=d['id'],
            user_id=d['user_id'],
            event_id=d['event_id']
        )

    def to_dict(self):
        return filter_not_none({
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id
        })
