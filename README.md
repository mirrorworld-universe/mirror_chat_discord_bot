# mirror_chat_discord_bot

Please create a .env file and add the bellow information

```shell
DISCORD_TOKEN=
DISCORD_GUILD=

# The url for the model
MODEL_URL=

# The role which can freely talk without any limit
AVAILABLE_ROLES='["959435164545591231", "1241257182471212"]'

# amount of time each response will take (Seconds)
MESSAGE_DELAY=

# Number of the amount of responses each none mirror holder has
NUMBER_OF_FREE_RESPONSE=

# Reset response limit time (Minutes)
RESET_RESPONSE_LIMIT_TIME=

# Channels bot allowed to send message to
ALLOWED_CHANNELS='["959435164545591231", "1241257182471212"]'

# Message that the bot will send as DM to users
DM_MESSAGE='Hey! This is your DM message!'

# End of limit message
LIMIT_PUBLIC_MESSAGE='This is your limit message!'

# Status of the bot for Playing...
PLAYING_STATUS='BOM'

# List of keywords which will trigger the bot to reply to
TRIGGER_LIST='["gm", "get", "hello", "good morning", "good afternoon", "how is everyone", "weather", "hot", "cold", "up to", "market"]'

# Min random interval to send random message to channel (Seconds)
MIN_RANDOM_TIME_MESSAGE = 1800

# Max random interval to send random message to channel (Seconds)
MAX_RANDOM_TIME_MESSAGE = 3600

```

install torch from https://pytorch.org/

Install requirements:
```shell
pip install -r requirements.txt
```


Run the `discordBot.py`, and your bot is live!

## docker build

1. build the docker image using command bellow and please replace the variables to your desired values.

```shell
docker build -t "<Tag:Version>" .
```

2. run the docker image.
```shell
docker run --name <image-name> -e DISCORD_TOKEN='asdawda' -e DISCORD_GUILD='asdfs' -e MODEL_URL='adwwadw' -e AVAILABLE_ROLES='["Foo", "Bar"]' -e MESSAGE_DELAY=10 -e NUMBER_OF_FREE_RESPONSE=10 -e RESET_RESPONSE_LIMIT_TIME=12345 -e ALLOWED_CHANNELS='["foo", "bar"]' -e DM_MESSAGE='Hey! This is your DM message!' -e LIMIT_PUBLIC_MESSAGE='This is your limit message!' -e TRIGGER_LIST='["gm"]' -d <image-name-tag>
```
