from time_module import when_ending, strfdelta, time_zone
from datetime import datetime
from datetime import time as time_object


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
        return f"Сейчас перемена перед {end_data['No']+1} уроком." \
               f"\nКонец через {m}:{s}"
