import discord
from json import loads as load_json, dumps as dump_json
from typing import List
from functools import cache

from src.database_controller import DatabaseController
from src.logger import Logger
from src.command import Command, Argument


class CustomClient(discord.Client):
    __available_commands: List[Command]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__available_commands = [
            Command("help", "Displays help message",
                    [Argument(0, "\"<command_name>\"", "command name", True, False)],
                    self.help),

            Command("set-status", "Sets bot active status",
                    [Argument(0, "[true/false]", "active value", False, True)],
                    self.set_status),

            Command("set-command-prefix", "Sets bot command prefix",
                    [Argument(0, "\"<prefix>\"", "command prefix", True, True)],
                    self.set_command_prefix),

            Command("set-message", "Sets bot response message",
                    [Argument(0, "\"<message>\"", "response message", True, True)],
                    self.set_message),

            Command("add-im-variation", "Adds im variation",
                    [Argument(0, "\"<im_variation>\"", "im variation", True, True)],
                    self.add_im_variation),

            Command("remove-im-variation", "Removes im variation",
                    [Argument(0, "\"<im_variation>\"", "im variation", True, True)],
                    self.remove_im_variation),

            Command("get-variable", "Displays variable content",
                    [Argument(0, "\"<variable>\"", "variable name", True, True)],
                    self.get_variable),

            # TODO: add edit/get/remove rekt
            Command("create-rekt", "Creates new rekt",
                    [Argument(0, "\"<name>\"", "rekt name", True, True),
                     Argument(1, "\"<on_message>\"", "triggering message", True, True),
                     Argument(2, "\"<response>\"", "rekt response", True, True)],
                    self.create_rekt),
        ]

    async def on_ready(self):
        print(f"Connected to Discord as {self.user}!")

    async def on_message(self, message):
        await self.wait_until_ready()

        if message.author == self.user:
            return None

        try:
            # performing command
            if self.get_message_content(message).startswith(DatabaseController.get_server_value(message.guild.name,
                                                                                   "command_prefix"), 0, 2):
                await self.perform_command(message)
                return None

            # is enabled check
            if not DatabaseController.get_server_status(message.guild.name):
                return None

        except TypeError:
            DatabaseController.create_server(message.guild.name)

        # sending back dad-message
        for i in load_json(DatabaseController.get_server_value(message.guild.name, "im_variations")):
            if self.get_message_content(message).lower().startswith(i.lower() + " ", 0):
                await message.channel.send(
                    DatabaseController.get_server_value(message.guild.name, "message").replace("<name>",
                       self.get_message_content(message).replace(self.get_message_content(message)[0:len(i)] + " ", ""))
                )
                break

        # sending back rekts
        for i in DatabaseController.get_all_rekts(message.guild.name):
            if self.get_message_content(message).lower() == i["on_message"]:
                await message.channel.send(i["response"])
                break

    async def on_error(self, event, *args, **kwargs):
        Logger.log(f"""
        Error occurred while handling event: {event}
            with args: {args}
            and kwargs: {kwargs}
    """)

    # class functions
    async def perform_command(self, message):
        # we don't want command prefix here
        message_content = self.get_message_content(message)[1:]

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
            if (argument.is_string and argument.required) and \
                    (not self.get_argument(message_content, command_to_execute.arguments.index(argument))):
                embed = discord.Embed(title="Error occurred...", color=discord.Color.red(),
                                      description=f"Woah! \"{command_to_execute.name}\" requires an argument, check it "
                                                  f"with help command.")

                await message.channel.send(embed=embed)
                return None

        await command_to_execute.callback(message)

        # TODO: add clear command (clears amount of messages)
        # TODO: add dad-jokes like Joe, Candice etc...

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

    def get_message_content(self, message):
        return str(message.content).replace("'", "")

    # command callbacks
    async def help(self, message):
        if self.get_message_content(message)[1:].replace(" ", "") == "help":
            embed = discord.Embed(title="Available Commands", color=discord.Color.blue())

            for command in self.__available_commands:
                embed.add_field(
                    name=command.name,
                    value=command.description,
                    inline=False
                )

        else:
            command_to_get_help_with_name = self.get_argument(self.get_message_content(message)[1:], 0)
            embed = None

            for command_to_get_help_with in self.__available_commands:
                if command_to_get_help_with.name == command_to_get_help_with_name:
                    embed = discord.Embed(title=f"{command_to_get_help_with_name}", color=discord.Color.blue())
                    embed.add_field(
                        name="Description",
                        value=f"{command_to_get_help_with.description}",
                        inline=False
                    )

                    for argument in command_to_get_help_with.arguments:
                        embed.add_field(
                            name=f"{argument.description}",
                            value=f"{argument.example = }\n{argument.index = }\n{argument.is_string = }\n"
                                  f"{argument.required = }",
                            inline=True
                        )

                    break

            if not embed:
                embed = discord.Embed(title="Error occurred...", color=discord.Color.red(),
                                      description=f"Woah! \"{command_to_get_help_with_name}\" isn't registered in "
                                                  f"list of commands, please check your spelling and try again.")

        await message.channel.send(embed=embed)

    async def set_status(self, message):
        status = self.get_message_content(message)[1:].replace("set-status", "").replace(" ", "")

        if status == "":
            embed = discord.Embed(title="Error occurred...", color=discord.Color.red(),
                                  description=f"Woah! \"set-status\" requires an argument, check it "
                                              f"with help command.")

            await message.channel.send(embed=embed)
            return None

        DatabaseController.set_server_status(message.guild.name, "t" in status)

    async def set_command_prefix(self, message):
        DatabaseController.set_server_value(message.guild.name, "command_prefix",
                                            self.get_argument(self.get_message_content(message)[1:], 0))

    async def set_message(self, message):
        DatabaseController.set_server_value(message.guild.name, "message", self.get_argument(
            self.get_message_content(message)[1:], 0).replace("'", ""))

    async def add_im_variation(self, message):
        im_variations = load_json(DatabaseController.get_server_value(message.guild.name, "im_variations"))
        im_variations.append(self.get_argument(self.get_message_content(message)[1:], 0))
        DatabaseController.set_server_value(message.guild.name, "im_variations", dump_json(im_variations))

    async def remove_im_variation(self, message):
        im_variations = load_json(DatabaseController.get_server_value(message.guild.name, "im_variations"))
        im_variations.remove(self.get_argument(self.get_message_content(message)[1:], 0))
        DatabaseController.set_server_value(message.guild.name, "im_variations", dump_json(im_variations))

    async def get_variable(self, message):
        variables = {
            "command_prefix": DatabaseController.get_server_value(message.guild.name, "command_prefix"),
            "im_variations": DatabaseController.get_server_value(message.guild.name, "im_variations"),
            "message": DatabaseController.get_server_value(message.guild.name, "message"),
            "enabled": bool(DatabaseController.get_server_value(message.guild.name, "enabled")),
            "status": bool(DatabaseController.get_server_value(message.guild.name, "enabled")),
        }

        variable_content = variables.get(self.get_argument(self.get_message_content(message), 0))

        if variable_content is None:
            embed = discord.Embed(title="Error occurred...", color=discord.Color.red(),
                                  description=f"Woah! \"{self.get_argument(self.get_message_content(message), 0)}\" "
                                              f"isn't registered in list of variables, please check your spelling and "
                                              f"try again.")

        else:
            embed = discord.Embed(title=f"{self.get_argument(self.get_message_content(message), 0)}",
                                  color=discord.Color.red(), description=f"{variable_content}")

        await message.channel.send(embed=embed)

    async def create_rekt(self, message):
        DatabaseController.create_rekt(message.guild.name, self.get_argument(self.get_message_content(message), 0),
                                       self.get_argument(self.get_message_content(message), 1),
                                       self.get_argument(self.get_message_content(message), 2))


def run():
    client = CustomClient()

    with open("./token", "r") as file:
        token = file.read()

    token = token.replace("\n", "")
    token = token.replace("\r", "")

    client.run(token)


if __name__ == '__main__':
    run()
