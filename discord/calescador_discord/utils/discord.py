from discord import Embed

NEWLINES = '\n\n'

def error_embed(message=None, error=None):
    return Embed(
        description=f":warning: {NEWLINES.join(str(x) for x in [message, error] if x)}"
    )
