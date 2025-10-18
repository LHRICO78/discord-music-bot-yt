# 🚀 Guide de démarrage automatique sur Debian

Ce guide vous explique comment configurer votre bot Discord pour qu'il démarre automatiquement au démarrage de votre Debian et tourne en permanence en arrière-plan.

## 📋 Prérequis

Avant de commencer, assurez-vous que:
- Le bot fonctionne correctement quand vous le lancez manuellement
- FFmpeg est installé: `sudo apt install ffmpeg`
- Les dépendances Python sont installées: `pip3 install -r requirements.txt`

## 🔧 Étape 1: Préparer votre bot

### 1.1 Notez le chemin complet de votre bot

```bash
cd /chemin/vers/votre/discord-music-bot
pwd
```

**Exemple de résultat:** `/home/votre_utilisateur/discord-music-bot`

### 1.2 Notez votre nom d'utilisateur

```bash
whoami
```

**Exemple de résultat:** `debian` ou `pi` ou votre nom d'utilisateur

### 1.3 Trouvez le chemin de Python3

```bash
which python3
```

**Exemple de résultat:** `/usr/bin/python3`

## 🛠️ Étape 2: Créer le fichier de service systemd

### 2.1 Créer le fichier de service

```bash
sudo nano /etc/systemd/system/discord-bot.service
```

### 2.2 Copier cette configuration

**⚠️ IMPORTANT: Remplacez les valeurs suivantes:**
- `VOTRE_UTILISATEUR` → votre nom d'utilisateur (résultat de `whoami`)
- `/chemin/vers/discord-music-bot` → le chemin complet de votre bot (résultat de `pwd`)
- `VOTRE_TOKEN_DISCORD_ICI` → votre vrai token Discord

```ini
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
User=VOTRE_UTILISATEUR
WorkingDirectory=/chemin/vers/discord-music-bot
Environment="DISCORD_BOT_TOKEN=VOTRE_TOKEN_DISCORD_ICI"
ExecStart=/usr/bin/python3 /chemin/vers/discord-music-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2.3 Exemple concret

Si votre utilisateur est `debian` et votre bot est dans `/home/debian/discord-music-bot`:

```ini
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
User=debian
WorkingDirectory=/home/debian/discord-music-bot
Environment="DISCORD_BOT_TOKEN=MTIzNDU2Nzg5.AbCdEf.GhIjKlMnOpQrStUvWxYz"
ExecStart=/usr/bin/python3 /home/debian/discord-music-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2.4 Sauvegarder le fichier

- Appuyez sur `Ctrl + O` pour sauvegarder
- Appuyez sur `Entrée` pour confirmer
- Appuyez sur `Ctrl + X` pour quitter

## ✅ Étape 3: Activer et démarrer le service

### 3.1 Recharger systemd

```bash
sudo systemctl daemon-reload
```

### 3.2 Activer le démarrage automatique

```bash
sudo systemctl enable discord-bot.service
```

Vous devriez voir: `Created symlink...`

### 3.3 Démarrer le bot maintenant

```bash
sudo systemctl start discord-bot.service
```

### 3.4 Vérifier que tout fonctionne

```bash
sudo systemctl status discord-bot.service
```

**Si tout va bien, vous devriez voir:**
- `Active: active (running)` en **vert**
- Le bot connecté avec son nom

**Exemple de sortie:**
```
● discord-bot.service - Discord Music Bot
     Loaded: loaded (/etc/systemd/system/discord-bot.service; enabled)
     Active: active (running) since Sat 2025-01-18 14:30:00 CET; 5s ago
   Main PID: 12345 (python3)
      Tasks: 2 (limit: 4915)
     Memory: 45.2M
        CPU: 1.234s
     CGroup: /system.slice/discord-bot.service
             └─12345 /usr/bin/python3 /home/debian/discord-music-bot/bot.py

Jan 18 14:30:00 debian systemd[1]: Started Discord Music Bot.
Jan 18 14:30:01 debian python3[12345]: VotreBot#1234 est connecté et prêt!
```

### 3.5 Quitter l'affichage du statut

Appuyez sur `Q` pour quitter

## 🎉 C'est terminé !

Votre bot est maintenant:
- ✅ **En cours d'exécution** en arrière-plan
- ✅ **Démarrera automatiquement** à chaque démarrage de votre Debian
- ✅ **Redémarrera automatiquement** s'il crash

## 📊 Commandes utiles

### Voir le statut du bot

