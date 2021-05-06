from json import loads, dumps, JSONDecodeError


class ConfigController:
    @staticmethod
    def read_config():
        with open("config.json", "r") as file:
            try:
                data = loads(file.read())
            except JSONDecodeError:
                data = {}

        return data

    @staticmethod
    def get_config(config):
        data = ConfigController.read_config()

        return data[config]

    @staticmethod
    def set_config(config, value):
        data = ConfigController.read_config()

        data[config] = value

        with open("config.json", "w") as file:
            file.write(dumps(data))

    @staticmethod
    def init_config(server_name):
        data = ConfigController.read_config()

        data[server_name] = {
            "im_variations": ["im", "Im", "i'm", "I'm", "ja som", "som", "i am", "I am"],
            "message": "Hi <name>, I'm Dad!",
            "disabled": False
        }

        with open("config.json", "w") as file:
            file.write(dumps(data))
