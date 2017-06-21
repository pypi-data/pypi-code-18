""" Main .py file for running the card-py-bot """
import os
import argparse

import discord
from discord.ext import commands

from card_py_bot.get_card import scrape_wizzards, card_data2string, card_data2embed
from card_py_bot.config_emoji import print_ids


DESCRIPTION = '''Toasterstein's card-py-bot: An auto magic card link parsing
and embedding Discord bot!'''

BASEDIR = os.path.dirname(os.path.realpath(__file__))

BOT = commands.Bot(command_prefix='?', description=DESCRIPTION)


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
    await BOT.process_commands(message)

@BOT.command()
async def print_setup():
    """ Print the emoji config strings for setting up the mana icon config """
    await BOT.say(print_ids())


@BOT.command(pass_context=True)
async def save_setup(ctx):
    """ Save any user printed emoji config strings to the card_py_bot """
    channel = ctx.message.channel
    async for message in BOT.logs_from(ctx.message.channel, limit=1):
        config_f = open(BASEDIR+'\\mana_config.txt', 'w')
        emoji_ids = message.content.split()[1:]
        for emoji_id in emoji_ids:
            emoji_id = emoji_id.lstrip('\\\\')
            print("saving emoji_id:", emoji_id)
            config_f.write(emoji_id+'\n')
        config_f.close()
        print("all emoji_ids saved successfuly")

def main():
    parser = argparse.ArgumentParser(description='Discord magic card detail parser')

    parser.add_argument('-t', '--token', type=str,
                        help='Discord Token for the bot!')

    args = parser.parse_args()

    if args.token is None:
        raise Exception('Error: Discord Bot token required')
    else:
        BOT.run(args.token)


if __name__ == "__main__":
    main()
