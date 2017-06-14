""" Main .py file for running the card-py-bot """
import argparse
from card_py_bot import config_emoji
from discord.ext import commands
import discord
from card_py_bot.get_card import scrape_wizzards, card_data2string, card_data2embed

DESCRIPTION = '''Toasterstein's card-py-bot: An auto magic card link parsing
and embedding Discord bot!'''

# BOT = commands.Bot(command_prefix='?', description=DESCRIPTION)
BOT = discord.Client()

@BOT.event
async def on_ready():
    """ Startup callout/setup """
    print('Logged in as')
    print(BOT.user.id)
    print("Avatar url:", BOT.user.avatar_url)
    print('------')


@BOT.event
async def on_message(message):
    """ Standard message handler with card and shush functions """
    if "http://gatherer.wizards.com/Pages/Card" in message.content:
        print("likely inputted card url:", message.content)
        card_data = scrape_wizzards(message.content)
        card_em = card_data2embed(card_data, message.content, BOT.user.avatar_url)
        await BOT.send_message(message.channel, embed=card_em)

        # TODO: old
        # card_string = card_data2string(card_data)
        # await BOT.send_message(message.channel, card_string)
    # 
    # await BOT.process_commands(message)


def main():
    parser = argparse.ArgumentParser(description='Discord magic card detail parser')

    # TODO REMOVE DEFAULT FOR RELEASE
    parser.add_argument('-t', '--token', type=str,
                        default='MzIxNzgxNzEzNTAyMDc2OTMw.DBj7Uw.KymkGSfhgfTUqdDkJrEf8tXdCxw',
                        help='Discord Token for the bot!')

    args = parser.parse_args()

    if args.token is None:
        raise Exception('Error: Discord Bot token required')
    else:
        BOT.run(args.token)


if __name__ == "__main__":
    main()
