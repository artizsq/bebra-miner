from utils.data import read_file, save_file


data = read_file('data/rate_info.json') 

# 1. С помощью цикла for и условия if:
filtered_data = []
for value in data:
    if value >= 0:
        filtered_data.append(value)

# 2. С помощью list comprehension:
filtered_data = [value for value in data if value >= 0]

# 3. С помощью filter():
filtered_data = list(filter(lambda x: x >= 0, data))

# Вывод отфильтрованных данных
print(filtered_data)
save_file('data/rate_info.json', filtered_data)
