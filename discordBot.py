import os
import json
import logging
import time
import torch
import numpy as np
import discord
from transformers import AutoTokenizer
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests as requests

load_dotenv()

# TOKEN = "OTQ2Njc2MzMyNjM1NTE2OTQ5.YhiLCg.iERMYJG72vb7CesL3SpomM20Xpo"
# GUILD = "morty's game server"


TOKEN = "OTQ4MDk3MDE2OTkzNTc0OTQy.Yh22Jw.OC5rjpru7cuGlDYs5q8W7Xyt5nA"
GUILD = "Mirror World"


MODEL_URL = 'http://8.142.23.250:8081/v1/models/kfserving-custom-model:predict'
logging.critical('Loading Tokenizer...')
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
logging.critical('Loading Tokenizer Done.')


client = discord.Client(proxy="http://127.0.0.1:7890")


users = []
dm = []


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    # if bot got mentioned
    if client.user.mentioned_in(message):

        # collector = discord.utils.find(lambda r: r.name == 'Mirror Collector', message.guild.roles)
        collector = discord.utils.find(lambda r: r.name == 'Mirror Collector', message.guild.roles)

        # if User sent more than 5 message today
        if is_user_limited(message.author.id) and collector not in message.author.roles:
            # Delete the message
            await message.delete()
            # if bot didnt DM the user today
            if not did_user_receive_dm(message.author.id):
                # add user to daily DMed list
                dm.append({"id": message.author.id, "time": datetime.now()})
                # Send Message in Channel
                await message.channel.send(f"{message.author.mention} Yo! You finished your daily quota! Check DM to "
                                           f"see how you can continue talking to me!")
                # Send DM to user
                await message.author.send(f"Hey there!\nYou finished your daily quota of talking to me!\nIf you wanna "
                                          "Enjoy talking to me more, you can purchase a mirror from "
                                          "here!\nhttps://mirrorworld.fun/buy?section=top&utm_medium=header\n\n\nAlso "
                                          "note that I'm not gonna send you more messages today and also will delete "
                                          "all new messages you send me in the server until tomorrow! \nCheers!")
                return

        # if User didnt finished their daily quota
        else:
            # Add append user to the daily list if user is not a collector
            if collector not in message.author.roles:
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
            time.sleep(5)
            response = get_mirror_model_response(user_message, user_message_reference)
            # response = "Looking Good!"
            await message.reply(response)
            return
    elif message.content == 'raise-exception':
        raise discord.DiscordException


def is_user_limited(user_id):
    users_history = [x for x in users if x['id'] == user_id and x['time'] > datetime.now() - timedelta(hours=24)]
    # users_history = [x for x in users if x['id'] == user_id and x['time'] > datetime.now() - timedelta(minutes=1)]
    print(f"Number of the time user chatted within 1 minutes: {len(users_history)}")
    if len(users_history) >= 2:
        print("User is limited")
        return True
    print("User is not limited")
    return False


def did_user_receive_dm(user_id):
    users_dm_history = [x for x in dm if x['id'] == user_id and x['time'] > datetime.now() - timedelta(hours=24)]
    # users_dm_history = [x for x in dm if x['id'] == user_id and x['time'] > datetime.now() - timedelta(minutes=1)]
    print(f"Number of the time user got DM within 1 minutes: {len(users_dm_history)}")
    if len(users_dm_history) >= 1:
        print("User Received DM")
        return True
    print("User did not receive DM")
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
    # print(f"str to numpy: {_string_to_numpy}")

    _numpy_to_tensor = torch.from_numpy(_string_to_numpy)
    # print(f"Numpy Back to tensor: {_numpy_to_tensor}")
    return _numpy_to_tensor


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)


