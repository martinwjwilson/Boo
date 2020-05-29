import discord
from discord.ext import commands
import asyncio
import json
import utils
import users
import config
import logging
import time


class member_moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # conversion to seconds for use with unix epoch ie time()
    def convtime(self, toconv):
        numstr = ""
        for i in range(0, len(toconv)):
            if toconv[i].isdigit():
                numstr = numstr + toconv[i]
        if toconv.endswith("s"): # seconds
            num = int(numstr)
        elif toconv.endswith("m"): # minutes
            num = int(numstr) * 60
        elif toconv.endswith("h"): # hours
            num = int(numstr) * (60^2)
        elif toconv.endswith("d"): # days
            num = int(numstr) * 24 * (60^2)
        elif toconv.endswith("w"): # weeks
            num = int(numstr) * 7 * 24 * (60^2)
        elif toconv.endswith("M"): # months
            num = int(numstr) * 30 * 24 * (60^2)
        elif toconv.endswith("y"): # years
            num = int(numstr) * 365 * 24 * (60^2)
        return num

    # used to create the base record
    def createRecord(self, ctx, member, isMuted=0, timer=0, muteReason='None', warnings=0):
        with open('records.json') as f:
            data = json.load(f)
        data.append( {  'id': member.id,
                        'name': str(member.display_name),
                        'isMuted': isMuted,
                        'timer': timer,
                        'muteReason': muteReason,
                        'warnings': warnings} )
        with open('records.json', 'w') as f:
            json.dump(data, f, indent = 2)
        with open('records.json') as f:
            data = json.load(f)
            return data

    # DO NOT USE UNLESS FILLING RECORDS FOR FIRST TIME
    # IT WILL CREATE DUPLICATES IF YOU DO
    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("red_panda"))
    async def addalltorecords(self, ctx):
        gmem = ctx.guild.members
        async with ctx.channel.typing():
            for member in gmem:
                self.createRecord(ctx, member)
            await ctx.send("done")

    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def record(self, ctx, message=None):
        if ctx.message.channel.id == config.channel_dict.get("adminchannel"):
            if message is not None:
                member = ctx.message.mentions[0]
            if message is None:
                member = ctx.message.author
            record_exists = False
            with open('records.json') as f:
                data = json.load(f)
            for user in data:
                if user['id'] == member.id:
                    embed = discord.Embed(title=f"{member.display_name}'s Record", description=f"{member.mention}")
                    embed.set_thumbnail(url=member.avatar_url)
                    if user['isMuted'] == 1:
                        embed.add_field(name="isMuted:", value=user['isMuted'], inline=False)
                        embed.add_field(name="Time Left:", value=f"{user['timer']-time():.2f} seconds remaining", inline=False)
                        embed.add_field(name="muteReason:", value=f"{user['muteReason']}")
                    embed.add_field(name="Warnings:", value=user['warnings'], inline=False)
                    record_exists = True
            if record_exists != True:
                data = self.createRecord(ctx, member)
                embed = discord.Embed(title=f"{member.display_name}'s Record", description=f"{member.mention}")
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name="isMuted:", value=user['isMuted'], inline=False)
                embed.add_field(name="Warnings:", value=user['warnings'], inline=False)


    # verify command
    @commands.command(hidden = True)
    async def verify(self, ctx):
        if ctx.message.channel.id == config.channel_dict["verify"]:
            user = ctx.message.author
            entrance = self.bot.get_channel(config.channel_dict["entrance"])
            add_role = discord.utils.get(ctx.guild.roles, name = "Member")
            await user.add_roles(add_role)
            print(f"The role {add_role} was added to {user}")
            await asyncio.sleep(1)
            rmv_role = discord.utils.get(ctx.guild.roles, name = "Temp")
            await user.remove_roles(rmv_role)
            print(f"The role {rmv_role} was removed from {user}")
            with open("records.json") as f:
                data = json.load(f)
            if user.id not in data: #checks if user is in database
                self.createRecord(ctx, user)
                print(f"{user} was successfully added to our records.")
            # Server greeting when user verifies
            await entrance.send(f"<@{user.id}> just joined the server!")


    # mute specific user
    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def mute(self, ctx, mute_user, length="24h", *, reason="None Provided."):
        lenginsec = self.convtime(length)
        user_to_mute = ctx.message.mentions[0] # id of person to mute that was mentioned in command
        mute_role = discord.utils.get(ctx.guild.roles, id = config.role_dict.get("Muted")) # get the role to apply
        record_exists = False
        # load the json file
        with open('records.json') as f:
            data = json.load(f)
        # search for the warned user
        for user in data:
            if user['id'] == user_to_mute.id: # if the user id sent matches the one in the json file
                user['isMuted'] = 1
                user['timer'] = time() + lenginsec
                user['muteReason'] = reason
                record_exists = True # record has been found
        # if no record exists for the mentioned user
        if record_exists != True:
            data = self.createRecord(ctx, user_to_mute, isMuted=1, timer=time() + lenginsec, muteReason=reason)
        # write the edited dict to the json file
        with open('records.json', 'w') as f:
            json.dump(data, f, indent = 2)
        await user_to_mute.add_roles(mute_role) # assign the role
        await ctx.send(f"{ctx.message.author} has muted {user_to_mute} for {length}")


    # unmute specific user
    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def unmute(self, ctx, unmute_user):
        user_to_unmute = ctx.message.mentions[0] # id of person to unmute that was mentioned in command
        unmute_role = discord.utils.get(ctx.guild.roles, id = config.role_dict.get("Muted")) # get the role to apply
        record_exists = False
        # load the json file
        with open('records.json') as f:
            data = json.load(f)
        for user in data:
            if user['id'] == user_to_unmute.id: # if the user id sent matches the one in the json file
                user['timer'] = 0
                user['isMuted'] = 0
                user['muteReason'] = "None"
                record_exists = True # record has been found
        # if no record exists for the mentioned user
        if record_exists != True:
            data = self.createRecord(ctx, user_to_unmute)
        with open('records.json', 'w') as f:
            json.dump(data, f, indent = 2)
        await user_to_unmute.remove_roles(unmute_role) # remove the role
        await ctx.send(f"{ctx.message.author} has unmuted {user_to_unmute}")


    # warn specific user
    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def warn(self, ctx, warneduser):
        warning_id      = ctx.message.mentions[0].id # id of person to that was warned
        # load the json file
        with open('records.json') as f:
            data = json.load(f)
        record_exists = False
        # search for the warned user
        for user in data:
            if user['id'] == warning_id: # if the warning id sent matches the one in the json file
                # increase the users warning count
                user['warnings'] += 1
                await ctx.send(f"{user['name']} now has {user['warnings']} warnings.") # discord
                record_exists = True # record has been found
        # if no record exists for the mentioned user
        if record_exists != True:
            data = self.createRecord(ctx, ctx.message.mentions[0], warnings=1)
            await ctx.send(f"{user['name']} now has {user['warnings']} warnings.") # discord
        # write the edited dict to the json file
        with open('records.json', 'w') as f:
            json.dump(data, f, indent = 2)


    # remove warning from specific user
    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def unwarn(self, ctx, warneduser):
        warning_id      = ctx.message.mentions[0].id # id of person to that was warned
        # load the json file
        with open('records.json') as f:
            data = json.load(f)
        # search for the warned user
        for user in data:
            if user['id'] == warning_id: # if the warning id sent mathes the one in the json file
                if user['warnings'] == 0:
                    await ctx.send(f"{user['name']} doesnt have any warnings!") # discord
                    continue
                # decrements the users warning count
                user['warnings'] -= 1
                await ctx.send(f"{user['name']} now has {user['warnings']} warnings.") # discord
        # write the edited dict to the json file
        with open('records.json', 'w') as f:
            json.dump(data, f, indent = 2)


    # kick mentioned user
    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def kick(self, ctx, ban_user, *, words):
        await ctx.message.mentions[0].kick(reason = words)


    # ban mentioned user
    @commands.command(hidden = True)
    @commands.has_role(config.role_dict.get("admin"))
    async def ban(self, ctx, ban_user):
        await ctx.message.mentions[0].ban()


    # assign roles based on adding a reaction
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # variables
        guild   = self.bot.get_guild(payload.guild_id)
        user    = guild.get_member(payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)

        if payload.user_id != users.users_dict["Booette"]: # reaction author wasn't bot
            if payload.channel_id == config.channel_dict["auto_role"]: # in the role channel
                role_to_add = discord.utils.get(channel.guild.roles, id = config.role_dict.get(str(payload.emoji)))
                await user.add_roles(role_to_add) # add role to user depending on the reaction emoji
                await self.bot.get_channel(config.channel_dict["logs"]).send(embed=self.role_embed("added.", user, role_to_add))


    # remove roles based on removing a reaction
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # variables
        guild   = self.bot.get_guild(payload.guild_id)
        user    = guild.get_member(payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)

        if payload.channel_id == config.channel_dict["auto_role"]:
            role_to_remove = discord.utils.get(channel.guild.roles, id = config.role_dict.get(str(payload.emoji)))
            await user.remove_roles(role_to_remove) # remove role to user depending on the reaction emoji
            await self.bot.get_channel(config.channel_dict["logs"]).send(embed=self.role_embed("removed.", user, role_to_remove))


    # post an embed logging someone getting/losing a role
    def role_embed(self, status, user, role):
        embed = discord.Embed(title = "Role Change", description = f"<@{user.id}> had the role {role.name} {status}", color=0xaf68c9)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"ID: {user.id}")
        return embed


    # a new member joins
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # welcome new user
        # message destinations
        new_member = await self.bot.fetch_user(member.id)
        # send messages
        await new_member.send("BOO! Welcome to Zer0!\nPlease read through our rules page then type `/verify` into the #verify channel to access the server")

        # log
        embed = discord.Embed(title="Member Joined", description=f"<@{new_member.id}> {new_member.name}", color=0xaf68c9) # set up embed
        embed.set_thumbnail(url=new_member.avatar_url)
        embed.add_field(name = "Account Creation", value = new_member.created_at.strftime("%c"), inline = False)
        embed.set_footer(text=f"ID: {new_member.id}")
        await self.bot.get_channel(config.channel_dict["logs"]).send(embed=embed)

        # auto assign role to new member
        add_role = discord.utils.get(member.guild.roles, name = "Temp")
        await member.add_roles(add_role)


    # a member leaves
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # log
        embed = discord.Embed(title="Member Left", description=f"<@{member.id}> {member.name}", color=0xaf68c9) # set up embed
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"ID: {member.id}")
        await self.bot.get_channel(config.channel_dict["logs"]).send(embed=embed)


def setup(bot):
    bot.add_cog(member_moderation(bot))
