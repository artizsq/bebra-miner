# Файл для хранения, изменения, чтения данных


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
            'user_prefix': "Игрок",
            'prefix': [
                "Игрок"
                ]
        }
    save_file('data/users.json', data)




def add_miners(user_id, miner):
    data = read_file('data/users.json')
    try:
        m_data = read_file('data/items/miners.json')
        
    except KeyError:
        config_data = Data()
        m_data = read_file(f'data/{config_data.event_name}/event_miners.json')
        if miner not in data[str(user_id)]['miners']:
            data[str(user_id)]['miners'][miner] = {
                'pow': m_data[miner]['pow'],
                'count': 1
            }
            save_file('data/users.json', data)
        else:
            data[str(user_id)]['miners'][miner]['count'] += 1
            save_file('data/users.json', data)




def add_thousands_separator(number):
    return '{:,}'.format(number).replace(',', ' ')


def get_ability(user_id, prefix):
    data = read_file('data/users.json')
    prefix_data = read_file('data/items/prefixes.json')
    return prefix_data[prefix]['ability']


def retranslate_prefix(prefix):
    data = read_file('data/items/prefixes.json')
    if "add" in data[prefix]['ability'] and not data[prefix]['ability'].startswith('spadd'):
        return f"К вашему текущему фарму прибавляется {data[prefix]['ability'].split('_')[1]}% от общей мощности майнеров."
    elif "speed" in data[prefix]['ability']:
        return f"Вы фармите на {data[prefix]['ability'].split('_')[1]} минут быстрее."
    
    elif "shop" in data[prefix]['ability']:
        return f"Вы получаете скидку {data[prefix]['ability'].split('_')[1]}% при покупке какого-либо товара в магазине."
    
    elif data[prefix]['ability'] == "show_rate":
        return f"Вам будет видно обновления курса BebraCoin'а (На данном моменте не работает)"
    
    elif "spadd" in data[prefix]['ability']:
        return f"К вашему текущему фарму прибавляется {data[prefix]['ability'].split('_')[1]}% от общей мощности майнеров, а также скорость майнинга на {data[prefix]['ability'].split('_')[1]} минут."


def convert_number(number_str):
    number = float(number_str.split('e-')[0]) * (10 ** int(number_str.split('e-')[1]))
    return '{:.5f}'.format(number)

