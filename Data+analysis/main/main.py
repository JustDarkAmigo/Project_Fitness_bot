# TOKEN = '8322844383:AAEyKzAuHmNMA8SgVYe3l2EKPKnbXgHSxW8'
import json
import os
import random

import requests
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

TOKEN = "8322844383:AAEyKzAuHmNMA8SgVYe3l2EKPKnbXgHSxW8"

USER_FILE = "users.json"
EXERCISE_FILE = "DB.json"

LEVEL = 0
DAYS = 1
GOAL = 2

LEVEL_MAP = {
    "начинающий": "beginner",
    "продвинутый": "intermediate",
    "профессионал": "expert"
}

DAYS_MAP = {
    "2 д/н": "2",
    "3 д/н": "3",
    "4 д/н": "4"
}

GOAL_MAP = {
    "кардиотренировка": "cardio",
    "пауэрлифтинг": "powerlifting",
    "сила": "strength"
}


def load_json(filename):
    file_exists = os.path.exists(filename)
    if not file_exists:
        if filename == USER_FILE:
            return {}
        else:
            return []

    try:
        file_object = open(filename, "r", encoding="utf-8")
        data = json.load(file_object)
        file_object.close()
        return data
    except Exception:
        if filename == USER_FILE:
            return {}
        else:
            return []


def save_json(filename, data):
    file_object = open(filename, "w", encoding="utf-8")
    json.dump(
        data,
        file_object,
        ensure_ascii=False,
        indent=2
    )
    file_object.close()


def update_user_test(user_id, key, value):
    db = load_json(USER_FILE)
    if user_id in db:
        user_data = db[user_id]
        test_data = user_data["test"]
        test_data[key] = value
        save_json(USER_FILE, db)


def get_quote():
    url = "https://zenquotes.io/api/quotes/random"
    try:
        response = requests.get(url)
        status = response.status_code
        if status == 200:
            json_data = response.json()
            first_quote = json_data[0]
            quote_text = first_quote['q']
            quote_author = first_quote['a']

            result_string = "\n\""
            result_string += quote_text
            result_string += "\"\n- "
            result_string += quote_author

            return result_string
        else:
            return ""
    except Exception:
        return ""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    db = load_json(USER_FILE)

    if user_id not in db:
        first_name = user.first_name
        last_name = user.last_name

        full_name = first_name
        if last_name:
            full_name += " " + last_name

        new_user_entry = {}
        new_user_entry["username"] = user.username
        new_user_entry["full_name"] = full_name

        test_info = {}
        test_info["difficulty"] = ""
        test_info["days_p_w"] = ""
        test_info["goal"] = ""

        new_user_entry["test"] = test_info
        new_user_entry["training"] = {}

        db[user_id] = new_user_entry
        save_json(USER_FILE, db)

        message_text = "Привет, " + full_name + f"! Регистрация успешна. \nПройди тест для твоей тренировки!"
    else:
        existing_user = db[user_id]
        saved_name = existing_user["full_name"]
        message_text = "С возвращением, " + saved_name + "!"

    button = KeyboardButton("Пройти тест")
    row = [button]
    keyboard = [row]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(message_text, reply_markup=markup)


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    db = load_json(USER_FILE)

    if user_id not in db:
        await update.message.reply_text("Сначала /start")
        return ConversationHandler.END

    db[user_id]["training"] = {}
    save_json(USER_FILE, db)

    level_options = list(LEVEL_MAP.keys())
    keyboard = [level_options]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"Вопрос 1/3: \nКакой твой уровень подготовки? \n\n"
        f"    Любитель - занимается нерегулярно, либо никак. Опыт до 6 месяцев. Знание базовых движений\n"
        f"    Продвинутый - регулярно занимается. Опыт от 6 месяцев до 4 лет. Уверенное владение разнообразными упражнениями, опыт в секциях.\n"
        f"    Профессионал - регулярно занимается. Опыт от 4 лет. Знание БЖУ, все выше перечисленное."
        f"\n\nВыбери один вариант ответа.",
        reply_markup=markup
    )
    return LEVEL


async def set_difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text not in LEVEL_MAP:
        return LEVEL

    user_id = str(update.effective_user.id)
    value = LEVEL_MAP[text]
    update_user_test(user_id, "difficulty", value)

    days_options = list(DAYS_MAP.keys())
    keyboard = [days_options]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"Вопрос 2/3: Сколько дней в неделю предпочтешь заниматься? \n\n"
        f"    2 - Рекомендовано для любителя, либо для тех, кто хочет только сохранить форму.\n"
        f"    3 - Идеальный вариант для всех категорий.\n"
        f"    4 - Рекомендовано для Профессионалов, либо тех, кто уже так занимался хотя бы месяц.\n"
        f"\n\n выбери один вариант ответа.",
        reply_markup=markup
    )
    return DAYS


async def set_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text not in DAYS_MAP:
        return DAYS

    user_id = str(update.effective_user.id)
    value = DAYS_MAP[text]
    update_user_test(user_id, "days_p_w", value)

    goal_options = list(GOAL_MAP.keys())
    keyboard = [goal_options]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"Вопрос 3/3: Какой тип тренировок тебе подходит? \n\n"
        f"    Кардиотренировка - направлена на жиросжигание и повышение выносливости.\n"
        f"    Пауэрлифтинг - направлен на поднятие больших весов и правильное выполнение техник. (штанга, скамья обязательны!)\n"
        f"    Сила - направлена на повышение мышечной массы и на поддержание мышечного тонуса.\n"
        f"\n\nВыбери один вариант ответа.",
        reply_markup=markup
    )
    return GOAL


