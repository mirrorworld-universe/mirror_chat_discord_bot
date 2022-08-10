import os
import time
import discord
from dotenv import load_dotenv
from Pegasus import Pegasus
from config import Config

load_dotenv()

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


@client.event
async def on_error(event, *args, **kwargs):
    print(repr(event))
    global client
    client = discord.Client()

client.run(Config.TOKEN)
