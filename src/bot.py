import discord
from json import loads, dumps

from src.database_controller import DatabaseController
from src.logger import Logger


class CustomClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"Connected to Discord as {self.user}!")

    async def on_message(self, message):
        await self.wait_until_ready()

        if message.author == self.user:
            return None

        try:
            # command perform
            if str(message.content).startswith(DatabaseController.get_value(message.guild.name,
                                                                            "command_prefix"), 0, 2):
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
                                                                                        str(message.content).replace(
                                                                                            str(message.content)[
                                                                                            0:len(i)] + " ", ""))
                )

    # TODO idea: change syntax, fe $set-message "Message..."
    # noinspection PyMethodMayBeStatic
    async def perform_command(self, message):
        # we don't want command prefix here
        message_content = str(message.content)[1:]

        if message_content == "help":
            embed = discord.Embed(title="Available Commands", color=discord.Color.blue())

            commands = [
                ["help", "displays help message"],
                ["set-status [true/false]", "Sets bot status"],
                ["set-command-prefix \"<prefix>\"", "Sets command prefix"],
                ["set-message \"<message>\"", "Sets response message"],
                ["add-im-variation \"<variation>\"", "Adds im variation"],
                ["remove-im-variation \"<variation>\"", "Removes im variation"]
            ]

            for command in commands:
                embed.add_field(
                    name=command[0],
                    value=command[1],
                    inline=False
                )

            await message.channel.send(embed=embed)

        elif message_content.startswith("set-status"):
            DatabaseController.set_status(message.guild.name, "f" in message_content.replace("set-status ", ""))

        elif message_content.startswith("set-command-prefix"):
            DatabaseController.set_value(message.guild.name, "command_prefix",
                                         (await self.extract_arguments(message_content))[0])

        elif message_content.startswith("set-message"):
            DatabaseController.set_value(message.guild.name, "message",
                                         (await self.extract_arguments(message_content))[0].replace("'", ""))

        elif message_content.startswith("add-im-variation"):
            im_variations = loads(DatabaseController.get_value(message.guild.name, "im_variations"))
            im_variations.append((await self.extract_arguments(message_content))[0])
            DatabaseController.set_value(message.guild.name, "im_variations", dumps(im_variations))

        elif message_content.startswith("remove-im-variation"):
            im_variations = loads(DatabaseController.get_value(message.guild.name, "im_variations"))
            im_variations.remove((await self.extract_arguments(message_content))[0])
            DatabaseController.set_value(message.guild.name, "im_variations", dumps(im_variations))

        else:
            embed = discord.Embed(title="Command not recognized", color=discord.Color.blue(),
                                  description="Dad-Bot couldn't recognize your command, please check "
                                              "help to get list of all available commands.")

            await message.channel.send(embed=embed)

        # TODO: handle no arguments
        # TODO: finish this function
        # TODO idea: maybe add variable getting (so they can know their im_variations and stuff)

    # noinspection PyMethodMayBeStatic
    async def extract_arguments(self, command: str):
        arguments = []

        current_argument = ""
        record = False

        for char in command:
            if char == "\"":
                if record:
                    arguments.append(current_argument)
                    current_argument = ""

                record = not record

            if record and char != "\"":
                current_argument += char

        return arguments

    async def on_error(self, event, *args, **kwargs):
        Logger.log(
            f"""Error occurred while handling event: {event}
with args: {args}
and kwargs: {kwargs}""")


def run():
    client = CustomClient()

    with open("./token", "r") as file:
        token = file.read()

    token = token.replace("\n", "")
    token = token.replace("\r", "")

    client.run(token)


if __name__ == '__main__':
    run()
