from datetime import date, datetime


class Logger:
    @staticmethod
    def log(message, console=True):
        if console:
            print(f"{datetime.now()}: {message}")

        file = open(f"../log/log-{str(date.today())}.txt", "a")
        file.write(f"{datetime.now()}: {message}\n")
        file.close()
