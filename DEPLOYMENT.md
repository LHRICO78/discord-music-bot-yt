# 🚀 Guide de déploiement - Bot Discord Musique

Ce guide vous explique comment exécuter le bot en arrière-plan et le démarrer automatiquement au démarrage du système.

## 📋 Table des matières

1. [Méthode 1: Systemd (Linux - Recommandé)](#méthode-1-systemd-linux---recommandé)
2. [Méthode 2: Docker (Multi-plateforme)](#méthode-2-docker-multi-plateforme)
3. [Méthode 3: Screen/Tmux (Linux/macOS)](#méthode-3-screentmux-linuxmacos)
4. [Méthode 4: PM2 (Node.js - Multi-plateforme)](#méthode-4-pm2-nodejs---multi-plateforme)
5. [Méthode 5: Tâche planifiée Windows](#méthode-5-tâche-planifiée-windows)
6. [Méthode 6: Nohup (Linux/macOS - Simple)](#méthode-6-nohup-linuxmacos---simple)

---

## Méthode 1: Systemd (Linux - Recommandé)

**Avantages:** Démarrage automatique, redémarrage automatique en cas de crash, gestion native par le système.

### Étape 1: Préparer le fichier de service

Éditez le fichier `discord-bot.service` et modifiez les valeurs suivantes:

```bash
nano discord-bot.service
```

Remplacez:
- `votre_utilisateur` par votre nom d'utilisateur Linux (ex: `ubuntu`, `pi`)
- `/chemin/vers/discord-music-bot` par le chemin complet vers le dossier du bot
- `votre_token_ici` par votre token Discord

**Exemple:**
```ini
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-music-bot
Environment="DISCORD_BOT_TOKEN=VOTRE_TOKEN_DISCORD_ICI"
ExecStart=/usr/bin/python3 /home/ubuntu/discord-music-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Étape 2: Installer le service

```bash
# Copier le fichier de service dans le répertoire systemd
sudo cp discord-bot.service /etc/systemd/system/

# Recharger systemd pour prendre en compte le nouveau service
sudo systemctl daemon-reload

# Activer le service au démarrage
sudo systemctl enable discord-bot.service

# Démarrer le service
sudo systemctl start discord-bot.service
```

### Étape 3: Vérifier le statut

```bash
# Vérifier que le bot fonctionne
sudo systemctl status discord-bot.service

# Voir les logs en temps réel
sudo journalctl -u discord-bot.service -f
```

### Commandes utiles

```bash
# Arrêter le bot
sudo systemctl stop discord-bot.service

# Redémarrer le bot
sudo systemctl restart discord-bot.service

# Désactiver le démarrage automatique
sudo systemctl disable discord-bot.service

# Voir les logs
sudo journalctl -u discord-bot.service -n 50
```

---

## Méthode 2: Docker (Multi-plateforme)

**Avantages:** Isolation complète, portable, facile à déployer.

### Prérequis

Installez Docker et Docker Compose:

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose-plugin
```

**Windows/macOS:** Téléchargez [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Étape 1: Créer le fichier .env

```bash
cp .env.example .env
nano .env
```

Ajoutez votre token Discord:
```
DISCORD_BOT_TOKEN=votre_token_ici
```

### Étape 2: Construire et démarrer le conteneur

```bash
# Construire l'image
docker compose build

# Démarrer le bot en arrière-plan
docker compose up -d

# Voir les logs
docker compose logs -f
```

### Commandes utiles

```bash
# Arrêter le bot
docker compose down

# Redémarrer le bot
docker compose restart

# Voir le statut
docker compose ps

# Voir les logs
docker compose logs -f discord-bot
```

### Démarrage automatique

Le bot redémarrera automatiquement grâce à `restart: unless-stopped` dans le fichier `docker-compose.yml`.

---

## Méthode 3: Screen/Tmux (Linux/macOS)

**Avantages:** Simple, léger, pas besoin de droits root.

### Avec Screen

```bash
# Installer screen
sudo apt-get install screen  # Ubuntu/Debian
# ou
brew install screen  # macOS

# Rendre le script exécutable
chmod +x start_bot.sh

# Éditer le script pour ajouter votre token
nano start_bot.sh

# Démarrer le bot dans une session screen
screen -dmS discord-bot ./start_bot.sh

# Voir la session
screen -r discord-bot

# Détacher la session: Ctrl+A puis D
```

### Avec Tmux

```bash
# Installer tmux
sudo apt-get install tmux  # Ubuntu/Debian
# ou
brew install tmux  # macOS

# Démarrer le bot dans une session tmux
tmux new-session -d -s discord-bot './start_bot.sh'

# Voir la session
tmux attach -t discord-bot

# Détacher la session: Ctrl+B puis D
```

### Démarrage automatique avec crontab

```bash
# Éditer le crontab
crontab -e

# Ajouter cette ligne pour démarrer au boot
@reboot screen -dmS discord-bot /chemin/vers/discord-music-bot/start_bot.sh
# ou avec tmux
@reboot tmux new-session -d -s discord-bot '/chemin/vers/discord-music-bot/start_bot.sh'
```

---

## Méthode 4: PM2 (Node.js - Multi-plateforme)

**Avantages:** Gestion avancée des processus, monitoring, logs, redémarrage automatique.

### Étape 1: Installer PM2

```bash
# Installer Node.js si nécessaire
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Installer PM2 globalement
sudo npm install -g pm2
```

### Étape 2: Créer un fichier de configuration PM2

Créez `ecosystem.config.js`:

```javascript
module.exports = {
  apps: [{
    name: 'discord-music-bot',
    script: 'bot.py',
    interpreter: 'python3',
    env: {
      DISCORD_BOT_TOKEN: 'votre_token_ici'
    },
    autorestart: true,
    watch: false,
    max_memory_restart: '500M'
  }]
};
```

### Étape 3: Démarrer le bot

```bash
# Démarrer le bot
pm2 start ecosystem.config.js

# Sauvegarder la configuration
pm2 save

# Configurer le démarrage automatique
pm2 startup
# Suivez les instructions affichées
```

### Commandes utiles

```bash
# Voir le statut
pm2 status

# Voir les logs
pm2 logs discord-music-bot

# Redémarrer
pm2 restart discord-music-bot

# Arrêter
pm2 stop discord-music-bot

# Supprimer
pm2 delete discord-music-bot

# Monitoring
pm2 monit
```

---

## Méthode 5: Tâche planifiée Windows

**Avantages:** Solution native Windows, démarrage automatique.

### Étape 1: Préparer le script

Éditez `start_bot.bat` et ajoutez votre token:

```batch
@echo off
set DISCORD_BOT_TOKEN=votre_token_ici
python bot.py
```

### Étape 2: Créer une tâche planifiée

1. Ouvrez le **Planificateur de tâches** (Task Scheduler)
2. Cliquez sur **Créer une tâche...**
3. **Général:**
   - Nom: `Discord Music Bot`
   - Cochez "Exécuter même si l'utilisateur n'est pas connecté"
   - Cochez "Exécuter avec les autorisations maximales"
4. **Déclencheurs:**
   - Nouveau → Au démarrage
5. **Actions:**
   - Nouveau → Démarrer un programme
   - Programme: `C:\chemin\vers\discord-music-bot\start_bot.bat`
   - Commencer dans: `C:\chemin\vers\discord-music-bot`
6. **Conditions:**
   - Décochez "Démarrer uniquement si l'ordinateur est relié au secteur"
7. **Paramètres:**
   - Cochez "Autoriser l'exécution de la tâche à la demande"
   - Cochez "Si la tâche échoue, recommencer toutes les 1 minute"

### Étape 3: Exécuter en arrière-plan

Pour exécuter sans fenêtre visible, créez `start_bot_hidden.vbs`:

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c start_bot.bat", 0, False
Set WshShell = Nothing
```

Utilisez ce fichier `.vbs` dans la tâche planifiée au lieu du `.bat`.

---

## Méthode 6: Nohup (Linux/macOS - Simple)

**Avantages:** Très simple, pas d'installation requise.

### Démarrer le bot

```bash
# Rendre le script exécutable
chmod +x start_bot.sh

# Éditer le script pour ajouter votre token
nano start_bot.sh

# Démarrer avec nohup
nohup ./start_bot.sh > bot.log 2>&1 &

# Voir le PID
echo $!

# Voir les logs
tail -f bot.log
```

### Arrêter le bot

```bash
# Trouver le PID
ps aux | grep bot.py

# Tuer le processus
kill <PID>
```

### Démarrage automatique avec crontab

```bash
crontab -e

# Ajouter cette ligne
@reboot cd /chemin/vers/discord-music-bot && nohup ./start_bot.sh > bot.log 2>&1 &
```

---

## 🔒 Sécurité du token

**⚠️ IMPORTANT:** Ne commitez jamais votre token Discord sur GitHub!

### Utiliser un fichier .env

Installez `python-dotenv`:

```bash
pip install python-dotenv
```

Modifiez `bot.py` pour charger le token depuis `.env`:

```python
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
```

Créez un fichier `.env`:

```
DISCORD_BOT_TOKEN=votre_token_ici
```

Le fichier `.env` est déjà dans `.gitignore`, donc il ne sera pas uploadé sur GitHub.

---

## 🐛 Dépannage

### Le bot ne démarre pas

1. Vérifiez que FFmpeg est installé: `ffmpeg -version`
2. Vérifiez que les dépendances sont installées: `pip install -r requirements.txt`
3. Vérifiez que le token est correct
4. Vérifiez les logs pour voir les erreurs

### Le bot s'arrête après quelques minutes

1. Vérifiez les logs pour voir les erreurs
2. Assurez-vous que la méthode de démarrage automatique est configurée (systemd, PM2, etc.)
3. Vérifiez que votre serveur/ordinateur a assez de RAM

### Le bot ne se reconnecte pas après un crash

Utilisez une méthode avec redémarrage automatique:
- Systemd avec `Restart=always`
- Docker avec `restart: unless-stopped`
- PM2 avec `autorestart: true`

---

## 📊 Comparaison des méthodes

| Méthode | Difficulté | Démarrage auto | Redémarrage auto | Multi-plateforme |
|---------|------------|----------------|------------------|------------------|
| Systemd | Moyenne | ✅ | ✅ | ❌ (Linux uniquement) |
| Docker | Moyenne | ✅ | ✅ | ✅ |
| Screen/Tmux | Facile | ⚠️ (avec cron) | ❌ | ⚠️ (Linux/macOS) |
| PM2 | Moyenne | ✅ | ✅ | ✅ |
| Tâche Windows | Moyenne | ✅ | ⚠️ (configurable) | ❌ (Windows uniquement) |
| Nohup | Facile | ⚠️ (avec cron) | ❌ | ⚠️ (Linux/macOS) |

### Recommandations

- **Linux (serveur):** Systemd ou Docker
- **Windows:** Tâche planifiée ou Docker
- **macOS:** PM2 ou Docker
- **Développement/Test:** Screen/Tmux ou Nohup
- **Production:** Docker ou Systemd

---

## 🎯 Hébergement cloud

Pour un bot disponible 24/7, vous pouvez utiliser:

- **VPS (Virtual Private Server):**
  - DigitalOcean (à partir de 5$/mois)
  - Linode (à partir de 5$/mois)
  - Vultr (à partir de 3.50$/mois)
  - OVH (à partir de 3.50€/mois)

- **Gratuit (limité):**
  - Oracle Cloud (Always Free tier)
  - Google Cloud Platform (300$ de crédits)
  - AWS Free Tier (12 mois gratuits)

- **Spécialisé Discord:**
  - Railway.app
  - Render.com
  - Heroku (payant maintenant)

---

## 📞 Support

Si vous rencontrez des problèmes, ouvrez une issue sur GitHub avec:
- Votre système d'exploitation
- La méthode de déploiement utilisée
- Les logs d'erreur
- Les étapes que vous avez suivies

