from utils.data import read_file, save_file

data = read_file('data/users.json')
data['2093823215']['prefix'].append('Сися')
save_file('data/users.json', data)
print(data)