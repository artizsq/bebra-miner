# Файл для обновлений 
from utils.data import read_file, save_file

data = read_file('data/users.json')
for user in data:
    data[user]['Rbalance'] = 100000
    data[user]['miners'] = {
                "Antminer S9 13.5Th PC": {
                    "pow": 0.0005,
                    'count': 1}
            }
save_file('data/users.json', data)