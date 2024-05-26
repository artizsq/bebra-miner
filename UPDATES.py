from utils.data import read_file, save_file

user_data = read_file('data/users.json')
event_data = read_file('data/beta/event_miners.json')

for user in user_data:
    for miner in user_data[user]['miners']:
        if miner not in event_data:
            user_data[user]['miners'][miner]['event'] = ''

save_file('data/users.json', user_data)

