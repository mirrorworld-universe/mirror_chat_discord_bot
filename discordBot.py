import asyncio
import os
import json
import logging
import random
import time
import torch
import numpy as np
import discord
from transformers import AutoTokenizer, pipeline
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests as requests

load_dotenv()
users = []
dm = []

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
STATUS = os.getenv('PLAYING_STATUS')
STRICT_BYPASS = os.getenv('STRICT_BYPASS')
MODEL_URL = os.getenv('MODEL_URL')
AVAILABLE_ROLES = json.loads(os.getenv('AVAILABLE_ROLES'))
ALLOWED_CHANNELS = json.loads(os.getenv('ALLOWED_CHANNELS'))
DM_MESSAGE = os.getenv('DM_MESSAGE')
LIMIT_PUBLIC_MESSAGE = os.getenv('LIMIT_PUBLIC_MESSAGE')
TRIGGER_LIST = json.loads(os.getenv('TRIGGER_LIST'))
RANDOM_MESSAGE_CHANNEL = os.getenv('RANDOM_MESSAGE_CHANNEL')
PRE_RANDOM_MESSAGE_LIST = ["Be careful", "Be careful driving", "Don't worry", "Everyone knows it", "Everything is ready", "Excellent", "From time to time", "Good idea", "He's very annoying", "He's very famous", "I can't hear you", "I'd like to go for a walk", "I don't like it", "I don't understand", "I don't want that", "I don't want to bother you", "I feel good", "I have a headache", "I know",  "I like her", "I'll pay", "I'll take it", "I lost my watch", "I love you", "I'm an American", "I'm cold", "I'm going to leave", "I'm hungry", "I'm married", "I'm busy", "I'm not ready yet", "I'm not sure",  "I'm thirsty", "I'm very busy. I don't have time now", "I need to go home", "I only want a snack", "I thought the clothes were cheaper", "I've been here for two days", "I've heard Texas is a beautiful place", "I've never seen that before", "Just a little", "Just a moment", "Let me check", "Let me think about it", "Let's go have a look", "Never mind", "Next time", "No", "Nonsense", "No, thank you", "Nothing else", "Not recently", "Not yet", "Of course", "Okay", "Please fill out this form", "Please take me to this address", "Please write it down", "Really?  Right here", "Right there", "See you later", "See you tomorrow", "See you tonight", "She's pretty", "Sorry to bother you", "Stop!  Take a chance", "Take it outside", "Tell me", "Thanks for everything", "Thanks for your help", "Thank you", "Thank you miss", "Thank you sir", "Thank you very much", "That looks great", "That's alright", "That's enough", "That's fine", "That's it", "That smells bad", "That's not fair", "That's not right", "That's right", "That's too bad", "That's too many", "That's too much", "The book is under the table", "They'll be right back", "They're the same", "They're very busy", "This doesn't work", "This is very difficult", "This is very important", "Try it", "Very good, thanks", "We like it very much", "You're beautiful", "You're very nice", "You're very smart", "Your things are all here"]
MIN_RANDOM_TIME_MESSAGE = int(os.getenv('MIN_RANDOM_TIME_MESSAGE'))
MAX_RANDOM_TIME_MESSAGE = int(os.getenv('MAX_RANDOM_TIME_MESSAGE'))

logging.critical('Loading Tokenizer...')
tokenizer = AutoTokenizer.from_pretrained("luca-martial/DialoGPT-Elon")
generator = pipeline('text-generation', model='huggingtweets/elonmusk')
logging.critical('Loading Tokenizer Done.')
# client = discord.Client(proxy='http://127.0.0.1:7890')
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    game = discord.Game(STATUS)
    await client.change_presence(status=discord.Status.online, activity=game)
    while True:
        random_time = random.randrange(MIN_RANDOM_TIME_MESSAGE, MAX_RANDOM_TIME_MESSAGE)
        chosen_random_message = random.choice(PRE_RANDOM_MESSAGE_LIST)
        channel = client.get_channel(int(RANDOM_MESSAGE_CHANNEL))
        await channel.send(generate_random_message(chosen_random_message))
        await asyncio.sleep(random_time)


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot or message.channel.id not in ALLOWED_CHANNELS:
        return

    # if bot got mentioned or trigger word found
    if client.user.mentioned_in(message) or any(trigger in message.clean_content.lower() for trigger in TRIGGER_LIST):
        _roles = []
        for role in AVAILABLE_ROLES:
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
                await message.channel.send(f"{message.author.mention} {LIMIT_PUBLIC_MESSAGE}")
                # Send DM to user
                await message.author.send(f"{DM_MESSAGE}")
                return

        # if User didnt finished their daily quota
        else:
            # Add append user to the daily list if user is not a collector
            if not _role_check:
                users.append({"id": message.author.id, "time": datetime.now()})
            # Assign users message
            user_message = message.clean_content

            # Assign users message reference
            try:
                user_message_reference = message.reference.resolved.clean_content
            except Exception as e:
                user_message_reference = ""
                print(str(e))
            # Reply user message
            time.sleep(int(os.getenv('MESSAGE_DELAY')))

            # Replace gm to good morning for better understanding
            user_message = user_message.replace("gm", "good morning")
            response = get_mirror_model_response(user_message, user_message_reference)
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


def get_mirror_model_response(user_input, reply_to=""):

    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    bot_input_ids = torch.cat([tokenizer.encode(reply_to + tokenizer.eos_token, return_tensors='pt'),
                               new_user_input_ids],
                              dim=-1) if len(reply_to) > 0 else new_user_input_ids

    message_byte_to_str = tensor_to_string(bot_input_ids)
    s = requests.Session()
    s.trust_env = False
    res = s.post(MODEL_URL, json={"tokens": message_byte_to_str})
    response = res.json()["Response"]
    chat_history_ids = convert_string_to_tensor(response)
    return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)


def tensor_to_string(tensor_object):
    message_in_bytes = tensor_object.numpy()
    message_byte_to_str = json.dumps(message_in_bytes.tolist())
    return message_byte_to_str


def convert_string_to_tensor(string_array):
    _string_to_numpy = np.array(json.loads(string_array))
    _numpy_to_tensor = torch.from_numpy(_string_to_numpy)
    return _numpy_to_tensor


def generate_random_message(chosen_random_message):
    results = generator(chosen_random_message, num_return_sequences=5)
    for sentence in results:
        if '@' in sentence['generated_text']:
            pass
        else:
            print("\nChosen msg: ", sentence['generated_text'])
            return sentence['generated_text']


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)


