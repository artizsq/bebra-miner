from utils.data import read_file, save_file
from apscheduler.schedulers.background import BackgroundScheduler
import time
import json

# Ваши данные
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

data = read_file('example.json')

def calculate_power():
    for id, user_data in data.items():
        # Расчет общей мощности
        total_power = sum(miner['pow'] * miner['count'] for miner in user_data['miners'].values())

        # Добавление общей мощности к Bbalance
        user_data['Bbalance'] += total_power

    # Сохранение данных
    save_file('example.json', data)

# Создание планировщика
scheduler = BackgroundScheduler()

# Добавление задачи
scheduler.add_job(calculate_power, 'interval', minutes=15)

# Запуск планировщика
scheduler.start()

while True:
    time.sleep(1)


