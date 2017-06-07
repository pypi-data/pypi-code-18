""" Main .py file for running the card-py-bot """
from discord.ext import commands
import get_card

DESCRIPTION = '''Toasterstein's card-py-bot: An auto magic card link parsing
and embedding Discord bot!'''

BOT = commands.Bot(command_prefix='?', description=DESCRIPTION)


@BOT.event
async def on_ready():
    """ Startup callout/setup """
    print('Logged in as')
    print(BOT.user.id)
    print('------')


@BOT.event
async def on_message(message):
    """ Standard message handler with card and shush functions """
    if "http://gatherer.wizards.com/Pages/Card" in message.content:
        print("likely inputted card url:", message.content)
        card_string = get_card.grab_html_from_url(message.content)

        await BOT.send_message(message.channel, card_string)

    await BOT.process_commands(message)


def main():
    BOT.run('MzIxNzgxNzEzNTAyMDc2OTMw.DBj7Uw.KymkGSfhgfTUqdDkJrEf8tXdCxw')


if __name__ == "__main__":
    main()
