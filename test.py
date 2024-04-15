# from utils.data import read_file, save_file 
# import random

# data = read_file('data/shop.json')
# for items in data:
#     item1 = random.choice(list(data))
# print(item1[0])
# print(item1[0])

from utils.data import read_file, save_file

data = read_file('data/current_shop.json')
print(data[0])