# import matplotlib.pyplot as plt
from utils.data import read_file, save_file

# data = read_file('data/rate_info.json')
# rate = []
# for key in data:
#     rate.append(int(key))
#     print(key)
# plt.plot(rate)
# plt.show()

import matplotlib.pyplot as plt
import numpy as np

# # Сгенерируем данные (предположим, что data содержит список значений)
# data = read_file('data/rateinfo.json')
# nums = [10, 20, 30, 40, 50]

# plt.figure(figsize=(8, 5))
# plt.plot(data, nums)

# plt.xlabel('Позиция элемента')
# plt.ylabel('Значение')
# plt.title('График позиции элементов')

# plt.grid(True)
# plt.show()
while True:
    nums = input()
    if nums == "0":
        break
    print(nums.split()[3])
    data = read_file('data/rate_info.json')
    data.append(int(nums.split()[3]))
    save_file('data/rate_info.json', data)


