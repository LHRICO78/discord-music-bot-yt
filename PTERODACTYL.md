# 🦖 Installation sur Pterodactyl Panel

Ce guide vous explique comment installer et configurer le bot Discord Music sur un panel Pterodactyl.

## 📋 Prérequis

- Accès à un panel Pterodactyl (admin ou utilisateur)
- Un token de bot Discord
- Le fichier egg: `egg-discord-music-bot.json`

---

## 🎯 Installation pour les administrateurs

### Étape 1: Importer l'egg

1. Connectez-vous à votre **Panel Admin Pterodactyl**
2. Allez dans **Nests** (Nids)
3. Sélectionnez ou créez un nest (par exemple "Discord Bots")
4. Cliquez sur **Import Egg** (Importer un Egg)
5. Uploadez le fichier `egg-discord-music-bot.json`
6. Cliquez sur **Import**

### Étape 2: Configurer l'egg (optionnel)

Après l'import, vous pouvez modifier:
- Le nom de l'egg
- La description
- L'image Docker (par défaut: `ghcr.io/parkervcp/yolks:python_3.11`)
- Les variables d'environnement

### Étape 3: Créer un serveur

1. Allez dans **Servers** (Serveurs)
2. Cliquez sur **Create New** (Créer nouveau)
3. Remplissez les informations:
   - **Name**: Discord Music Bot
   - **Owner**: Sélectionnez l'utilisateur
   - **Nest**: Sélectionnez le nest où vous avez importé l'egg
   - **Egg**: Discord Music Bot
   - **Docker Image**: `ghcr.io/parkervcp/yolks:python_3.11`

4. **Allocation**:
   - Assignez une IP et un port (pas utilisé par le bot, mais requis par Pterodactyl)

5. **Resource Limits** (recommandé):
   - **Memory**: 512 MB minimum (1024 MB recommandé)
   - **Disk**: 1024 MB minimum (2048 MB recommandé)
   - **CPU**: 100% minimum

6. Cliquez sur **Create Server**

---

## 👤 Installation pour les utilisateurs

### Étape 1: Accéder à votre serveur

1. Connectez-vous au **Panel Pterodactyl**
2. Sélectionnez votre serveur Discord Music Bot

### Étape 2: Configuration initiale

1. Allez dans l'onglet **Startup**
2. Configurez les variables:

#### **Variables obligatoires:**

**Discord Bot Token**
- Votre token Discord
- Obtenez-le sur https://discord.com/developers/applications
- Exemple: `VOTRE_TOKEN_DISCORD_ICI`

#### **Variables optionnelles:**

**Git Repository Address**
- Adresse du dépôt GitHub (sans `https://`)
- Par défaut: `github.com/LHRICO78/discord-music-bot-yt.git`
- Modifiez si vous utilisez votre propre fork

**Auto Update**
- `1` = Mise à jour automatique depuis GitHub au démarrage
- `0` = Pas de mise à jour automatique
- Par défaut: `1` (recommandé)

**User Upload**
- `false` = Cloner depuis GitHub (recommandé)
- `true` = Utiliser les fichiers uploadés manuellement
- Par défaut: `false`

**Git Username** et **Git Access Token**
- Nécessaires uniquement pour les dépôts privés
- Laissez vide pour les dépôts publics

### Étape 3: Installation

1. Allez dans l'onglet **Console**
2. Cliquez sur **Install** ou **Reinstall** si déjà installé
3. Attendez la fin de l'installation (vous verrez "Installation complete!")

### Étape 4: Démarrer le bot

1. Cliquez sur **Start** (Démarrer)
2. Attendez que le bot se connecte
3. Vous devriez voir dans la console:
   ```
   🔍 Vérification des mises à jour de yt-dlp...
   ✅ yt-dlp est déjà à jour
   
   🚀 Démarrage du bot...
   
   VotreBot#1234 est connecté et prêt!
   Bot ID: 123456789012345678
   ```

---

## 🎮 Utilisation

Une fois le bot démarré, il est prêt à être utilisé sur Discord!

### Commandes disponibles

