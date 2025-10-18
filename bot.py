import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import os

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration de youtube_dl
ytdl_format_options = {
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
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # Prend la première entrée si c'est une playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# File d'attente pour chaque serveur
queues = {}


def get_queue(guild_id):
    if guild_id not in queues:
        queues[guild_id] = []
    return queues[guild_id]


@bot.event
async def on_ready():
    print(f'{bot.user} est connecté et prêt!')
    print(f'Bot ID: {bot.user.id}')


@bot.command(name='join', help='Fait rejoindre le bot dans votre salon vocal')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("❌ Vous devez être dans un salon vocal pour utiliser cette commande!")
        return

    channel = ctx.message.author.voice.channel
    
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    
    await ctx.send(f"✅ Connecté à **{channel.name}**")


@bot.command(name='play', help='Joue une musique depuis YouTube (URL ou recherche)')
async def play(ctx, *, url):
    if not ctx.message.author.voice:
        await ctx.send("❌ Vous devez être dans un salon vocal pour utiliser cette commande!")
        return

    channel = ctx.message.author.voice.channel
    
    if ctx.voice_client is None:
        await channel.connect()
    
    async with ctx.typing():
        try:
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            queue = get_queue(ctx.guild.id)
            queue.append(player)
            
            if not ctx.voice_client.is_playing():
                await play_next(ctx)
            else:
                await ctx.send(f"🎵 **{player.title}** ajouté à la file d'attente!")
        except Exception as e:
            await ctx.send(f"❌ Erreur lors du chargement de la musique: {str(e)}")


async def play_next(ctx):
    queue = get_queue(ctx.guild.id)
    
    if len(queue) > 0:
        player = queue.pop(0)
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        await ctx.send(f"🎶 Lecture en cours: **{player.title}**")


@bot.command(name='pause', help='Met en pause la musique')
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Musique mise en pause")
    else:
        await ctx.send("❌ Aucune musique n'est en cours de lecture")


@bot.command(name='resume', help='Reprend la musique')
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Musique reprise")
    else:
        await ctx.send("❌ Aucune musique n'est en pause")


@bot.command(name='skip', help='Passe à la musique suivante')
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Musique passée")
    else:
        await ctx.send("❌ Aucune musique n'est en cours de lecture")


@bot.command(name='stop', help='Arrête la musique et vide la file d\'attente')
async def stop(ctx):
    queue = get_queue(ctx.guild.id)
    queue.clear()
    
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹️ Musique arrêtée et file d'attente vidée")
    else:
        await ctx.send("❌ Le bot n'est pas dans un salon vocal")


@bot.command(name='leave', help='Fait quitter le bot du salon vocal')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Déconnecté du salon vocal")
    else:
        await ctx.send("❌ Le bot n'est pas dans un salon vocal")


@bot.command(name='queue', help='Affiche la file d\'attente')
async def show_queue(ctx):
    queue = get_queue(ctx.guild.id)
    
    if len(queue) == 0:
        await ctx.send("📭 La file d'attente est vide")
    else:
        message = "📋 **File d'attente:**\n"
        for i, player in enumerate(queue, 1):
            message += f"{i}. {player.title}\n"
        await ctx.send(message)


@bot.command(name='volume', help='Change le volume (0-100)')
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("❌ Le bot n'est pas connecté à un salon vocal")

    if 0 <= volume <= 100:
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"🔊 Volume réglé à {volume}%")
    else:
        await ctx.send("❌ Le volume doit être entre 0 et 100")


# Récupération du token depuis les variables d'environnement
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN is None:
    print("❌ ERREUR: La variable d'environnement DISCORD_BOT_TOKEN n'est pas définie!")
    print("Veuillez définir votre token Discord avec: export DISCORD_BOT_TOKEN='votre_token_ici'")
else:
    bot.run(TOKEN)

