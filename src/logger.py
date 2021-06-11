from datetime import datetime


class Logger:
    @staticmethod
    def log(message):
        with open(f"../log/log-{datetime.now()}", "w") as file:
            file.write(f"{datetime.now().time()}: {message}")
