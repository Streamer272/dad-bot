import discord
from json import loads
from src.database_controller import DatabaseController
from src.logger import Logger


class CustomClient(discord.Client):
    command_symbol = "$"

    async def on_ready(self):
        print(f"{self.user} is now running!")

    async def on_message(self, message):
        await self.wait_until_ready()

        if message.author == self.user:
            return None

        try:
            if DatabaseController.get_status(message.guild.name):
                return None

        except TypeError:
            DatabaseController.create_record(message.guild.name, [])

        if message.content.startswith(DatabaseController.get_value(message.guild.name, "command_prefix"), 0, 2):
            await self.perform_command(message)
            return None

        for i in loads(DatabaseController.get_value(message.guild.name, "im_variations")):
            if message.content.lower().startswith(i.lower() + " ", 0):
                await message.channel.send(
                    DatabaseController.get_value(message.guild.name, "message").replace("<name>",
                        message.content.replace(message.content[0:len(i)] + " ", ""))
                )

    # TODO: rewrite this function
    async def perform_command(self, message):
        # if message.content.startswith(self.command_symbol + "disable"):
        #     config = ConfigController.get_config(message.guild.name)
        #     config["disabled"] = True
        #     ConfigController.set_config(message.guild.name, config)
        #
        # elif message.content.startswith(self.command_symbol + "enable"):
        #     config = ConfigController.get_config(message.guild.name)
        #     config["disabled"] = False
        #     ConfigController.set_config(message.guild.name, config)
        #
        # elif message.content.startswith(self.command_symbol + "set-message "):
        #     config = ConfigController.get_config(message.guild.name)
        #     config["message"] = message.content.replace(self.command_symbol + "set-message ", "")
        #     ConfigController.set_config(message.guild.name, config)
        pass

    async def on_error(self, event, *args, **kwargs):
        error_message = f"Error occurred while handling {event} with {args}, {kwargs}"
        Logger.log(error_message)


if __name__ == '__main__':
    client = CustomClient()

    with open("../token", "r") as file:
        token = file.read()

    token = token.replace("\n", "")
    token = token.replace("\r", "")

    client.run(token)
