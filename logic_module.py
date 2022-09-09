from time_module import when_ending, strfdelta
from time_module import time_zone, breaks_schedule, lesson_schedule
from datetime import datetime
from sql_module import db_row_exists, db_create_new_row, db_update_time, db_select_column


def get_time():
    end_data = when_ending(datetime.now(time_zone).time(), datetime.today().weekday())

    if end_data['status'] == 'exception':
        if end_data['exception_status'] == "weekend":
            weekday = "субботу" if end_data['additional_info'] == 5 else "воскресенье"
            return f"Не понимаю, что ты делаешь в школе в {weekday}.\nДаже в выходные покоя не дают(("

        elif end_data['exception_status'] == "too_late":
            return f"Баста. Уроки закончились, можешь отдыхать спокойно"

        elif end_data['exception_status'] == "too_early":
            h, m, s = str(end_data['additional_info']).split(':')
            return f"Куда ты в такую рань собрался!" \
                   f"\nУ тебя еще {h}ч. {m}мин. до начала «<b><i>Важных</i></b> разговоров»"

    elif end_data['status'] == 'lesson':
        m, s = strfdelta(end_data['time_left'])
        return f"Сейчас идет {end_data['No']} урок." \
               f"\nКонец через {m}:{s}"

    elif end_data['status'] == 'break':
        m, s = strfdelta(end_data['time_left'])
        return f"Сейчас перемена перед {end_data['No'] + 1} уроком." \
               f"\nКонец через {m}:{s}"


def get_timetable():
    return "\n".join(f"Урок №{x[0]}: {str(x[1][0])[:-3]}–{str(x[1][1])[:-3]}"
                     for x in sorted(lesson_schedule.items(), key=lambda x: x[0])
                     ).replace("Урок №0", "<b><i>Важные разговоры</i></b>")


def new_user(m):
    if not db_row_exists(m.chat.id):
        name = "None" if not m.chat.first_name else m.chat.first_name
        username = "None" if not m.chat.username else m.chat.username

        db_create_new_row(m.chat.id, name, username)


def update_time_used(m):
    timestamp = datetime.now(time_zone)
    db_update_time(m.chat.id, timestamp)


def get_statistics():
    names = db_select_column("user_name")
    usernames = db_select_column("user_username")
    data = db_select_column("last_data")
    statistics = "\n".join([f"{x[0][0]} – @{x[1][0]} {x[2][0][:-13]}" if x[1][0] != "None"
                            else f"{x[0][0]} – no username {x[2][0][:-13]}"
                            for x in list(zip(names, usernames, data))])
    return statistics


if __name__ == "__main__":
    print(get_timetable())