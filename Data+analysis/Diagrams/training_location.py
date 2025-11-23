import json

import matplotlib.pyplot as plt


def load_data_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def plot_training_location(data):
    home_count = 0
    gym_count = 0

    for user in data:
        if user['training_loc'] == 'Home':
            home_count += 1
        elif user['training_loc'] == 'Gym':
            gym_count += 1

    labels = ['Дом', 'Зал']
    counts = [home_count, gym_count]
    colors = ['#ff9999', '#66b3ff']

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, counts, color=colors, alpha=0.7, edgecolor='black')

    plt.title('Соотношение пользователей тренирующихся дома и в зале')
    plt.xlabel('Место тренировки')
    plt.ylabel('Количество пользователей')

    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 str(count), ha='center', va='bottom')

    plt.show()

    total_users = len(data)
    print(f"Всего пользователей: {total_users}")
    print(f"Тренируются дома: {home_count}")
    print(f"Тренируются в зале: {gym_count}")


filename = "users_data.json"
data = load_data_from_json(filename)
plot_training_location(data)

