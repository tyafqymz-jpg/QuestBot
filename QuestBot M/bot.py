import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'default_search': 'ytsearch',
    'noplaylist': True,
    'extractaudio': True,
}

ffmpeg_options = {
    'options': '-vn -b:a 192k'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f'تم تسجيل الدخول بنجاح باسم: {bot.user}')

@bot.command(name='ش')
async def play(ctx, *, query: str):
    if not ctx.author.voice:
        return await ctx.send("يجب أن تكون في روم صوتي أولاً!")

    channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    async with ctx.typing():
        try:
            data = ytdl.extract_info(query, download=False)
            if 'entries' in data:
                data = data['entries'][0]

            audio_url = data['url']
            title = data.get('title', 'مقطع صوتي')
        except Exception as e:
            return await ctx.send(f"حدث خطأ أثناء البحث: {e}")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        # تشغيل الصوت باستخدام تدفق مباشر وثابت
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options))
        ctx.voice_client.play(source)

    await ctx.send(f"🎶 يتم الآن تشغيل: **{title}**")

@bot.command(name='إيقاف')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("تم الخروج من الروم الصوتي.")

bot.run('MTU1NzI2NzA4ODkxMjAyNzY2MA.GPODbS.Mlly7jXyGuBqUc_eCvQizZjqpguLTVYlkqwofM')