async def set_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text not in GOAL_MAP:
        return GOAL

    user_id = str(update.effective_user.id)
    value = GOAL_MAP[text]
    update_user_test(user_id, "goal", value)

    button = KeyboardButton("Посмотреть тренировку")
    row = [button]
    keyboard = [row]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Тест завершен!",
        reply_markup=markup
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardRemove()
    await update.message.reply_text("Отменено.", reply_markup=markup)
    return ConversationHandler.END


async def generate_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    user_db = load_json(USER_FILE)

    if user_id not in user_db:
        await update.message.reply_text("Сначала пройди тест!")
        return

    user_data = user_db[user_id]
    test_results = user_data["test"]
    days_per_week = test_results["days_p_w"]

    if not days_per_week:
        await update.message.reply_text("Сначала пройди тест!")
        return

    existing_training = user_data.get("training", {})

    has_program = False
    if existing_training:
        keys = existing_training.keys()
        for day_k in keys:
            exercises = existing_training[day_k]
            if exercises:
                has_program = True
                break

    if has_program:
        await update.message.reply_text("Нашел твою сохраненную программу:")

        keys = existing_training.keys()
        sorted_days = sorted(keys, key=int)

        for day_key in sorted_days:
            day_msg = "День " + str(day_key) + "\n\n"
            exercises_list = existing_training[day_key]

            for ex in exercises_list:
                name = ex['name']
                eq_list = ex.get("equipments", [])

                if not eq_list:
                    eq_text = "ничего"
                else:
                    eq_text = ", ".join(eq_list)

                day_msg += "- " + name + "\n"
                day_msg += "(Инвентарь: " + eq_text + ")\n\n"

            quote = get_quote()
            day_msg += quote

            await update.message.reply_text(day_msg)

    else:
        days_str = test_results["days_p_w"]
        user_diff = test_results["difficulty"]
        user_goal = test_results["goal"]

        try:
            days_p_w = int(days_str)
        except ValueError:
            return

        ex_count = 3
        if days_p_w == 2:
            ex_count = 4
        elif days_p_w == 3:
            ex_count = 3
        elif days_p_w == 4:
            ex_count = 2

        new_training_data = {}
        for day_num in range(1, days_p_w + 1):
            day_str = str(day_num)
            new_training_data[day_str] = []

        user_db[user_id]["training"] = new_training_data
        save_json(USER_FILE, user_db)

        msg_header = "Твоя новая программа составлена на " + str(days_p_w) + " дня (дней) "
        await update.message.reply_text(msg_header)

        for day in range(1, days_p_w + 1):
            day_msg = "День " + str(day) + "\n\n"
            exercises_db = load_json(EXERCISE_FILE)

            matched_exercises = []
            for ex in exercises_db:
                diff_match = False
                type_match = False

                if ex.get("difficulty") == user_diff:
                    diff_match = True

                if ex.get("type") == user_goal:
                    type_match = True

                if diff_match and type_match:
                    matched_exercises.append(ex)

            if not matched_exercises:
                day_msg += "Нет подходящих упражнений в базе."
            else:
                for i in range(ex_count):
                    random_ex = random.choice(matched_exercises)

                    name = random_ex['name']
                    eq_list = random_ex.get("equipments", [])

                    if not eq_list:
                        eq_text = "ничего"
                    else:
                        eq_text = ", ".join(eq_list)

                    day_msg += "- " + name + "\n"
                    day_msg += "(Инвентарь: " + eq_text + ")\n\n"

                    current_db = load_json(USER_FILE)
                    current_training = current_db[user_id]["training"]
                    day_str = str(day)
                    current_day_list = current_training[day_str]
                    current_day_list.append(random_ex)

                    save_json(USER_FILE, current_db)

            quote = get_quote()
            day_msg += quote

            await update.message.reply_text(day_msg)

    button = KeyboardButton("Пройти тест")
    row = [button]
    keyboard = [row]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    final_text = "Если хочешь сменить программу, пройди тест заново"
    await update.message.reply_text(final_text, reply_markup=markup)


def main():
    builder = Application.builder()
    builder.token(TOKEN)
    application = builder.build()

    regex_filter = filters.Regex("^Пройти тест$")
    entry_point = MessageHandler(regex_filter, start_test)

    state_level_handler = MessageHandler(filters.TEXT, set_difficulty)
    state_days_handler = MessageHandler(filters.TEXT, set_days)
    state_goal_handler = MessageHandler(filters.TEXT, set_goal)

    states_dict = {
        LEVEL: [state_level_handler],
        DAYS: [state_days_handler],
        GOAL: [state_goal_handler]
    }

    cancel_handler = CommandHandler("cancel", cancel)
    fallbacks_list = [cancel_handler]

    conv_handler = ConversationHandler(
        entry_points=[entry_point],
        states=states_dict,
        fallbacks=fallbacks_list
    )

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.add_handler(conv_handler)

    workout_filter = filters.Regex("^Посмотреть тренировку$")
    workout_handler = MessageHandler(workout_filter, generate_workout)
    application.add_handler(workout_handler)

    print("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
