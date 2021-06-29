from datetime import date, datetime
from os import mkdir, path


class Logger:
    @staticmethod
    def log(message, console=True):
        if console:
            print(f"{datetime.now()}: {message}")

        if not path.exists("log"):
            mkdir("log")

        with open(f"./log/log-{str(date.today())}.txt", "a") as file:
            # TODO: remove milliseconds from datetime
            file.write(f"{datetime.now()}: {message}\n")
