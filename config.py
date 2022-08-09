import json
import os


class Config:
    PEGASUS_BASE_URL = os.getenv('PEGASUS_BASE_URL')
    PEGASUS_APP_ID = os.getenv('PEGASUS_APP_ID')
    PEGASUS_ACCESS_TOKEN = os.getenv('PEGASUS_ACCESS_TOKEN')
    PEGASUS_ACCESS_KEY = os.getenv('PEGASUS_ACCESS_KEY')
    PEGASUS_BYRNE_NODE = os.getenv('PEGASUS_BYRNE_NODE')
    PEGASUS_ZAGAN_NODE = os.getenv('PEGASUS_ZAGAN_NODE')
    PEGASUS_SATO_NODE = os.getenv('PEGASUS_SATO_NODE')

    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')
    STATUS = os.getenv('PLAYING_STATUS')
    AVAILABLE_ROLES = json.loads(os.getenv('AVAILABLE_ROLES'))
    ALLOWED_CHANNELS = json.loads(os.getenv('ALLOWED_CHANNELS'))
    DM_MESSAGE = os.getenv('DM_MESSAGE')
    LIMIT_PUBLIC_MESSAGE = os.getenv('LIMIT_PUBLIC_MESSAGE')
    TRIGGER_LIST = json.loads(os.getenv('TRIGGER_LIST'))
    RANDOM_MESSAGE_CHANNEL = os.getenv('RANDOM_MESSAGE_CHANNEL')
    PRE_RANDOM_MESSAGE_LIST = ["Be careful", "Be careful driving", "Don't worry", "Everyone knows it",
                               "Everything is ready", "Excellent", "From time to time", "Good idea",
                               "He's very annoying", "He's very famous", "I can't hear you",
                               "I'd like to go for a walk", "I don't like it", "I don't understand",
                               "I don't want that", "I don't want to bother you", "I feel good", "I have a headache",
                               "I know", "I like her", "I'll pay", "I'll take it", "I lost my watch", "I love you",
                               "I'm an American", "I'm cold", "I'm going to leave", "I'm hungry", "I'm married",
                               "I'm busy", "I'm not ready yet", "I'm not sure", "I'm thirsty",
                               "I'm very busy. I don't have time now", "I need to go home", "I only want a snack",
                               "I thought the clothes were cheaper", "I've been here for two days",
                               "I've heard Texas is a beautiful place", "I've never seen that before", "Just a little",
                               "Just a moment", "Let me check", "Let me think about it", "Let's go have a look",
                               "Never mind", "Next time", "No", "Nonsense", "No, thank you", "Nothing else",
                               "Not recently", "Not yet", "Of course", "Okay", "Please fill out this form",
                               "Please take me to this address", "Please write it down", "Really?  Right here",
                               "Right there", "See you later", "See you tomorrow", "See you tonight", "She's pretty",
                               "Sorry to bother you", "Stop!  Take a chance", "Take it outside", "Tell me",
                               "Thanks for everything", "Thanks for your help", "Thank you", "Thank you miss",
                               "Thank you sir", "Thank you very much", "That looks great", "That's alright",
                               "That's enough", "That's fine", "That's it", "That smells bad", "That's not fair",
                               "That's not right", "That's right", "That's too bad", "That's too many",
                               "That's too much", "The book is under the table", "They'll be right back",
                               "They're the same", "They're very busy", "This doesn't work", "This is very difficult",
                               "This is very important", "Try it", "Very good, thanks", "We like it very much",
                               "You're beautiful", "You're very nice", "You're very smart", "Your things are all here"]
    MIN_RANDOM_TIME_MESSAGE = int(os.getenv('MIN_RANDOM_TIME_MESSAGE'))
    MAX_RANDOM_TIME_MESSAGE = int(os.getenv('MAX_RANDOM_TIME_MESSAGE'))
