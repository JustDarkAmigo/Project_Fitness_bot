import json
import matplotlib.pyplot as plt

def load_data_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def plot_experience_levels(data):
    experience_levels = {
        "Новичок (0-6 мес.)": 0,
        "Любитель (6-24 мес.)": 0,
        "Продвинутый (2-8 лет)": 0,
        "Профессионал (8+ лет)": 0
    }

    for user in data:
        training_level = user["training_level"]
        if training_level == 'новичок':
            experience_levels["Новичок (0-6 мес.)"] += 1
        elif training_level == "любитель":
            experience_levels["Любитель (6-24 мес.)"] += 1
        elif training_level == "продвинутый":
            experience_levels["Продвинутый (2-8 лет)"] += 1
        else:
            experience_levels["Профессионал (8+ лет)"] += 1

    labels = list(experience_levels.keys())
    sizes = list(experience_levels.values())
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']

    plt.figure(figsize=(13, 18))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, shadow=True)
    plt.title('Опытность испытуемых', fontsize=16, fontweight='bold')
    max_category = max(experience_levels, key=experience_levels.get)
    max_count = experience_levels[max_category]
    total_users = sum(experience_levels.values())
    percentage = (max_count / total_users) * 100
    print(f"Больше всего пользователей: '{max_category}' - {max_count} человек ({percentage}%)")
    plt.show()

filename = "users_data_10000_with_levels.json"
data = load_data_from_json(filename)
plot_experience_levels(data)
