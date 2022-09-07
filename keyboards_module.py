from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random


def real_choice(l, number=1):
    random.shuffle(l)
    ll = l[:]
    out = []
    for x in range(number):
        index = random.randint(0, len(ll)-1)
        out.append(ll[index])
        ll.pop(index)
    return out


phrases = ["Сколько мне еще тут разлагаться?",
           "Когда переходим на следуший круг ада?",
           "Скоро еще?",
           "Пааап, сколько еще ехать?"]


def generate_default_keyboard():
    buttons = real_choice(phrases, number=2)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for button in buttons:
        keyboard.add(button)
    return keyboard


if __name__ == "__main__":
    print(generate_default_keyboard)
