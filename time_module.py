from datetime import datetime, timedelta, date
from datetime import time as time_object
import pytz


# ––––––––-hardcoded variables––––––––
breaks = {0: 10,
          1: 10,
          2: 10,
          3: 20,
          4: 20,
          5: 20,
          6: 20,
          7: 20}
start_time = time_object(8, 20)
time_zone = pytz.timezone('Europe/Moscow')


# ––––––––-backend functions––––––––
add_minutes = lambda time, minutes: (datetime.combine(date(1, 1, 1), time) + timedelta(minutes=minutes)).time()
subtract_times = lambda time1, time2: datetime.combine(date.min, time1) - datetime.combine(date.min, time2)
calculate_lesson_start_time = lambda n: add_minutes(start_time, sum(list(breaks.values())[:n])+40*(n-1)+30)
calculate_lesson_end_time = lambda n:  add_minutes(calculate_lesson_start_time(n), 40)


def strfdelta(tdelta):
    minutes, seconds = divmod(tdelta.seconds, 60)
    return minutes, seconds


# schedule times {№_of_the_lesson: (start_time, end_time)}
# 0th lesson is «Important Talks» 30min session
lesson_schedule = {n: (calculate_lesson_start_time(n), calculate_lesson_end_time(n)) for n in range(1, 9)}
breaks_schedule = {n: (span[1], add_minutes(span[1], breaks[n-1])) for (n, span) in lesson_schedule.items()}
lesson_schedule[0] = (start_time, add_minutes(start_time, 30))


def when_ending(cur_time, current_week_day=1):
    if current_week_day in (5, 6):
        return {"status": "exception", "exception_status": "weekend", "additional_info": current_week_day}
    elif cur_time < lesson_schedule[0][0]:
        return {"status": "exception", "exception_status": "too_early",
                "additional_info": subtract_times(start_time, cur_time)}
    elif cur_time > lesson_schedule[8][0]:
        return {"status": "exception", "exception_status": "too_late", "additional_info": None}

    for n, timespan in lesson_schedule.items():
        if timespan[0] <= cur_time < timespan[1]:
            return {"status": "lesson", "No": n, "time_left": subtract_times(timespan[1], cur_time)}

    for n, timespan in breaks_schedule.items():
        if timespan[0] <= cur_time < timespan[1]:
            return {"status": "break", "No": n, "time_left": subtract_times(timespan[1], cur_time)}


if __name__ == "__main__":
    print(when_ending(datetime.now().time()))
