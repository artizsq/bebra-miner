import json
from utils.parsing import Data

def read_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            users_data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        users_data = {}
    return users_data
    

def save_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def check_user(user_id):
    data = read_file('data/users.json')
    if str(user_id) not in data:
        data[str(user_id)] = {
            'Bbalance': 0,
            'Rbalance': 0,
            'ban': False,
            'miners': {
                "Antminer S9 13.5Th PC": {
                    "pow": 0.0005,
                    'count': 1}
            },
            'clan': None,
            'user_prefix': "Бета-тестер",
            'prefix': [
                "Бета-тестер"
                ]
        }
    save_file('data/users.json', data)


def add_bebra_coins(user_id, amount: int | float):
    data = read_file('data/users.json')
    data[str(user_id)]['Bbalance'] += round(amount, 8)
    data[str(user_id)]['Bbalance'] = round(data[str(user_id)]['Bbalance'], 8)
    save_file('data/users.json', data)


def add_miners(user_id, miner):
    data = read_file('data/users.json')
    try:
        m_data = read_file('data/shop_items.json')
        if miner not in data[str(user_id)]['miners']:
            data[str(user_id)]['miners'][miner] = {
                'pow': m_data[miner]['pow'],
                'count': 1
            }
        else:
            data[str(user_id)]['miners'][miner]['count'] += 1
        save_file('data/users.json', data)
    except KeyError:
        config_data = Data()
        m_data = read_file(f'data/{config_data.event_name}/event_miners.json')
        if miner not in data[str(user_id)]['miners']:
            data[str(user_id)]['miners'][miner] = {
                'pow': m_data[miner]['pow'],
                'count': 1
            }
        else:
            data[str(user_id)]['miners'][miner]['count'] += 1
        save_file('data/users.json', data)


def add_thousands_separator(number):
    return '{:,}'.format(number).replace(',', ' ')