- `!join` - Rejoindre le salon vocal
- `!play <url ou recherche>` - Jouer une musique
- `!pause` - Mettre en pause
- `!resume` - Reprendre
- `!skip` - Passer à la suivante
- `!stop` - Arrêter et vider la file
- `!queue` - Voir la file d'attente
- `!volume <0-100>` - Changer le volume
- `!autoplay` - Activer/désactiver AutoPlay
- `!nowplaying` ou `!np` - Afficher la musique en cours
- `!ytdlp` - Voir la version de yt-dlp
- `!leave` - Quitter le salon vocal

---

## 🔧 Gestion du serveur

### Démarrer le bot
Cliquez sur **Start** dans la console

### Arrêter le bot
Cliquez sur **Stop** dans la console

### Redémarrer le bot
Cliquez sur **Restart** dans la console

### Voir les logs
Les logs s'affichent en temps réel dans la **Console**

### Mettre à jour le bot

**Si Auto Update = 1:**
- Redémarrez simplement le bot
- Il se mettra à jour automatiquement depuis GitHub

**Si Auto Update = 0:**
1. Allez dans **Files** (Fichiers)
2. Supprimez tous les fichiers
3. Allez dans **Settings** (Paramètres)
4. Cliquez sur **Reinstall Server**

---

## 📁 Gestion des fichiers

### Accéder aux fichiers

1. Allez dans l'onglet **Files**
2. Vous verrez tous les fichiers du bot:
   - `bot.py` - Code principal du bot
   - `requirements.txt` - Dépendances Python
   - `README.md` - Documentation
   - Etc.

### Modifier bot.py

1. Cliquez sur `bot.py`
2. Modifiez le code
3. Cliquez sur **Save Content**
4. Redémarrez le bot

### Uploader des fichiers personnalisés

1. Définissez `User Upload = true` dans Startup
2. Allez dans **Files**
3. Uploadez vos fichiers
4. Redémarrez le bot

---

## ⚙️ Configuration avancée

### Changer l'image Docker

**Images disponibles:**
- `ghcr.io/parkervcp/yolks:python_3.11` (recommandé)
- `ghcr.io/parkervcp/yolks:python_3.10`
- `ghcr.io/parkervcp/yolks:python_3.9`

**Pour changer:**
1. Arrêtez le serveur
2. Allez dans **Startup**
3. Changez **Docker Image**
4. Redémarrez le serveur

### Augmenter les ressources

Si le bot manque de mémoire ou de CPU:

1. Contactez votre administrateur Pterodactyl
2. Demandez une augmentation de:
   - **Memory**: 1024 MB ou plus
   - **CPU**: 150% ou plus
   - **Disk**: 2048 MB ou plus

### Utiliser un fork personnel

1. Forkez le dépôt GitHub
2. Dans **Startup**, changez **Git Repository Address**:
   - Exemple: `github.com/votre-username/discord-music-bot-yt.git`
3. Réinstallez le serveur

---

## 🐛 Dépannage

### Le bot ne démarre pas

**Vérifier le token Discord:**
1. Allez dans **Startup**
2. Vérifiez que **Discord Bot Token** est correct
3. Régénérez un nouveau token si nécessaire sur https://discord.com/developers/applications

**Vérifier les logs:**
1. Allez dans **Console**
2. Lisez les messages d'erreur
3. Erreurs courantes:
   - `DISCORD_BOT_TOKEN n'est pas définie` → Token manquant
   - `Improper token` → Token invalide
   - `Module not found` → Problème d'installation

**Réinstaller:**
1. Allez dans **Settings**
2. Cliquez sur **Reinstall Server**
3. Attendez la fin de l'installation
4. Redémarrez

### Le bot crash immédiatement

**Vérifier la mémoire:**
- Le bot nécessite au moins 512 MB de RAM
- Contactez l'admin pour augmenter la limite

**Vérifier FFmpeg:**
- FFmpeg est installé automatiquement au premier démarrage
- Si ça échoue, réinstallez le serveur

### Le bot ne joue pas de musique

