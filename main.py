from dotenv import dotenv_values
import discord


class BotKappa(discord.Client):
    async def on_ready(self):
        print('on_ready as {0}'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('`hi'):
            await message.channel.send('uwu')


token = dotenv_values(".env.token")["TOKEN"]

client = BotKappa()
client.run(token)
