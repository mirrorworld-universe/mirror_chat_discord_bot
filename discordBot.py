import os
import time
from typing import Callable, Tuple, Any, Dict, Coroutine
import discord
import logging
import functools
import asyncio
from dotenv import load_dotenv
from Pegasus import Pegasus
from config import Config

load_dotenv()

client = discord.Client()
logging.basicConfig(level=logging.INFO)


def to_thread(func: Callable) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Coroutine[Any, Any, Any]]:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper


@to_thread
def generate_response(node_id, user_message):
    response = Pegasus(node_id).generate_response(user_message)
    return response


@client.event
async def on_ready():
    logging.info('%s has connected to Discord!', client.user.name)
    game = discord.Game(Config.STATUS)
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot or str(message.channel.id) not in Config.ALLOWED_CHANNELS['channels']:
        return

    # if bot got mentioned or trigger word found
    if client.user.mentioned_in(message) or any(trigger in message.clean_content.lower() for trigger in Config.TRIGGER_LIST):
        # Assign users message
        user_message = message.clean_content
        time.sleep(int(os.getenv('MESSAGE_DELAY')))

        # Replace gm to good morning for better understanding
        user_message = user_message.replace("gm", "good morning")
        node_id = Config.ALLOWED_CHANNELS[str(message.channel.id)]
        response = await generate_response(node_id, user_message)

        logging.info(response)
        if response != "":
            # response = "Looking Good!"
            await message.reply(response)

        return

    elif message.content == 'raise-exception':
        raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs):
    logging.error(repr(event))
    global client
    client = discord.Client()

client.run(Config.TOKEN)
