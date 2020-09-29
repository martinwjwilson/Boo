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
        embed = discord.Embed(title=f"-Zer0 Server Community Guidelines-", description=f"""-Zer0 Server Community Guidelines-\n\n

            1.) No Advertising & Self Promoting of any kind.\n
              1.1) This Includes DMs or asking others to advertise in your place.\n\n

            2.) Spamming is not allowed. (enforced by admin discretion)\n
              2.1) Mass Image Drops in channels NSFW Channels, Offtopic, Art & Character Art are
                    exceptions to rule 2.\n\n

            3.) Do not ask to become staff.\n\n

            4.) No mass mentions.\n
              4.1) This includes mentioning staff. If you are not sure which staff to ping for a problem Ping
                     Administrator role. \n\n

            5.) No unicode / blank names. (Visible / Pingable Unicode names are allowed.)\n
               5.1) Names using “The longest single Character” are not allowed.\n
               5.2) Advertising in names & Status are not allowed.\n
               5.3) NSFW & Vulgar Names Are not allowed (enforced by admin discretion)\n
                 5.3.1) Admins reserve the right to Change your nickname in server.\n\n

            6.) No dangerous & shortened links.\n
              6.1) Example: Bit.ly , Goo.gl , ad.fy ect , Ip logging domains.\n\n

            7.) Racism & degrading behavior is not acceptable. (Admins reserve the right to bypass strikes
                And remove the offender if they deem fit.)\n\n

            8.) Be respectful to all users and staff\n\n

            9.) Admins Reserve the right to delete messages & remove members if they see fit.\n
              9.1) This will not be abused, Admins will remove messages that are not appropriate for the
                     Channel / Server / Topic.\n\n

            Strikes will be given to members by admin discretion. 3 Strike Limit. Good Behavior over time can result in strike removal.\n\n

            If you accept these Guidelines type “/verify” in #verify""")
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
        embed1.add_field(name = f"\u200b", value = f"""Sub Freak <:SubFreak:621120929468121091>\n
            Dub Peasant <:DubPeasent:621120916407058462>\n
            Seasonal <:Seasonal:621120929400881165>\n
            Roulette <:Roulette:621120898706964490>\n
            Lewd <:Lewd:621120898564489226>\n""", inline=False)
        channel_roles = await channel.send(embed=embed1)
        # add the emojis to react with
        await channel_roles.add_reaction("<:SubFreak:621120929468121091>")
        await channel_roles.add_reaction("<:DubPeasent:621120916407058462>")
        await channel_roles.add_reaction("<:Seasonal:621120929400881165>")
        await channel_roles.add_reaction("<:Roulette:621120898706964490>")
        await channel_roles.add_reaction("<:Lewd:621120898564489226>")

        # coloured roles
        embed2 = discord.Embed(title=f"Roles!", description=f"React to obtain the following roles:", color=0xaf68c9) # set up embed
        embed2.add_field(name = f"\u200b", value = f"""Blue {config.blue_emoji_id}\n
            Black {config.black_emoji_id}\n
            Yellow {config.yellow_emoji_id}\n
            Pink {config.pink_emoji_id}\n
            Red {config.red_emoji_id}\n
            White {config.white_emoji_id}\n
            Orange {config.orange_emoji_id}\n
            Green {config.green_emoji_id}\n
            Purple {config.purple_emoji_id}\n""", inline=False)
        channel_roles = await channel.send(embed=embed2)
        # add the emojis to react with
        await channel_roles.add_reaction(config.blue_emoji_id)
        await channel_roles.add_reaction(config.black_emoji_id)
        await channel_roles.add_reaction(config.yellow_emoji_id)
        await channel_roles.add_reaction(config.pink_emoji_id)
        await channel_roles.add_reaction(config.red_emoji_id)
        await channel_roles.add_reaction(config.white_emoji_id)
        await channel_roles.add_reaction(config.orange_emoji_id)
        await channel_roles.add_reaction(config.green_emoji_id)
        await channel_roles.add_reaction(config.purple_emoji_id)

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