**Vérifier FFmpeg:**
1. Allez dans **Console**
2. Tapez: `ffmpeg -version`
3. Si "command not found", réinstallez le serveur

**Vérifier yt-dlp:**
1. Utilisez la commande `!ytdlp` sur Discord
2. Vérifiez que yt-dlp est à jour
3. Redémarrez le bot pour forcer la mise à jour

**Vérifier les permissions Discord:**
- Le bot doit avoir les permissions:
  - Connect (Se connecter)
  - Speak (Parler)
  - Use Voice Activity (Utiliser la détection de voix)

### Erreur "Unable to extract video data"

**Solution:**
1. Redémarrez le bot (met à jour yt-dlp automatiquement)
2. Si le problème persiste, attendez quelques heures (YouTube peut bloquer temporairement)

### Le serveur ne démarre pas après l'installation

**Vérifier les variables:**
1. Allez dans **Startup**
2. Vérifiez que **Discord Bot Token** est rempli
3. Vérifiez que **Git Repository Address** est correct

**Vérifier les logs d'installation:**
1. Allez dans **Console**
2. Scrollez vers le haut pour voir les logs d'installation
3. Cherchez les erreurs

---

## 📊 Ressources recommandées

### Configuration minimale
- **Memory**: 512 MB
- **Disk**: 1024 MB
- **CPU**: 100%

### Configuration recommandée
- **Memory**: 1024 MB
- **Disk**: 2048 MB
- **CPU**: 150%

### Configuration optimale (serveurs actifs)
- **Memory**: 2048 MB
- **Disk**: 4096 MB
- **CPU**: 200%

---

## 🔒 Sécurité

### Protéger votre token Discord

⚠️ **IMPORTANT**: Ne partagez jamais votre token Discord!

**Si votre token est compromis:**
1. Allez sur https://discord.com/developers/applications
2. Sélectionnez votre application
3. Allez dans **Bot**
4. Cliquez sur **Reset Token**
5. Copiez le nouveau token
6. Mettez-le à jour dans **Startup** sur Pterodactyl
7. Redémarrez le bot

### Permissions du bot Discord

Configurez les permissions minimales nécessaires:
- Read Messages/View Channels
- Send Messages
- Embed Links
- Attach Files
- Connect
- Speak
- Use Voice Activity

---

## 🔄 Mises à jour

### Mise à jour automatique (Auto Update = 1)

Le bot se met à jour automatiquement depuis GitHub à chaque redémarrage:
1. Redémarrez simplement le bot
2. Il téléchargera les dernières modifications
3. Il mettra à jour yt-dlp

### Mise à jour manuelle

1. Allez dans **Files**
2. Supprimez tous les fichiers
3. Allez dans **Settings**
4. Cliquez sur **Reinstall Server**

---

## 📞 Support

### Problèmes avec le bot

Ouvrez une issue sur GitHub:
https://github.com/LHRICO78/discord-music-bot-yt/issues

### Problèmes avec Pterodactyl

Contactez votre administrateur Pterodactyl ou consultez:
https://pterodactyl.io/community/about.html

---

## 📝 Notes importantes

- Le bot nécessite une connexion internet stable
- FFmpeg est installé automatiquement au premier démarrage
- yt-dlp est mis à jour automatiquement à chaque démarrage
- Les fichiers téléchargés (musiques) sont automatiquement supprimés après lecture
- Le bot utilise le streaming pour minimiser l'utilisation du disque

---

## 🎯 Avantages de Pterodactyl

✅ **Interface web intuitive** - Gérez le bot depuis votre navigateur
✅ **Console en temps réel** - Voir les logs instantanément
✅ **Gestion des fichiers** - Éditez le code directement
✅ **Mises à jour faciles** - Un clic pour mettre à jour
✅ **Isolation** - Chaque bot dans son propre conteneur
✅ **Ressources limitées** - Évite la surcharge du serveur
✅ **Multi-utilisateurs** - Plusieurs personnes peuvent gérer le bot

---

**Votre bot Discord Music est maintenant prêt sur Pterodactyl ! 🎉**

Pour toute question, consultez la documentation complète sur GitHub.

