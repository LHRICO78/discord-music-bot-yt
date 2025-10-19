import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import os
import subprocess
import sys
from datetime import timedelta

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
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration', 0)
        self.thumbnail = data.get('thumbnail')
        self.webpage_url = data.get('webpage_url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class MusicPlayer:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.queue = []
        self.current = None
        self.current_message = None
        self.requester = None
        self.likes = set()
        self.start_time = None
        
    def add_to_queue(self, player, requester):
        self.queue.append({'player': player, 'requester': requester})
    
    def clear_queue(self):
        self.queue.clear()
        
    def get_next(self):
        if len(self.queue) > 0:
            item = self.queue.pop(0)
            self.current = item['player']
            self.requester = item['requester']
            self.likes.clear()
            return item
        return None


# Dictionnaire pour stocker les lecteurs de musique par serveur
music_players = {}


def get_music_player(guild_id):
    if guild_id not in music_players:
        music_players[guild_id] = MusicPlayer(guild_id)
    return music_players[guild_id]


def format_duration(seconds):
    """Formate la durée en format MM:SS"""
    if seconds == 0:
        return "00:00"
    return str(timedelta(seconds=int(seconds)))[2:7] if seconds < 3600 else str(timedelta(seconds=int(seconds)))


class MusicControlView(discord.ui.View):
    def __init__(self, ctx, player_manager):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.player_manager = player_manager
        
    @discord.ui.button(label='Pause', style=discord.ButtonStyle.blurple, emoji='⏸️')
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.voice_client and self.ctx.voice_client.is_playing():
            self.ctx.voice_client.pause()
            await interaction.response.send_message("⏸️ Musique mise en pause", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Aucune musique n'est en cours de lecture", ephemeral=True)
    
    @discord.ui.button(label='Resume', style=discord.ButtonStyle.green, emoji='▶️')
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.voice_client and self.ctx.voice_client.is_paused():
            self.ctx.voice_client.resume()
            await interaction.response.send_message("▶️ Musique reprise", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Aucune musique n'est en pause", ephemeral=True)
    
    @discord.ui.button(label='Skip', style=discord.ButtonStyle.gray, emoji='⏭️')
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.voice_client and self.ctx.voice_client.is_playing():
            self.ctx.voice_client.stop()
            await interaction.response.send_message("⏭️ Musique passée", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Aucune musique n'est en cours", ephemeral=True)
    
    @discord.ui.button(label='Stop', style=discord.ButtonStyle.gray, emoji='⏹️')
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player_manager.clear_queue()
        if self.ctx.voice_client:
            self.ctx.voice_client.stop()
            await interaction.response.send_message("⏹️ Musique arrêtée et file d'attente vidée", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Le bot n'est pas dans un salon vocal", ephemeral=True)
    
    @discord.ui.button(label='Like', style=discord.ButtonStyle.gray, emoji='❤️')
    async def like_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        if user_id in self.player_manager.likes:
            self.player_manager.likes.remove(user_id)
            message = "💔 Like retiré"
        else:
            self.player_manager.likes.add(user_id)
            message = "❤️ Musique likée!"
        
        # Mettre à jour l'embed avec le nouveau nombre de likes
        if self.player_manager.current and self.ctx.voice_client:
            embed = await create_now_playing_embed(self.ctx, self.player_manager.current, self.player_manager.requester, self.player_manager)
            await interaction.response.edit_message(embed=embed, view=self)
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)


async def create_now_playing_embed(ctx, player, requester, player_manager):
    """Crée un embed enrichi pour la musique en cours"""
    embed = discord.Embed(
        title="🎵 Lecture en cours",
        color=discord.Color.blue()
    )
    
    # Titre de la musique avec durée
    duration_str = format_duration(player.duration)
    embed.add_field(
        name=f"{player.title}",
        value=f"⏱️ **Durée:** {duration_str}",
        inline=False
    )
    
    # Informations sur le demandeur
    embed.add_field(
        name="Requested by",
        value=f"{requester.mention} ({requester.display_name})",
        inline=True
    )
    
    # Salon vocal connecté
    if ctx.voice_client and ctx.voice_client.channel:
        embed.add_field(
            name="Connected in",
            value=f"🔊 {ctx.voice_client.channel.name}",
            inline=True
        )
    
    # Nombre de likes
    likes_count = len(player_manager.likes)
    embed.add_field(
        name="Likes",
        value=f"❤️ {likes_count}",
        inline=True
    )
    
    # Miniature si disponible
    if player.thumbnail:
        embed.set_thumbnail(url=player.thumbnail)
    
    # Lien vers la vidéo
    if player.webpage_url:
        embed.add_field(
            name="Lien",
            value=f"[Écouter sur YouTube]({player.webpage_url})",
            inline=False
        )
    
    embed.set_footer(text="Utilisez les boutons ci-dessous pour contrôler la lecture")
    
    return embed


def update_ytdlp():
    """Vérifie et met à jour yt-dlp au démarrage"""
    print("🔍 Vérification des mises à jour de yt-dlp...")
    try:
        # Essayer de mettre à jour yt-dlp
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if "Successfully installed" in result.stdout:
            print("✅ yt-dlp a été mis à jour avec succès!")
        elif "Requirement already satisfied" in result.stdout or "already up-to-date" in result.stdout:
            print("✅ yt-dlp est déjà à jour")
        else:
            print("ℹ️ yt-dlp vérifié")
            
    except subprocess.TimeoutExpired:
        print("⚠️ La mise à jour de yt-dlp a pris trop de temps, passage en mode normal")
    except Exception as e:
        print(f"⚠️ Erreur lors de la mise à jour de yt-dlp: {e}")
        print("Le bot continuera avec la version actuelle")


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
    
    player_manager = get_music_player(ctx.guild.id)
    
    async with ctx.typing():
        try:
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            player_manager.add_to_queue(player, ctx.author)
            
            if not ctx.voice_client.is_playing():
                await play_next(ctx)
            else:
                await ctx.send(f"🎵 **{player.title}** ajouté à la file d'attente!")
        except Exception as e:
            await ctx.send(f"❌ Erreur lors du chargement de la musique: {str(e)}")


async def play_next(ctx):
    player_manager = get_music_player(ctx.guild.id)
    item = player_manager.get_next()
    
    if item:
        player = item['player']
        requester = item['requester']
        
        def after_playing(error):
            if error:
                print(f'Erreur de lecture: {error}')
            
            coro = play_next(ctx)
            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
            try:
                fut.result()
            except Exception as e:
                print(f'Erreur dans after_playing: {e}')
        
        ctx.voice_client.play(player, after=after_playing)
        player_manager.start_time = asyncio.get_event_loop().time()
        
        # Créer l'embed et les boutons
        embed = await create_now_playing_embed(ctx, player, requester, player_manager)
        view = MusicControlView(ctx, player_manager)
        
        # Supprimer l'ancien message s'il existe
        if player_manager.current_message:
            try:
                await player_manager.current_message.delete()
            except:
                pass
        
        # Envoyer le nouveau message
        player_manager.current_message = await ctx.send(embed=embed, view=view)


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
    player_manager = get_music_player(ctx.guild.id)
    player_manager.clear_queue()
    
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹️ Musique arrêtée et file d'attente vidée")
    else:
        await ctx.send("❌ Le bot n'est pas dans un salon vocal")


@bot.command(name='leave', help='Fait quitter le bot du salon vocal')
async def leave(ctx):
    if ctx.voice_client:
        player_manager = get_music_player(ctx.guild.id)
        player_manager.clear_queue()
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Déconnecté du salon vocal")
    else:
        await ctx.send("❌ Le bot n'est pas dans un salon vocal")


@bot.command(name='queue', help='Affiche la file d\'attente')
async def show_queue(ctx):
    player_manager = get_music_player(ctx.guild.id)
    
    if len(player_manager.queue) == 0:
        await ctx.send("📭 La file d'attente est vide")
    else:
        embed = discord.Embed(
            title="📋 File d'attente",
            color=discord.Color.blue()
        )
        
        for i, item in enumerate(player_manager.queue[:10], 1):
            player = item['player']
            requester = item['requester']
            duration = format_duration(player.duration)
            embed.add_field(
                name=f"{i}. {player.title}",
                value=f"⏱️ {duration} | Demandé par {requester.mention}",
                inline=False
            )
        
        if len(player_manager.queue) > 10:
            embed.set_footer(text=f"... et {len(player_manager.queue) - 10} autres musiques")
        
        await ctx.send(embed=embed)


@bot.command(name='volume', help='Change le volume (0-100)')
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("❌ Le bot n'est pas connecté à un salon vocal")

    if 0 <= volume <= 100:
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"🔊 Volume réglé à {volume}%")
    else:
        await ctx.send("❌ Le volume doit être entre 0 et 100")


@bot.command(name='nowplaying', aliases=['np'], help='Affiche la musique en cours')
async def now_playing(ctx):
    player_manager = get_music_player(ctx.guild.id)
    
    if player_manager.current and ctx.voice_client and ctx.voice_client.is_playing():
        embed = await create_now_playing_embed(ctx, player_manager.current, player_manager.requester, player_manager)
        view = MusicControlView(ctx, player_manager)
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("❌ Aucune musique n'est en cours de lecture")


# Récupération du token depuis les variables d'environnement
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN is None:
    print("❌ ERREUR: La variable d'environnement DISCORD_BOT_TOKEN n'est pas définie!")
    print("Veuillez définir votre token Discord avec: export DISCORD_BOT_TOKEN='votre_token_ici'")
else:
    # Vérifier et mettre à jour yt-dlp avant de démarrer le bot
    update_ytdlp()
    print("\n🚀 Démarrage du bot...\n")
    bot.run(TOKEN)




@bot.command(name='ytdlp', help='Affiche la version de yt-dlp')
async def ytdlp_version(ctx):
    """Affiche la version actuelle de yt-dlp"""
    try:
        import yt_dlp
        version = yt_dlp.version.__version__
        
        embed = discord.Embed(
            title="📦 yt-dlp Information",
            color=discord.Color.blue()
        )
        embed.add_field(name="Version", value=f"`{version}`", inline=False)
        embed.add_field(
            name="Mise à jour",
            value="yt-dlp est automatiquement mis à jour à chaque redémarrage du bot",
            inline=False
        )
        embed.set_footer(text="Pour forcer une mise à jour, redémarrez le bot")
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erreur lors de la récupération de la version: {str(e)}")

