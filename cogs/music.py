import discord
from discord.ext import commands, tasks
import asyncio
from discord import FFmpegPCMAudio
import youtube_dl
import os

# setting some important vars
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

# tells ffmpeg to ignore the video
ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_options)

class ytsrc(discord.PCMVolumeTransformer):
    def __init__(self, source, *, info, volume=0.5):
        super().__init__(source, volume)
        self.info       = info
        self.title      = info.get('title')
        self.url        = info.get('url')
        self.thumbnail  = info.get('thumbnail')

    @classmethod
    async def get_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        # gets the first item if link/search contains more than one entry
        if 'entries' in info:
            info = info['entries'][0]

        filename = info['url'] if stream else ytdl.prepare_filename(info)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), info=info)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # pylint: disable=no-member
        self.ytcleanup.start()

    
    @commands.command()
    async def leave(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.send("lol, you gotta be in a voice channel")
        channel = ctx.message.author.voice.channel
        vclient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) # gets voice client for that server
        if vclient and vclient.is_connected():
            await vclient.disconnect()
            print(f"Disconnecting from {channel}.")
        else:
            await ctx.send("I'm not in a voice channel :3")
            return

    @commands.command()
    async def play(self, ctx, *, url):
        if ctx.message.author.voice is None:
            return await ctx.send("lol, you gotta be in a voice channel")
        channel = ctx.message.author.voice.channel
        vclient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if vclient and vclient.is_paused() and vclient.channel == channel:
            return await vclient.resume()
        elif vclient and vclient.is_connected() and vclient.channel == channel:
            print("Already in channel, proceeding to player")
        # checks if voice client is already in a different channel
        elif vclient and vclient.is_connected():
            await vclient.move_to(channel)
            print(f"Moving to {channel}.")
        else:
            vclient = await channel.connect()
            print(f"Joining {channel}.")
        async with ctx.typing():
            player = await ytsrc.get_url(url, loop=self.bot.loop)
            vclient.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        membed = discord.Embed(title="Now Playing:", description=f"{player.title.replace('||', '| |')}")
        membed.set_thumbnail(url=player.thumbnail)
        await ctx.send(embed=membed)


    @commands.command()
    async def volume(self, ctx, vol):
        if ctx.message.author.voice is None:
            return await ctx.send("lol, you gotta be in a voice channel")
        vclient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if vol is None or vol is not None:
            return await ctx.send(f"Current Volume: {vclient.source.volume * 100}")
        vclient.source.volume = vol / 100
        await ctx.send(f"Changed volume to {vol}")
    

    @commands.command()
    async def pause(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.send("lol, you gotta be in a voice channel")
        vclient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        # checks if voice client is playing and user is in same channel
        if vclient and vclient.is_playing() and vclient.channel == ctx.message.author.voice.channel:
            return vclient.pause()
        else:
            return


    @commands.command()
    async def resume(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.send("lol, you gotta be in a voice channel")
        vclient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        # checks if voice client is paused and user is in same channel
        if vclient and vclient.is_paused() and vclient.channel == ctx.message.author.voice.channel:
            return vclient.resume()
        else:
            return
    

    @commands.command()
    async def stop(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.send("lol, you gotta be in a voice channel")
        vclient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        # checks if voice client exists and user is in same channel
        if vclient and vclient.channel == ctx.message.author.voice.channel:
            return vclient.stop()
        else:
            return
    
    def cog_unload(self):
        # pylint: disable=no-member
        self.ytcleanup.cancel()

    @tasks.loop(minutes=60)
    async def ytcleanup(self):
        files = []
        for leftovers in os.listdir('.'):
            if os.path.isfile(leftovers):
                files.append(leftovers)
        toDelete = []
        for f in files:
            if f.startswith("youtube"):
                toDelete.append(f)
        for f in toDelete:
            os.remove(f)
                

def setup(bot):
    bot.add_cog(Music(bot))
