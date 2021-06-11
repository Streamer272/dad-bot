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
            # command perform
            if message.content.startswith(DatabaseController.get_value(message.guild.name, "command_prefix"), 0, 2):
                await self.perform_command(message)
                return None

            # is disabled check
            if DatabaseController.get_status(message.guild.name):
                return None

        except TypeError:
            DatabaseController.create_record(message.guild.name, [])

        # sending back message
        for i in loads(DatabaseController.get_value(message.guild.name, "im_variations")):
            if message.content.lower().startswith(i.lower() + " ", 0):
                await message.channel.send(
                    DatabaseController.get_value(message.guild.name, "message").replace("<name>",
                        message.content.replace(message.content[0:len(i)] + " ", ""))
                )

    async def perform_command(self, message):
        # we don't want command prefix here
        message.content = message.content[1:]

        if message.content == "help":
            await message.channel.send("""```
Available commands:
    help - displays help message
    set-status <true/false> - sets bot status
```""")

        elif message.content.startswith("set-status"):
            DatabaseController.set_status(message.guild.name, "f" in message.content.replace("set-status ", ""))

        # TODO: finish this function

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
