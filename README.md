# 🎵 Bot Discord Musique

Un bot Discord simple et efficace pour lire de la musique YouTube dans les salons vocaux.

## ✨ Fonctionnalités

- 🎶 Lecture de musiques depuis YouTube (URL ou recherche)
- 📋 File d'attente pour gérer plusieurs musiques
- ⏸️ Contrôles de lecture (pause, reprise, skip, stop)
- 🔊 Contrôle du volume
- 🎯 Commandes simples et intuitives

## 📋 Prérequis

- Python 3.8 ou supérieur
- FFmpeg installé sur votre système
- Un token de bot Discord

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/discord-music-bot.git
cd discord-music-bot
```

### 2. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 3. Installer FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
- Téléchargez FFmpeg depuis [ffmpeg.org](https://ffmpeg.org/download.html)
- Ajoutez FFmpeg au PATH de votre système

**macOS:**
```bash
brew install ffmpeg
```

### 4. Créer un bot Discord

1. Allez sur le [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez sur "New Application" et donnez-lui un nom
3. Allez dans l'onglet "Bot" et cliquez sur "Add Bot"
4. Copiez le token du bot (vous en aurez besoin pour la configuration)
5. Activez les "Privileged Gateway Intents" suivants:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT
6. Allez dans l'onglet "OAuth2" > "URL Generator"
7. Sélectionnez les scopes: `bot`
8. Sélectionnez les permissions suivantes:
   - Read Messages/View Channels
   - Send Messages
   - Connect
   - Speak
9. Copiez l'URL générée et utilisez-la pour inviter le bot sur votre serveur

### 5. Configuration

Définissez votre token Discord en tant que variable d'environnement:

**Linux/macOS:**
```bash
export DISCORD_BOT_TOKEN='votre_token_ici'
```

**Windows (CMD):**
```cmd
set DISCORD_BOT_TOKEN=votre_token_ici
```

**Windows (PowerShell):**
```powershell
$env:DISCORD_BOT_TOKEN='votre_token_ici'
```

Ou créez un fichier `.env` (non recommandé pour la production):
```
DISCORD_BOT_TOKEN=votre_token_ici
```

## 🎮 Utilisation

### Démarrer le bot

```bash
python bot.py
```

### Commandes disponibles

| Commande | Description | Exemple |
|----------|-------------|---------|
| `!join` | Fait rejoindre le bot dans votre salon vocal | `!join` |
| `!play <url ou recherche>` | Joue une musique depuis YouTube | `!play https://youtube.com/watch?v=...` ou `!play despacito` |
| `!pause` | Met en pause la musique | `!pause` |
| `!resume` | Reprend la musique | `!resume` |
| `!skip` | Passe à la musique suivante | `!skip` |
| `!stop` | Arrête la musique et vide la file d'attente | `!stop` |
| `!leave` | Fait quitter le bot du salon vocal | `!leave` |
| `!queue` | Affiche la file d'attente | `!queue` |
| `!volume <0-100>` | Change le volume | `!volume 50` |

## 📝 Exemple d'utilisation

1. Rejoignez un salon vocal sur votre serveur Discord
2. Tapez `!join` pour faire rejoindre le bot
3. Tapez `!play despacito` pour jouer une musique
4. Utilisez `!pause`, `!resume`, `!skip` pour contrôler la lecture
5. Tapez `!leave` pour déconnecter le bot

## 🛠️ Technologies utilisées

- **discord.py** - Bibliothèque Python pour interagir avec l'API Discord
- **yt-dlp** - Outil pour télécharger des vidéos depuis YouTube
- **FFmpeg** - Outil de traitement multimédia pour l'audio
- **PyNaCl** - Bibliothèque pour le support vocal

## ⚠️ Notes importantes

- Le bot nécessite FFmpeg installé sur votre système pour fonctionner
- Assurez-vous d'activer les intents nécessaires dans le Developer Portal
- Ne partagez jamais votre token Discord publiquement
- Le bot utilise le streaming pour éviter de télécharger les fichiers

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🐛 Problèmes connus

- Si le bot ne se connecte pas, vérifiez que votre token est correct
- Si l'audio ne fonctionne pas, assurez-vous que FFmpeg est installé et accessible dans le PATH
- Si vous avez des erreurs avec YouTube, essayez de mettre à jour yt-dlp: `pip install --upgrade yt-dlp`

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

