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
    while True:
        random_time = random.randrange(Config.MIN_RANDOM_TIME_MESSAGE, Config.MAX_RANDOM_TIME_MESSAGE)
        chosen_random_message = random.choice(Config.PRE_RANDOM_MESSAGE_LIST)
        channel = client.get_channel(int(Config.RANDOM_MESSAGE_CHANNEL))
        response = Pegasus(Config.PEGASUS_SATO_NODE).generate_response(chosen_random_message)

        if response != "":
            await channel.send(response)

        await asyncio.sleep(random_time)


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot or str(message.channel.id) not in Config.ALLOWED_CHANNELS['channels']:
        return

    # if bot got mentioned or trigger word found
    if client.user.mentioned_in(message) or any(trigger in message.clean_content.lower() for trigger in Config.TRIGGER_LIST):
        _roles = []
        for role in Config.AVAILABLE_ROLES:
            _roles.append(discord.utils.find(lambda r: r.id == role, message.guild.roles))

        _role_check = any(item in _roles for item in message.author.roles)

        # if User sent more than 5 message today
        if is_user_limited(message.author.id) and not _role_check:
            # Delete the message
            await message.delete()
            # if bot didnt DM the user today
            if not did_user_receive_dm(message.author.id):
                # add user to daily DMed list
                dm.append({"id": message.author.id, "time": datetime.now()})
                # Send Message in Channel
                await message.channel.send(f"{message.author.mention} {Config.LIMIT_PUBLIC_MESSAGE}")
                # Send DM to user
                await message.author.send(f"{Config.DM_MESSAGE}")
                return

        # if User didnt finished their daily quota
        else:
            # Add append user to the daily list if user is not a collector
            if not _role_check:
                users.append({"id": message.author.id, "time": datetime.now()})
            # Assign users message
            user_message = message.clean_content

            time.sleep(int(os.getenv('MESSAGE_DELAY')))

            # Replace gm to good morning for better understanding
            user_message = user_message.replace("gm", "good morning")
            # TODO: should use which node?
            print("USE NODE: " + Config.ALLOWED_CHANNELS[str(message.channel.id)])
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
