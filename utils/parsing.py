from configparser import ConfigParser
from typing import List

def get_config():
    config = ConfigParser()
    config.read('data/config.ini', encoding='utf-8')
    return config


class Data:
    def __init__(self):
        self.config = get_config()
        self.admin_ids: List[str] = self.config.get('Telegram', 'admin_ids').split(',') 
        self.TOKEN = self.config.get('Telegram', 'TOKEN')
        self.rate = self.config.getint('Bot', 'rate')
        self.isEvent = self.config.getboolean('Bot', 'event')
        self.event_name = self.config.get('Bot', 'event_name')

    def update(self, section, option, value):
        self.config.set(section, option, str(value))

        with open('data/config.ini', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
