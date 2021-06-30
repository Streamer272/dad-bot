import discord
from json import loads, dumps
from typing import List

from src.database_controller import DatabaseController
from src.logger import Logger
from src.command import Command, Argument


class CustomClient(discord.Client):
    __available_commands: List[Command]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__available_commands = [
            Command("help", "Displays help message", [Argument(0, "\"<command_name>\"", "active value", False,
                                                               False)], self.help),
            Command("set-status", "Sets bot active status", [Argument(0, "[true/false]", "active value", False,
                                                                      True)], self.set_status),
            Command("set-command-prefix", "Sets bot command prefix", [Argument(0, "\"<prefix>\"", "command prefix",
                                                                               True, True)],
                    self.set_command_prefix),
            Command("set-message", "Sets bot response message", [Argument(0, "\"<message>\"", "response message", True,
                                                                          True)],
                    self.set_message),
            Command("add-im-variation", "Adds im variation", [Argument(0, "\"<im_variation>\"", "im variation", True,
                                                                       True)],
                    self.add_im_variation),
            Command("remove-im-variation", "Removes im variation", [Argument(0, "\"<im_variation>\"", "im variation",
                                                                             True, True)],
                    self.remove_im_variation)
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

            # is enabled check
            if DatabaseController.get_status(message.guild.name):
                return None

        except TypeError:
            DatabaseController.create_record(message.guild.name, [])

        # sending back message
        for i in loads(DatabaseController.get_value(message.guild.name, "im_variations")):
            if str(message.content).lower().startswith(i.lower() + " ", 0):
                await message.channel.send(
                    DatabaseController.get_value(message.guild.name, "message").replace("<name>", str(message.content)
                        .replace(str(message.content)[0:len(i)] + " ", ""))
                )

    async def perform_command(self, message):
        # we don't want command prefix here
        message_content = str(message.content)[1:]

        if not message.author.guild_permissions.administrator:
            embed = discord.Embed(title="Not administrator...", color=discord.Color.red(),
                                  description="Dad-Bot only accepts commands from administrators, sorry.")

            await message.channel.send(embed=embed)
            return None

        # checking if command exists
        command_to_execute = None
        for command in self.__available_commands:
            if message_content.startswith(command.name.split(" ")[0]):
                command_to_execute = command
                break

        if not command_to_execute:
            embed = discord.Embed(title="Command not recognized...", color=discord.Color.red(),
                                  description="Dad-Bot couldn't recognize your command, please check "
                                              "help to get list of all available commands.")

            await message.channel.send(embed=embed)
            return None

        # executing command
        for argument in command_to_execute.arguments:
            print(argument)
            if (argument.is_string and argument.required) and (not self.get_argument(message_content, command_to_execute.arguments.index(argument))):
                embed = discord.Embed(title="Error occurred...", color=discord.Color.red(),
                                      description=f"Woah! \"{command_to_execute.name}\" requires an argument, check it "
                                                  f"with help command.")

                await message.channel.send(embed=embed)
                return None

        await command_to_execute.callback(message)

        # TODO: add clear command (clears amount of messages)
        # TODO: add variable getting (so they can know their im_variations and stuff)
        # TODO: add dad-jokes like Joe, Candice etc...

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
        Logger.log(f"""
    Error occurred while handling event: {event}
        with args: {args}
        and kwargs: {kwargs}
""")

    # commands callbacks
    async def help(self, message):
        embed = discord.Embed(title="Available Commands", color=discord.Color.blue())

        for command in self.__available_commands:
            embed.add_field(
                name=command.name,
                value=command.description,
                inline=False
            )

        await message.channel.send(embed=embed)

    async def set_status(self, message):
        status = str(message.content)[1:].replace("set-status", "").replace(" ", "")

        if not status:
            embed = discord.Embed(title="Error occurred...", color=discord.Color.red(),
                                  description=f"Woah! \"set-status\" requires an argument, check it "
                                              f"with help command.")

            await message.channel.send(embed=embed)
            return None

        DatabaseController.set_status(message.guild.name, "f" in status)

    async def set_command_prefix(self, message):
        DatabaseController.set_value(message.guild.name, "command_prefix", self.get_argument(str(message.content)[1:],
                                                                                             0))

    async def set_message(self, message):
        DatabaseController.set_value(message.guild.name, "message", self.get_argument(str(message.content)[1:],
                                                                                      0).replace("'", ""))

    async def add_im_variation(self, message):
        im_variations = loads(DatabaseController.get_value(message.guild.name, "im_variations"))
        im_variations.append(self.get_argument(str(message.content)[1:], 0))
        DatabaseController.set_value(message.guild.name, "im_variations", dumps(im_variations))

    async def remove_im_variation(self, message):
        im_variations = loads(DatabaseController.get_value(message.guild.name, "im_variations"))
        im_variations.remove(self.get_argument(str(message.content)[1:], 0))
        DatabaseController.set_value(message.guild.name, "im_variations", dumps(im_variations))


def run():
    client = CustomClient()

    with open("./token", "r") as file:
        token = file.read()

    token = token.replace("\n", "")
    token = token.replace("\r", "")

    client.run(token)


if __name__ == '__main__':
    run()
