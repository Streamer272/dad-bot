from json import loads, dumps, JSONDecodeError


class ConfigController:
    @staticmethod
    def get_config(config):
        with open("config.json", "r") as file:
            try:
                data = loads(file.read())
            except JSONDecodeError:
                data = {}

        return data[config]

    @staticmethod
    def set_config(config, value):
        with open("config.json", "r") as file:
            data = loads(file.read())

        data[config] = value

        with open("config.json", "w") as file:
            file.write(dumps(data))

    @staticmethod
    def init_config(server_name):
        with open("config.json", "r") as file:
            try:
                data = loads(file.read())
            except JSONDecodeError:
                data = {}

        data[server_name] = {
            "im_variations": ["im", "Im", "i'm", "I'm", "ja som", "som", "i am", "I am"],
            "message": "Hi <name>, I'm Dad!",
            "disabled": False
        }

        with open("config.json", "w") as file:
            file.write(dumps(data))
