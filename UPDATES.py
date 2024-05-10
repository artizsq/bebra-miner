from utils.data import read_file, save_file

data = read_file('data/users.json')
for user in data:
    data[user]['Bbalance'] = 0
    data[user]['Rbalance'] = 0
    data[user]['miners'] = []

save_file('data/users.json', data)