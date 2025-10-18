# 🔄 Mise à jour automatique de yt-dlp

## ✨ Fonctionnalité ajoutée

Le bot vérifie et met à jour **automatiquement yt-dlp** à chaque démarrage. Cela garantit que le bot peut toujours télécharger des vidéos YouTube même quand YouTube change son API.

## 🚀 Comment ça fonctionne

### Au démarrage du bot

1. Le bot vérifie la version actuelle de yt-dlp
2. Il tente de la mettre à jour avec `pip install --upgrade yt-dlp`
3. Il affiche le résultat dans les logs:
   - ✅ `yt-dlp a été mis à jour avec succès!` - Une nouvelle version a été installée
   - ✅ `yt-dlp est déjà à jour` - Aucune mise à jour nécessaire
   - ⚠️ `Erreur lors de la mise à jour` - Le bot continuera avec la version actuelle

### Dans les logs systemd

Vous verrez ces messages au démarrage:

```
🔍 Vérification des mises à jour de yt-dlp...
✅ yt-dlp est déjà à jour

🚀 Démarrage du bot...

VotreBot#1234 est connecté et prêt!
```

## 📊 Vérifier la version de yt-dlp

### Depuis Discord

Utilisez la commande:
```
!ytdlp
```

Le bot affichera un embed avec:
- La version actuelle de yt-dlp
- Information sur la mise à jour automatique

### Depuis le serveur

```bash
# Voir la version installée
python3 -m pip show yt-dlp | grep Version

# Ou avec le script fourni
./update_ytdlp.sh
```

## 🔧 Forcer une mise à jour manuelle

### Méthode 1: Redémarrer le bot (recommandé)

```bash
sudo systemctl restart discord-bot.service
```

Le bot vérifiera automatiquement les mises à jour au redémarrage.

### Méthode 2: Utiliser le script de mise à jour

```bash
cd /root/discord-music-bot-yt/discord-music-bot-yt
./update_ytdlp.sh
```

Puis redémarrez le bot:
```bash
sudo systemctl restart discord-bot.service
```

### Méthode 3: Mise à jour manuelle

```bash
python3 -m pip install --upgrade yt-dlp
sudo systemctl restart discord-bot.service
```

## 📋 Voir les logs de mise à jour

### Logs en temps réel

```bash
sudo journalctl -u discord-bot.service -f
```

### Derniers démarrages

```bash
sudo journalctl -u discord-bot.service -n 100 | grep -A 5 "Vérification des mises à jour"
```

## ⚙️ Configuration avancée

### Désactiver la mise à jour automatique

Si vous voulez désactiver la mise à jour automatique (non recommandé):

1. Éditez `bot.py`
2. Commentez la ligne `update_ytdlp()`:

```python
# Vérifier et mettre à jour yt-dlp avant de démarrer le bot
# update_ytdlp()  # ← Commenté
print("\n🚀 Démarrage du bot...\n")
bot.run(TOKEN)
```

3. Redémarrez le bot

### Modifier le timeout de mise à jour

Par défaut, la mise à jour a un timeout de 30 secondes. Pour le modifier:

Dans `bot.py`, ligne `timeout=30`:

```python
result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
    capture_output=True,
    text=True,
    timeout=60  # ← Changez à 60 secondes par exemple
)
```

## 🐛 Dépannage

### La mise à jour échoue

**Vérifier les permissions:**
```bash
# Si vous utilisez un environnement virtuel
source venv/bin/activate
pip install --upgrade yt-dlp
```

**Vérifier la connexion internet:**
```bash
ping -c 3 pypi.org
```

**Installer manuellement:**
```bash
python3 -m pip install --upgrade --force-reinstall yt-dlp
```

### Le bot ne démarre pas après la mise à jour

**Voir les logs d'erreur:**
```bash
sudo journalctl -u discord-bot.service -n 50
```

**Revenir à une version stable:**
```bash
python3 -m pip install yt-dlp==2023.3.4
sudo systemctl restart discord-bot.service
```

### La mise à jour prend trop de temps

Le bot a un timeout de 30 secondes. Si la mise à jour prend plus de temps:
- Le bot affichera un avertissement
- Il continuera avec la version actuelle
- Vous pouvez augmenter le timeout (voir Configuration avancée)

## 📅 Fréquence des mises à jour

Le bot vérifie les mises à jour:
- ✅ À chaque démarrage du bot
- ✅ À chaque redémarrage du serveur
- ✅ Après chaque crash (grâce à `Restart=always` dans systemd)

**Recommandation:** Redémarrez le bot au moins une fois par semaine pour garantir que yt-dlp reste à jour.

## 🔄 Automatiser les redémarrages hebdomadaires

Pour redémarrer automatiquement le bot chaque semaine:

```bash
# Éditer le crontab root
sudo crontab -e

# Ajouter cette ligne pour redémarrer chaque dimanche à 4h du matin
0 4 * * 0 /bin/systemctl restart discord-bot.service
```

## ℹ️ Pourquoi c'est important

YouTube change régulièrement son API pour empêcher les téléchargements. yt-dlp est mis à jour fréquemment pour contourner ces changements.

**Sans mise à jour régulière:**
- ❌ Le bot ne pourra plus lire de musiques YouTube
- ❌ Vous verrez des erreurs "Unable to extract video data"
- ❌ Les commandes `!play` échoueront

**Avec la mise à jour automatique:**
- ✅ Le bot reste toujours fonctionnel
- ✅ Pas besoin d'intervention manuelle
- ✅ Compatibilité garantie avec YouTube

## 📝 Commandes récapitulatives

```bash
# Vérifier la version de yt-dlp
python3 -m pip show yt-dlp | grep Version

# Forcer une mise à jour
python3 -m pip install --upgrade yt-dlp

# Redémarrer le bot (met à jour automatiquement)
sudo systemctl restart discord-bot.service

# Voir les logs de mise à jour
sudo journalctl -u discord-bot.service -n 100 | grep ytdlp

# Utiliser le script de mise à jour
./update_ytdlp.sh
```

---

**La mise à jour automatique est maintenant active ! 🎉**

Votre bot restera toujours compatible avec YouTube sans intervention manuelle.

