import discord
from json import loads, dumps
from typing import List

from src.database_controller import DatabaseController
from src.logger import Logger


class CustomClient(discord.Client):
    __available_commands: List[List[str]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__available_commands = [
                ["help", "displays help message"],
                ["set-status [true/false]", "Sets bot status"],
                ["set-command-prefix \"<prefix>\"", "Sets command prefix"],
                ["set-message \"<message>\"", "Sets response message"],
                ["add-im-variation \"<variation>\"", "Adds im variation"],
                ["remove-im-variation \"<variation>\"", "Removes im variation"]
            ]

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

    # noinspection PyMethodMayBeStatic
    async def perform_command(self, message):
        # we don't want command prefix here
        message_content = str(message.content)[1:]
        first_argument = self.get_argument(message_content, 0)

        # checking if command exists
        command_recognized = False
        for command in self.__available_commands:
            if message_content.startswith(command[0].split(" ")[0]):
                command_recognized = True
                break

        if not command_recognized:
            embed = discord.Embed(title="Command not recognized", color=discord.Color.red(),
                                  description="Dad-Bot couldn't recognize your command, please check "
                                              "help to get list of all available commands.")

            await message.channel.send(embed=embed)
            return None

        # executing commands without first argument
        if message_content == "help":
            embed = discord.Embed(title="Available Commands", color=discord.Color.blue())

            for command in self.__available_commands:
                embed.add_field(
                    name=command[0],
                    value=command[1],
                    inline=False
                )

            await message.channel.send(embed=embed)

        elif message_content.startswith("set-status"):
            DatabaseController.set_status(message.guild.name, "f" in message_content.replace("set-status ", ""))

        # executing commands with first argument
        elif not first_argument:
            embed = discord.Embed(title="Error occurred...", color=discord.Color.red(),
                                  description="Woah! That command requires an argument, check it with help command.")

            await message.channel.send(embed=embed)
            return None

        elif message_content.startswith("set-command-prefix"):
            DatabaseController.set_value(message.guild.name, "command_prefix", first_argument)

        elif message_content.startswith("set-message"):
            DatabaseController.set_value(message.guild.name, "message", first_argument.replace("'", ""))

        elif message_content.startswith("add-im-variation"):
            im_variations = loads(DatabaseController.get_value(message.guild.name, "im_variations"))
            im_variations.append(first_argument)
            DatabaseController.set_value(message.guild.name, "im_variations", dumps(im_variations))

        elif message_content.startswith("remove-im-variation"):
            im_variations = loads(DatabaseController.get_value(message.guild.name, "im_variations"))
            im_variations.remove(first_argument)
            DatabaseController.set_value(message.guild.name, "im_variations", dumps(im_variations))

        # TODO idea: add variable getting (so they can know their im_variations and stuff)

    # noinspection PyMethodMayBeStatic
    def get_argument(self, command: str, index: int):
        # getting arguments
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

        try:
            return arguments[index]

        except IndexError:
            return None

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
