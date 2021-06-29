from datetime import date, datetime


class Logger:
    @staticmethod
    def log(message, console=True):
        message_to_write = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}\n"

        if console:
            print(f"{message_to_write}")

        file = open(f"./log/log-{str(date.today())}.txt", "a")
        file.write(f"{message_to_write}")
        file.close()
