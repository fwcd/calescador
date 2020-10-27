from discord import Embed

NEWLINE = '\n'

def error_embed(message=None, error=None):
    return Embed(
        description=f":warning: {(str(x) for x in [message, error] if x).join(NEWLINE)}"
    )
