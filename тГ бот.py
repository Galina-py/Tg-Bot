import telebot
import datetime
import time
import threading
import random
import schedule

bot = telebot.TeleBot(" ")

CHANNEL_ID = -100

# Флаг для контроля запуска потока напоминаний
water_reminders_started = False

schedule_lessons = {
    "monday": "Расписание на понедельник: \n1. Разговор о важном\n2. Анг.язык\n3. История\n4. Математика\n5. Рус.язык\n6. Литература\n7. ф-в Церк.пение\n8. Программирование на Python\n9. Бассейн (16-00)",
    "tuesday": "Расписание на вторник: \n1. Биология\n2. Музыка\n3. Рус.язык\n3. Математика\n4. Физкультура\n5. Рус.язык\n6. Фортепиано (14-15 Ксения)\n7. Сольфеджио (15-00)\n8. Нар.инструменты и Фортепиано (16-30 Дария, Александр)\n9. Гитара (17-10 Александр)\n",
    "wednesday": "Расписание на среду: \n1. Труд\n2. Труд\n3. Математика\n4. Физкультура\n5. ИЗО\n6. Анг.язык\n7. ф-в ЦСЯ\n8. Бассейн (16-00)",
    "thursday": "Расписание на четверг: \n1. История\n2. Математика\n3. Рус.язык\n4. Литература\n5. Математика\n6. География\n7. Анг.язык\n8. ЮнАрмия и Гимнастика (14-30)\n9. Хор в муз.школе (16-50)\n",
    "friday": "Расписание на пятницу: \n1. Рус.язык\n2. Физкультура\n3. Математика\n4. ОПВ\n5. Литература\n6. Программирование на Python\n7. Гитара (17-10 Александр)\n"
}
@bot.message_handler(commands=["start"])
def start_message(message):
    global water_reminders_started
    bot.reply_to(message, 'Привет! Я чат бот, который будет напоминать тебе делать зарядку, пить водичку, а также напомнит расписание на день!')
    chat_id = message.chat.id

    # Проверяем, запущены ли уже напоминания о воде
    if not water_reminders_started:
        water_reminders_started = True

    # Создаем и запускаем поток для напоминаний о воде
    water_reminder_thread = threading.Thread(target=send_water_reminders, args=(chat_id,))
    water_reminder_thread.daemon = True
    water_reminder_thread.start()

    # Создаем и запускаем поток для расписания задач
    schedule_thread = threading.Thread(target=schedule_jobs)
    schedule_thread.start()



@bot.message_handler(commands=['fact'])
def fact_message(message):
    facts = ["Обезвоживание может значительно снизить вашу физическую активность, вызывая усталость, снижение координации и выносливости. Питье достаточного количества воды помогает поддерживать энергию и улучшает общую производительность",
            "Достаточное потребление воды способствует улучшению концентрации, памяти и общего настроения. Даже легкое обезвоживание может ухудшать когнитивные функции и вызывать головные боли",
            "Хороший водный баланс может улучшить внешний вид кожи, придавая ей более здоровый и свежий вид. Это может способствовать уменьшению сухости и улучшению эластичности кожи",
            "Вода необходима для правильного пищеварения и помогает поддерживать здоровье кишечника, предотвращая запоры",
            "Вода помогает почкам эффективно выводить отходы и токсины из организма, поддерживая работу мочевыделительной системы"]
    random_fact = random.choice(facts)
    bot.reply_to(message, f"Лови факт о воде: {random_fact}")

def send_water_reminders(*args, **kwargs):
    first_rem = "09:00"
    second_rem = "14:00"
    end_rem = "18:00"
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == first_rem or now == second_rem or now == end_rem:
            bot.send_message(CHANNEL_ID, "Напоминание - выпей стакан воды")
            time.sleep(61)
        time.sleep(1)

def send_water_fact():
    facts = [
        "Обезвоживание может значительно снизить вашу физическую активность, вызывая усталость, снижение координации и выносливости. Питье достаточного количества воды помогает поддерживать энергию и улучшает общую производительность",
        "Достаточное потребление воды способствует улучшению концентрации, памяти и общего настроения. Даже легкое обезвоживание может ухудшать когнитивные функции и вызывать головные боли",
        "Хороший водный баланс может улучшить внешний вид кожи, придавая ей более здоровый и свежий вид. Это может способствовать уменьшению сухости и улучшению эластичности кожи",
        "Вода необходима для правильного пищеварения и помогает поддерживать здоровье кишечника, предотвращая запоры",
        "Вода помогает почкам эффективно выводить отходы и токсины из организма, поддерживая работу мочевыделительной системы"
    ]
    random_fact = random.choice(facts)
    bot.send_message(CHANNEL_ID, f"Интересный факт о воде: {random_fact}")

def send_schedule_for_next_day():
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%A").lower()
    if tomorrow in schedule_lessons:
        message = schedule_lessons[tomorrow]
        bot.send_message(CHANNEL_ID, message)

def send_exercise_reminder():
    bot.send_message(CHANNEL_ID, "Напоминание: время делать зарядку!")

def schedule_jobs():
    # Напоминание о расписании уроков на следующий день каждый будний день в 15:00
    schedule.every().sunday.at("15:00").do(send_schedule_for_next_day)
    schedule.every().monday.at("15:00").do(send_schedule_for_next_day)
    schedule.every().tuesday.at("15:00").do(send_schedule_for_next_day)
    schedule.every().wednesday.at("15:00").do(send_schedule_for_next_day)
    schedule.every().thursday.at("15:00").do(send_schedule_for_next_day)

    # Напоминание о зарядке каждый день в 6:30
    schedule.every().day.at("06:30").do(send_exercise_reminder)

    schedule.every().day.at("12:00").do(send_water_fact)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    bot.polling(none_stop=True)


