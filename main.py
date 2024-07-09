import json
import random

import telebot

TOKEN = "7399119202:AAF2PsqjlwD4m8dX0SPg5mCGQsPFkUIswtM"

bot = telebot.TeleBot(TOKEN)

try:
    with open("user_data.json", "r", encoding="utf-8") as file:
        user_data = json.load(file)
except:
    user_data = {}

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это твой бот.Скоро я буду уметь много нового!")

@bot.message_handler(commands=["learn"])
def handle_learn(message):
    bot.send_message(message.chat.id, "Обучение сейчас начнется!")
    user_words = user_data.get(str(message.chat.id), {})

    words_number = int(message.text.split()[1])

    word = random.choice(list(user_words.keys()))

    bot.send_message(message.chat.id, word)


    ask_translation(message.chat.id, user_words, words_number)

def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id, f"Напиши перевод слова '{word}'.")

        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left)
    else:
        bot.send_message(chat_id, "Урок закончен")


def lower():
    pass


def check_translation(message, expected_translation, words_left):
    user_translation = message.text.strip().lower()
    if user_translation == expected_translation.lower():
        bot.send_message(message.chat.id, "Правильно!Молодец!")
    else:
        bot.send_message(message.chat.id, f"Неправильно.Правильный перевод {expected_translation}")
    ask_translation(message.chat.id, user_data[str(message.chat_id)], words_left)






@bot.message_handler(commands=["addword"]) #addword apple яблоко
def handle_addword(message):
    global user_data
    chat_id = message.chat.id
    user_dict = user_data.get(chat_id, {})

    words = message.text.split()[1:]
    if len(words) == 2:
        word, translation = words[0].lower(), words[1].lower()
        user_dict[word] = translation

        user_data[chat_id] = user_dict

        with open("user_data.json", "w", encoding="utf-8") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)
        bot.send_message(chat_id, f"Слово '{word}' добавлено в словарь")
    else:
        bot.send_message(chat_id, "Произошла ошибка.Попробуйте снова")


@bot.message_handler(commands=["help"])
def handle_start(message):
    bot.send_message(message.chat.id, "Этот бот создан для изучения английского языка.\n"
                                           "В нем есть команды learn.\n"
                                           "Автор : Володина Вася")



@bot.message_handler(func= lambda message: True)
def handle_all(message):
    if message.text.lower() == "пока":
        bot.send_message(message.chat.id, "Спектакль окончен! Гаааснет свет! И многоточий бооольшее нет!")
    elif message.text.lower() == "расскажи стих":
        bot.send_message(message.chat.id, "Муха села на варенье, вот и все стихотворение :)")
    elif message.text.lower() == "а что мы будем танцевать?":
        bot.send_message(message.chat.id, "Вальс конечно же вальс")
    elif message.text.lower() == "погода":
        bot.send_message(message.chat.id, "+29 > > > Сейчас будет жара а а а ")


if __name__ == "__main__":
    bot.polling(none_stop=True)