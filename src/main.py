import discord
from src.ConfigController import ConfigController


class CustomClient(discord.Client):
    # self.im_variations = ["im", "i'm", "ja som", "som", "i am"]

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        await self.wait_until_ready()

        if message.author == self.user:
            return None

        for i in ConfigController.get_config("im_variations"):
            if message.content.startswith(i + " ", 0):
                await message.channel.send(
                    ConfigController.get_config("message").replace("<name>", message.content.replace(i + " ", ""))
                )


if __name__ == '__main__':
    client = CustomClient()
    # noinspection SpellCheckingInspection
    client.run("ODM5NTYyNzg1MTIwOTc2OTU2.YJLdxg.dKqBhZA-WVl5837gUDhGrwfjO4k")
