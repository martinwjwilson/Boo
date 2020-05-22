import discord
from discord.ext import commands
import utils
import config


class update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def update_rules(self, ctx):
        # update the rules channel with any updates
        lewd_role = ctx.guild.get_role(513436281523404825)
        embed = discord.Embed(title=f"-Zer0 Server Community Guidelines-", description=f"""1. No Advertising & Self Promoting of any kind.\n
            2. Spamming is not allowed.\n
            3. Do not ask to become staff.\n
            4. No mass mentions.\n
            5. No unicode / blank names. (Visable / Pingable Unicode names are allowed.)\n
            6. No dangerous & shortened links.\n
            7. Racism & degrading behavior is not acceptable.\n\n
            Channel Rules of Use are in all channel descriptions.""", color=0xaf68c9) # set up embed
        embed.add_field(name = "TO VERIFY USE THE COMMAND", value = f"/verify", inline = False)
        embed.add_field(name = "ROLES", value = f"You can grab yourself a Color Role and Identifer Roles in <#{config.channel_dict.get('auto_role')}>. Lewd and Roulette Gives you access to there respective channels.", inline = False)
        embed.add_field(name = "WARNINGS", value = f"All users have a 3 Strike warning. Admins can bypass this and Choose to ban a user if they see fit.\naka Obvious Trolling/Bot accounts.", inline = False)
        embed.add_field(name = "WAIFU ROULETTE", value = f"<#{config.channel_dict.get('waifu_roulette')}> Harems will reset every 6 Months.\n\nThe Score leader Board will be posted in <#{config.channel_dict.get('announcements')}> at the end of every round and recive a uniqe role.", inline = False)
        await ctx.send(embed=embed)


    @commands.command(pass_context = True, hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def update_roles(self, ctx):
        # delete existing messages
        channel = self.bot.get_channel(config.channel_dict["auto_role"]) # get the channel to clear the messages from
        i = 0
        async for message in channel.history():
            if i < (2):
                i += 1
                await message.delete()
        print("Roles channel cleared\n")

        # update the roles channel for autoroles
        embed1 = discord.Embed(title=f"Roles!", description=f"React to obtain the following roles:", color=0xaf68c9) # set up embed
        embed1.add_field(name = f"\u200b", value = f"""Sub Freak {config.sub_emoji_id}\n
            Dub Peasant {config.dub_emoji_id}\n
            Seasonal {config.seasonal_emoji_id}\n
            Roulette {config.roulette_emoji_id}\n
            Lewd {config.lewd_emoji_id}\n""", inline=False)
        channel_roles = await channel.send(embed=embed1)
        # add the emojis to react with
        await channel_roles.add_reaction(config.sub_emoji_id)
        await channel_roles.add_reaction(config.dub_emoji_id)
        await channel_roles.add_reaction(config.seasonal_emoji_id)
        await channel_roles.add_reaction(config.roulette_emoji_id)
        await channel_roles.add_reaction(config.lewd_emoji_id)

        # coloured roles
        # embed2 = discord.Embed(title=f"Roles!", description=f"React to obtain the following roles:", color=0xaf68c9) # set up embed
        # embed2.add_field(name = f"\u200b", value = f"""Blue {config.blue_emoji_id}\n
        #     Black {config.black_emoji_id}\n
        #     Yellow {config.yellow_emoji_id}\n
        #     Pink {config.pink_emoji_id}\n
        #     Red {config.red_emoji_id}\n
        #     White {config.white_emoji_id}\n
        #     Orange {config.orange_emoji_id}\n
        #     Green {config.green_emoji_id}\n
        #     Purple {config.purple_emoji_id}\n""", inline=False)
        # channel_roles = await channel.send(embed=embed2)
        # # add the emojis to react with
        # await channel_roles.add_reaction(config.blue_emoji_id)
        # await channel_roles.add_reaction(config.black_emoji_id)
        # await channel_roles.add_reaction(config.yellow_emoji_id)
        # await channel_roles.add_reaction(config.pink_emoji_id)
        # await channel_roles.add_reaction(config.red_emoji_id)
        # await channel_roles.add_reaction(config.white_emoji_id)
        # await channel_roles.add_reaction(config.orange_emoji_id)
        # await channel_roles.add_reaction(config.green_emoji_id)
        # await channel_roles.add_reaction(config.purple_emoji_id)

        # seasonal roles
        # embed1 = discord.Embed(title=f"Roles!", description=f"React to obtain the following roles:", color=0xaf68c9) # set up embed
        # embed1.add_field(name = f"\u200b", value = f"""Virgin Succubus {config.succubus_emoji_id}\n
        #     Skeletal Ruler {config.skeletal_emoji_id}\n
        #     Loli Vampire {config.vampire_emoji_id}\n
        #     Elfen Twins {config.twins_emoji_id}""", inline=False)
        # channel_roles = await channel.send(embed=embed1)
        # # add the emojis to react with
        # await channel_roles.add_reaction(config.succubus_emoji_id)
        # await channel_roles.add_reaction(config.skeletal_emoji_id)
        # await channel_roles.add_reaction(config.vampire_emoji_id)
        # await channel_roles.add_reaction(config.twins_emoji_id)


def setup(bot):
    bot.add_cog(update(bot))
