import json
import os


class Config:
    PEGASUS_BASE_URL = os.getenv('PEGASUS_BASE_URL')
    PEGASUS_APP_ID = os.getenv('PEGASUS_APP_ID')
    PEGASUS_ACCESS_TOKEN = os.getenv('PEGASUS_ACCESS_TOKEN')
    PEGASUS_ACCESS_KEY = os.getenv('PEGASUS_ACCESS_KEY')

    TOKEN = os.getenv('DISCORD_TOKEN')
    STATUS = os.getenv('PLAYING_STATUS')
    AVAILABLE_ROLES = json.loads(os.getenv('AVAILABLE_ROLES'))
    ALLOWED_CHANNELS = json.loads(os.getenv('ALLOWED_CHANNELS'))
    TRIGGER_LIST = json.loads(os.getenv('TRIGGER_LIST'))
