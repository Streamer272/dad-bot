from datetime import datetime


class Date:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.year}-{self.month}-{self.day}." \
               f"{self.hour}:{self.minute}:{self.second}"

    @staticmethod
    def current():
        dt = datetime.now()
        return Date(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    @staticmethod
    def decode(timestamp: str):
        year = timestamp.split(".")[0].split("-")[0]
        month = timestamp.split(".")[0].split("-")[1]
        day = timestamp.split(".")[0].split("-")[2]
        hour = timestamp.split(".")[1].split(":")[0]
        minute = timestamp.split(".")[1].split(":")[1]
        second = timestamp.split(".")[1].split(":")[2]

        return Date(int(year), int(month), int(day), int(hour), int(minute), int(second))
