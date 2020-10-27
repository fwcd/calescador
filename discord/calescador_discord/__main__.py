import sys
import os

from calescador_discord.bot import create_bot

def getenv(key):
    value = os.getenv(key)
    if value == None:
        print(f'Please make sure that {key} is set!', file=sys.stderr)
        exit(1)
    return value

def main():
    bot = create_bot(command_prefix=';', web_url=getenv('CALESCADOR_WEB_URL'))
    bot.run(getenv('CALESCADOR_BOT_TOKEN'))

if __name__ == "__main__":
    main()
