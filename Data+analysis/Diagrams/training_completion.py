import json

import matplotlib.pyplot as plt
import numpy as np


def load_data_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def plot_training_completion(data):
    with_trainer = []
    without_trainer = []

    for user in data:
        finished_at = user['finished_training_at']
        if isinstance(finished_at, str) and finished_at.startswith('+'):
            finished_at = int(finished_at[1:])
        else:
            finished_at = int(finished_at)

        if user['trainer'] == 'Yes':
            with_trainer.append(finished_at)
        else:
            without_trainer.append(finished_at)

    max_training = 0
    if with_trainer:
        max_training = max(max_training, max(with_trainer))
    if without_trainer:
        max_training = max(max_training, max(without_trainer))

    with_trainer_counts = {}
    without_trainer_counts = {}

    for i in range(1, max_training + 1):
        with_trainer_counts[i] = 0
        without_trainer_counts[i] = 0

    for training_num in with_trainer:
        with_trainer_counts[training_num] = with_trainer_counts.get(training_num, 0) + 1

    for training_num in without_trainer:
        without_trainer_counts[training_num] = without_trainer_counts.get(training_num, 0) + 1

    training_numbers = list(range(1, max_training + 1))
    with_trainer_y = [with_trainer_counts.get(i, 0) for i in training_numbers]
    without_trainer_y = [without_trainer_counts.get(i, 0) for i in training_numbers]

    plt.figure(figsize=(12, 6))
    plt.plot(training_numbers, with_trainer_y, marker='o', linewidth=2, label='С тренером')
    plt.plot(training_numbers, without_trainer_y, marker='s', linewidth=2, label='Без тренера')

    plt.title('Количество пользователей заканчивающих тренировки', fontsize=14, fontweight='bold')
    plt.xlabel('Номер тренировки', fontsize=12)
    plt.ylabel('Количество пользователей', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(training_numbers)
    plt.tight_layout()
    plt.show()

    print(f"Всего пользователей с тренером: {len(with_trainer)}")
    print(f"Всего пользователей без тренера: {len(without_trainer)}")
    print(f"Среднее количество тренировок с тренером: {np.mean(with_trainer):.2f}")
    print(f"Среднее количество тренировок без тренера: {np.mean(without_trainer):.2f}")


filename = "users_data.json"
data = load_data_from_json(filename)
plot_training_completion(data)

