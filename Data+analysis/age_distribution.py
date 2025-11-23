import json

import matplotlib.pyplot as plt
import numpy as np


def load_data_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def plot_age_distribution(data):
    ages_with_trainer = []
    ages_without_trainer = []

    for user in data:
        age = user['age']
        if user['trainer'] == 'Yes':
            ages_with_trainer.append(age)
        else:
            ages_without_trainer.append(age)

    plt.figure(figsize=(12, 6))

    min_age = min(min(ages_with_trainer) if ages_with_trainer else 0,
                  min(ages_without_trainer) if ages_without_trainer else 0)
    max_age = max(max(ages_with_trainer) if ages_with_trainer else 0,
                  max(ages_without_trainer) if ages_without_trainer else 0)

    bins = range(min_age, max_age + 2)

    plt.hist(ages_with_trainer, bins=bins, alpha=0.7, label='С тренером',
             color='blue', edgecolor='black')
    plt.hist(ages_without_trainer, bins=bins, alpha=0.7, label='Без тренера',
             color='red', edgecolor='black')

    plt.title('Распределение возраста пользователей', fontsize=14, fontweight='bold')
    plt.xlabel('Возраст', fontsize=12)
    plt.ylabel('Количество пользователей', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("Статистика по возрасту:")
    print(f"С тренером: средний возраст = {np.mean(ages_with_trainer):.1f} лет, "
          f"медиана = {np.median(ages_with_trainer):.1f} лет")
    print(f"Без тренера: средний возраст = {np.mean(ages_without_trainer):.1f} лет, "
          f"медиана = {np.median(ages_without_trainer):.1f} лет")


filename = "users_data_10000_with_levels.json"
data = load_data_from_json(filename)
plot_age_distribution(data)
