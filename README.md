# 🎵 Bot Discord Musique

Un bot Discord avancé pour lire de la musique YouTube dans les salons vocaux avec une interface interactive enrichie.

## ✨ Fonctionnalités

- 🔄 **Mise à jour automatique de yt-dlp** - Vérifie et met à jour yt-dlp à chaque démarrage

- 🎶 **Lecture de musiques depuis YouTube** - Supporte les URLs directes et les recherches par mots-clés
- 📋 **File d'attente intelligente** - Gestion automatique de plusieurs musiques
- 🎨 **Interface enrichie** - Affichage détaillé avec embed Discord et boutons interactifs
- ⏱️ **Timer en temps réel** - Affichage de la durée de chaque musique
- 👤 **Demandeur affiché** - Voir qui a demandé chaque musique
- 🔊 **Salon vocal affiché** - Information sur le salon vocal connecté
- ❤️ **Système de likes** - Les utilisateurs peuvent liker les musiques en cours
- 🔄 **AutoPlay** - Lecture automatique continue (peut être activé/désactivé)
- 🎮 **Contrôles interactifs** - Boutons Discord pour Resume, Skip, Stop, AutoPlay et Like
- 🔊 **Contrôle du volume** - Ajustement de 0 à 100%
- 🎯 **Commandes simples** - Préfixe `!` pour toutes les commandes

## 📋 Prérequis

- Python 3.8 ou supérieur
- FFmpeg installé sur votre système
- Un token de bot Discord

## 🚀 Installation

> **💡 Pour exécuter le bot en arrière-plan et au démarrage automatique, consultez le [Guide de déploiement complet](DEPLOYMENT.md)**

### 1. Cloner le dépôt

```bash
git clone https://github.com/LHRICO78/discord-music-bot-yt.git
cd discord-music-bot-yt
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
   - Embed Links
   - Attach Files
   - Connect
   - Speak
   - Use Voice Activity
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
| `!autoplay` | Active/désactive l'AutoPlay | `!autoplay` |
| `!nowplaying` ou `!np` | Affiche la musique en cours | `!np` |

### Boutons interactifs

Lorsqu'une musique est en cours de lecture, un message enrichi s'affiche avec les boutons suivants:

- **▶️ Resume** - Reprend la lecture si elle est en pause
- **⏭️ Skip** - Passe à la musique suivante
- **⏹️ Stop** - Arrête la lecture et vide la file d'attente
- **🔄 AutoPlay** - Active/désactive la lecture automatique continue
- **❤️ Like** - Like la musique en cours (toggle)

### Affichage enrichi

Chaque musique en cours affiche:
- 🎵 **Titre de la musique** avec durée totale
- 👤 **Demandeur** - L'utilisateur qui a demandé la musique
- 🔊 **Salon vocal** - Le nom du salon vocal connecté
- ❤️ **Nombre de likes** - Combien d'utilisateurs ont liké
- 🔄 **Statut AutoPlay** - Si l'AutoPlay est activé ou non
- 🖼️ **Miniature** - Image de la vidéo YouTube
- 🔗 **Lien YouTube** - Lien direct vers la vidéo

## 📝 Exemple d'utilisation

1. Rejoignez un salon vocal sur votre serveur Discord
2. Tapez `!join` pour faire rejoindre le bot
3. Tapez `!play despacito` pour jouer une musique
4. Un message enrichi s'affiche avec toutes les informations et les boutons de contrôle
5. Cliquez sur **❤️ Like** pour liker la musique
6. Cliquez sur **🔄 AutoPlay** pour activer la lecture continue
7. Utilisez les boutons ou les commandes pour contrôler la lecture
8. Tapez `!queue` pour voir les musiques en attente
9. Tapez `!leave` pour déconnecter le bot

## 🛠️ Technologies utilisées

- **discord.py** - Bibliothèque Python pour interagir avec l'API Discord
- **yt-dlp** - Outil pour télécharger des vidéos depuis YouTube
- **FFmpeg** - Outil de traitement multimédia pour l'audio
- **PyNaCl** - Bibliothèque pour le support vocal
- **Discord UI Components** - Boutons et embeds interactifs

## ⚠️ Notes importantes

- Le bot nécessite FFmpeg installé sur votre système pour fonctionner
- Assurez-vous d'activer les intents nécessaires dans le Developer Portal
- Ne partagez jamais votre token Discord publiquement
- Le bot utilise le streaming pour éviter de télécharger les fichiers
- Les boutons interactifs nécessitent discord.py version 2.0 ou supérieure
- L'AutoPlay est une fonctionnalité de base (peut être améliorée avec une API de recommandations)

## 🎨 Captures d'écran

Le bot affiche un embed Discord enrichi avec:
- Titre et durée de la musique
- Miniature de la vidéo YouTube
- Informations sur le demandeur
- Salon vocal connecté
- Nombre de likes
- Statut AutoPlay
- Boutons interactifs pour contrôler la lecture

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🐛 Problèmes connus

- Si le bot ne se connecte pas, vérifiez que votre token est correct
- Si l'audio ne fonctionne pas, assurez-vous que FFmpeg est installé et accessible dans le PATH
- Si vous avez des erreurs avec YouTube, essayez de mettre à jour yt-dlp: `pip install --upgrade yt-dlp`
- Les boutons peuvent ne pas fonctionner si discord.py n'est pas à jour

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

## 🚀 Améliorations futures possibles

- Intégration d'une API de recommandations pour l'AutoPlay
- Sauvegarde des musiques likées dans une base de données
- Playlists personnalisées par utilisateur
- Égaliseur audio
- Paroles des chansons
- Historique de lecture

