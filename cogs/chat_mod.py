import discord
from discord.ext import commands
import banned_language
import utils
import config


class chat_mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # deletes messages containing specific words
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None and message.author.bot != True: # bot exception
            print(f"DM from: {message.author.name}\nContent: ")
            print(message.content)
            return
        if any(bad_word in message.content.lower() for bad_word in banned_language.bad_words):
            await message.delete()
            print("\nbad word!!!\n")
            await message.channel.send("Watch your language!")
            return


    # clears the last x messages
    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def clear(self, ctx, amount):
        channel = ctx.message.channel # get the channel to clear the messages from
        print(f"{ctx.message.author} deleted {amount} messages from {channel}...") # log how many messages are being deleted and from where and by who

        i = 0
        async for message in channel.history():
            if i < (int(amount) + 1):
                i += 1
                await message.delete()

        print("Messages deleted\n")


def setup(bot):
    bot.add_cog(chat_mod(bot))
