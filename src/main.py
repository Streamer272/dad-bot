import discord
from json import loads, dumps
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
            if str(message.content).startswith(DatabaseController.get_value(message.guild.name, "command_prefix"), 0, 2):
                await self.perform_command(message)
                return None

            # is disabled check
            if DatabaseController.get_status(message.guild.name):
                return None

        except TypeError:
            DatabaseController.create_record(message.guild.name, [])

        # sending back message
        for i in loads(DatabaseController.get_value(message.guild.name, "im_variations")):
            if str(message.content).lower().startswith(i.lower() + " ", 0):
                await message.channel.send(
                    DatabaseController.get_value(message.guild.name, "message").replace("<name>",
                        str(message.content).replace(str(message.content)[0:len(i)] + " ", ""))
                )

    # noinspection PyMethodMayBeStatic
    async def perform_command(self, message):
        # we don't want command prefix here
        message_content = str(message.content)[1:]

        if message_content == "help":
            await message.channel.send("""```
Available commands:
    help - displays help message
    set-status <true/false> - sets bot status
    set-command-prefix <prefix> - sets command prefix
    set-message <message> - sets response message
    add-im-variation <variation> - adds im variation
    remove-im-variation <variation> - removes im variation
```""")

        elif message_content.startswith("set-status"):
            DatabaseController.set_status(message.guild.name, "f" in message_content.replace("set-status ", ""))

        elif message_content.startswith("set-command-prefix"):
            DatabaseController.set_value(message.guild.name, "command_prefix", message_content
                                         .replace("set-command-prefix ", ""))

        elif message_content.startswith("set-message"):
            DatabaseController.set_value(message.guild.name, "message", message_content.replace("set-message ", "")
                                         .replace("'", ""))

        elif message_content.startswith("add-im-variation"):
            im_variations = loads(DatabaseController.get_value(message.guild.name, "im_variations"))
            im_variations.append(message_content.replace("add-im-variation ", ""))
            DatabaseController.set_value(message.guild.name, "im_variations", dumps(im_variations))

        elif message_content.startswith("remove-im-variation"):
            im_variations = loads(DatabaseController.get_value(message.guild.name, "im_variations"))
            im_variations.remove(message_content.replace("remove-im-variation ", ""))
            DatabaseController.set_value(message.guild.name, "im_variations", dumps(im_variations))

        # TODO: finish this function
        # TODO idea: maybe add variable getting (so they can know their im_variations and stuff)

    async def on_error(self, event, *args, **kwargs):
        Logger.log(f"""Error occurred while handling
event: {event}
with args: {args}
and kwargs: {kwargs}""")


if __name__ == '__main__':
    client = CustomClient()

    with open("../token", "r") as file:
        token = file.read()

    token = token.replace("\n", "")
    token = token.replace("\r", "")

    client.run(token)
