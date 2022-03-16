# mirror_chat_discord_bot

Please create a .env file and add the bellow information

```shell
DISCORD_TOKEN=
DISCORD_GUILD=

# The url for the model
MODEL_URL=

# The role which can freely talk without any limit
AVAILABLE_ROLE=

# amount of time each response will take (Seconds)
MESSAGE_DELAY=

# Number of the amount of responses each none mirror holder has
NUMBER_OF_FREE_RESPONSE=

# Reset response limit time (Minutes)
RESET_RESPONSE_LIMIT_TIME=

# Channels bot allowed to send message to
ALLOWED_CHANNELS='["foo", "bar"]'

# Message that the bot will send as DM to users
DM_MESSAGE='Hey! This is your DM message!'

# End of limit message
LIMIT_PUBLIC_MESSAGE='This is your limit message!'
```

install torch from https://pytorch.org/

Install requirements:
```shell
pip install -r requirements.txt
```


Run the `discordBot.py`, and your bot is live!