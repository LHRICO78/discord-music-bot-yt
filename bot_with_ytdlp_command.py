# Ajoutez cette commande à votre bot.py pour vérifier la version de yt-dlp depuis Discord

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

