import asyncio
import os
import random
import time
import discord
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Pegasus import Pegasus
from config import Config

load_dotenv()
users = []
dm = []

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
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
        response = Pegasus(Config.ALLOWED_CHANNELS[str(message.channel.id)]).generate_response(user_message)

        print(response)
        if response != "":
            # response = "Looking Good!"
            await message.reply(response)

        return

    elif message.content == 'raise-exception':
        raise discord.DiscordException


def is_user_limited(user_id):
    users_history = [x for x in users if x['id'] == user_id and x['time'] > datetime.now() - timedelta(minutes=int(os.getenv('RESET_RESPONSE_LIMIT_TIME')))]
    # print(f"Number of the time user chatted within {os.getenv('RESET_RESPONSE_LIMIT_TIME')} minutes: {len(users_history)}")
    if len(users_history) >= int(os.getenv('NUMBER_OF_FREE_RESPONSE')):
        # print("User is limited")
        return True
    # print("User is not limited")
    return False


def did_user_receive_dm(user_id):
    users_dm_history = [x for x in dm if x['id'] == user_id and x['time'] > datetime.now() - timedelta(minutes=int(os.getenv('RESET_RESPONSE_LIMIT_TIME')))]
    # print(f"Number of the time user got DM within {os.getenv('RESET_RESPONSE_LIMIT_TIME')} minutes: {len(users_dm_history)}")
    if len(users_dm_history) >= 1:
        # print("User Received DM")
        return True
    # print("User did not receive DM")
    return False


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(Config.TOKEN)