```bash
sudo systemctl status discord-bot.service
```

### Voir les logs en temps réel

```bash
sudo journalctl -u discord-bot.service -f
```

Appuyez sur `Ctrl + C` pour arrêter l'affichage

### Voir les 50 dernières lignes de logs

```bash
sudo journalctl -u discord-bot.service -n 50
```

### Redémarrer le bot

```bash
sudo systemctl restart discord-bot.service
```

### Arrêter le bot

```bash
sudo systemctl stop discord-bot.service
```

### Démarrer le bot

```bash
sudo systemctl start discord-bot.service
```

### Désactiver le démarrage automatique

```bash
sudo systemctl disable discord-bot.service
```

### Réactiver le démarrage automatique

```bash
sudo systemctl enable discord-bot.service
```

## 🔄 Modifier la configuration

Si vous devez changer votre token ou modifier la configuration:

### 1. Éditer le fichier de service

```bash
sudo nano /etc/systemd/system/discord-bot.service
```

### 2. Faire vos modifications

### 3. Sauvegarder (Ctrl + O, Entrée, Ctrl + X)

### 4. Recharger et redémarrer

```bash
sudo systemctl daemon-reload
sudo systemctl restart discord-bot.service
```

### 5. Vérifier

```bash
sudo systemctl status discord-bot.service
```

## 🐛 Dépannage

### Le bot ne démarre pas

**1. Vérifier les logs:**
```bash
sudo journalctl -u discord-bot.service -n 100
```

**2. Vérifier que le chemin est correct:**
```bash
ls -la /chemin/vers/discord-music-bot/bot.py
```

**3. Vérifier que Python3 fonctionne:**
```bash
/usr/bin/python3 --version
```

**4. Tester le bot manuellement:**
```bash
cd /chemin/vers/discord-music-bot
export DISCORD_BOT_TOKEN='votre_token'
python3 bot.py
```

### Le bot s'arrête après quelques secondes

**Vérifier les erreurs dans les logs:**
```bash
sudo journalctl -u discord-bot.service -n 100
```

**Erreurs courantes:**
- **Token invalide:** Vérifiez votre token Discord
- **Module manquant:** Installez les dépendances: `pip3 install -r requirements.txt`
- **FFmpeg manquant:** Installez FFmpeg: `sudo apt install ffmpeg`

### Le bot ne se connecte pas au salon vocal

**1. Vérifier que FFmpeg est installé:**
```bash
ffmpeg -version
```

**2. Installer FFmpeg si nécessaire:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**3. Redémarrer le bot:**
```bash
sudo systemctl restart discord-bot.service
```

### Voir si le bot est vraiment en cours d'exécution

```bash
ps aux | grep bot.py
```

Vous devriez voir une ligne avec `python3 bot.py`

## 🔒 Sécurité du token

**⚠️ ATTENTION:** Votre token Discord est stocké en clair dans le fichier de service.

### Pour plus de sécurité, utilisez un fichier .env:

**1. Créer un fichier .env dans le dossier du bot:**
```bash
cd /chemin/vers/discord-music-bot
nano .env
```

**2. Ajouter votre token:**
```
DISCORD_BOT_TOKEN=votre_token_ici
```

**3. Sauvegarder (Ctrl + O, Entrée, Ctrl + X)**

**4. Modifier bot.py pour utiliser python-dotenv:**

Installez python-dotenv:
```bash
pip3 install python-dotenv
```

Ajoutez au début de bot.py (après les imports):
```python
from dotenv import load_dotenv
load_dotenv()
```

**5. Modifier le fichier de service:**
```bash
sudo nano /etc/systemd/system/discord-bot.service
```

Supprimez la ligne `Environment=...` et gardez seulement:
```ini
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
User=VOTRE_UTILISATEUR
WorkingDirectory=/chemin/vers/discord-music-bot
ExecStart=/usr/bin/python3 /chemin/vers/discord-music-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**6. Recharger et redémarrer:**
```bash
sudo systemctl daemon-reload
sudo systemctl restart discord-bot.service
```

## 📞 Besoin d'aide ?

Si vous rencontrez des problèmes:

1. Vérifiez les logs: `sudo journalctl -u discord-bot.service -n 100`
2. Testez le bot manuellement pour voir l'erreur exacte
3. Vérifiez que tous les prérequis sont installés (Python3, FFmpeg, dépendances)

---

**Votre bot devrait maintenant tourner 24/7 en arrière-plan ! 🎉**

