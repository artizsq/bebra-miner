# Файл для обновлений 
from utils.data import read_file, save_file

data = read_file('data/items/prefixes.json')
for prefix in data:
    data[prefix]['ability'] = None

save_file('data/items/prefixes.json', data)