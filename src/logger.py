from datetime import date, datetime


# TODO idea: maybe try module logging for this?
class Logger:
    @staticmethod
    def log(message, console=True):
        if console:
            print(f"{datetime.now()}: {message}")

        file = open(f"./log/log-{str(date.today())}.txt", "a")
        file.write(f"{datetime.now()}: {message}\n")
        file.close()
