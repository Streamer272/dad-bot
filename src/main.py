import discord
from src.ConfigController import ConfigController


class CustomClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        await self.wait_until_ready()

        try:
            ConfigController.get_config(message.guild.name)
        except KeyError:
            ConfigController.init_config(message.guild.name)

        if message.author == self.user:
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


if __name__ == '__main__':
    client = CustomClient()
    # noinspection SpellCheckingInspection
    client.run("ODM5NTYyNzg1MTIwOTc2OTU2.YJLdxg.dKqBhZA-WVl5837gUDhGrwfjO4k")
