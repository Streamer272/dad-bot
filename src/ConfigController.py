from json import loads, dumps


class ConfigController:
    @staticmethod
    def get_config(config):
        with open("config.json", "r") as file:
            data = loads(file.read())

        return data[config]

    @staticmethod
    def set_config(config, value):
        with open("config.json", "r") as file:
            data = loads(file.read())

        data[config] = value

        with open("config.json", "w") as file:
            file.write(dumps(data))
