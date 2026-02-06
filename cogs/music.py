import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    @commands.command()
    async def play(self, ctx, *, query):
        url = ""

        ydl_opts = {
            "format": "b",
            "noplaylist": True,
            "quiet": True,
            "default_search": "ytsearch1",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, query, download = False)
            url = info["entries"][0]["url"] if 'entries' in info else info['url']
                
        title = info["entries"][0]["title"]

        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = []

        self.queues[ctx.guild.id].append({"url": url, "title": title})

        vc = ctx.guild.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
            await ctx.send(f"Joined {ctx.author.voice.channel.name}!")

        if not vc.is_playing():
            self.play_next(ctx)
        else:
            await ctx.send(f"Queued: {title}")

    def play_next(self, ctx):
        queue = self.queues.get(ctx.guild.id)
        if queue and len(queue) > 0:
            song = queue.pop(0)
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn -ar 48000 -ac 2 -f s16le'
            }
            vc = ctx.guild.voice_client
            audio_source = discord.FFmpegPCMAudio(song["url"], **ffmpeg_options)
            vc.play(audio_source, after=lambda e: self.play_next(ctx))
            asyncio.run_coroutine_threadsafe(
                ctx.send(f"Now playing: {song['title']}"), self.bot.loop
            )

    @commands.command()
    async def queue(self, ctx):
        q = self.queues.get(ctx.guild.id, [])
        q_list = ""
        if not q:
            await ctx.send("Queue is empty")
        else:
            for song in q:
                q_list += song['title'] + "\n"
            await ctx.send(f"{q_list}\n")
           
    @commands.command()
    async def skip(self, ctx):
        vc = ctx.guild.voice_client
        vc.stop()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        vc = ctx.voice_client
        if(vc.is_playing()):
            await ctx.voice_client.pause()
            await ctx.send("Audio Paused. Type -resume to continue listening")
        if(not vc.is_playing()):
            await ctx.send("No Audio to pause. did you mean resume?")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()

async def setup(bot):
    await bot.add_cog(Music(bot))
    print("setup worked")