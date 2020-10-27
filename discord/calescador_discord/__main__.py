import os

from calescador_discord.bot import create_bot

def main():
    bot = create_bot(command_prefix=';', web_url=os.getenv('CALESCADOR_WEB_URL'))
    bot.run(os.getenv('CALESCADOR_BOT_TOKEN'))

if __name__ == "__main__":
    main()
