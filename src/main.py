import discord
from src.ConfigController import ConfigController


class CustomClient(discord.Client):
    command_symbol = "$"

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        await self.wait_until_ready()

        if message.author == self.user:
            return None

        try:
            ConfigController.get_config(message.guild.name)
        except KeyError:
            ConfigController.init_config(message.guild.name)

        if message.content.startswith(self.command_symbol, 0, 2):
            await self.perform_command(message)
            return None

        if ConfigController.get_config(message.guild.name).get("disabled"):
            return None

        for i in ConfigController.get_config(message.guild.name).get("im_variations"):
            if message.content.startswith(i + " ", 0):
                await message.channel.send(
                    ConfigController.get_config(message.guild.name).get("message").replace("<name>",
                                                                                           message.content.replace(
                                                                                               i + " ", ""))
                )

    async def perform_command(self, message):
        if message.content.startswith(self.command_symbol + "disable"):
            config = ConfigController.get_config(message.guild.name)
            config["disabled"] = True
            ConfigController.set_config(message.guild.name, config)

        elif message.content.startswith(self.command_symbol + "enable"):
            config = ConfigController.get_config(message.guild.name)
            config["disabled"] = False
            ConfigController.set_config(message.guild.name, config)

        elif message.content.startswith(self.command_symbol + "set-message "):
            config = ConfigController.get_config(message.guild.name)
            config["message"] = message.content.replace(self.command_symbol + "set-message ", "")
            ConfigController.set_config(message.guild.name, config)


if __name__ == '__main__':
    client = CustomClient()
    # noinspection SpellCheckingInspection
    client.run("ODM5NTYyNzg1MTIwOTc2OTU2.YJLdxg.dKqBhZA-WVl5837gUDhGrwfjO4k")
