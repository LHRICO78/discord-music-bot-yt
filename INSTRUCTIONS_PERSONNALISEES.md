# 🚀 Instructions personnalisées pour votre serveur DiscordBot

## 📍 Votre configuration détectée

- **Utilisateur:** root
- **Serveur:** DiscordBot
- **Chemin du bot:** `/root/discord-music-bot-yt/discord-music-bot-yt/`
- **Environnement virtuel:** ENV (activé)

---

## ✅ ÉTAPE 1: Créer le fichier de service

Vous avez déjà ouvert l'éditeur avec:
```bash
sudo nano /etc/systemd/system/discord-bot.service
```

### Copiez EXACTEMENT ce contenu:

```ini
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/discord-music-bot-yt/discord-music-bot-yt
Environment="DISCORD_BOT_TOKEN=VOTRE_TOKEN_DISCORD_ICI"
ExecStart=/usr/bin/python3 /root/discord-music-bot-yt/discord-music-bot-yt/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### ⚠️ IMPORTANT: Remplacez uniquement cette ligne:

```ini
Environment="DISCORD_BOT_TOKEN=VOTRE_TOKEN_DISCORD_ICI"
```

Par votre vrai token Discord, par exemple:
```ini
Environment="DISCORD_BOT_TOKEN=VOTRE_VRAI_TOKEN_DISCORD_ICI"
```

### Sauvegarder le fichier:
1. Appuyez sur `Ctrl + O` (sauvegarder)
2. Appuyez sur `Entrée` (confirmer)
3. Appuyez sur `Ctrl + X` (quitter)

---

## ✅ ÉTAPE 2: Vérifier que Python3 est bien installé

```bash
which python3
```

**Résultat attendu:** `/usr/bin/python3`

Si le chemin est différent (par exemple `/usr/local/bin/python3`), modifiez la ligne `ExecStart=` dans le fichier de service.

---

## ✅ ÉTAPE 3: Vérifier que les dépendances sont installées

```bash
cd /root/discord-music-bot-yt/discord-music-bot-yt
pip3 install -r requirements.txt
```

---

## ✅ ÉTAPE 4: Vérifier que FFmpeg est installé

```bash
ffmpeg -version
```

Si FFmpeg n'est pas installé:
```bash
apt update
apt install ffmpeg -y
```

---

## ✅ ÉTAPE 5: Activer et démarrer le service

### 5.1 Recharger systemd
```bash
systemctl daemon-reload
```

### 5.2 Activer le démarrage automatique
```bash
systemctl enable discord-bot.service
```

**Résultat attendu:**
```
Created symlink /etc/systemd/system/multi-user.target.wants/discord-bot.service → /etc/systemd/system/discord-bot.service.
```

### 5.3 Démarrer le bot maintenant
```bash
systemctl start discord-bot.service
```

### 5.4 Vérifier que tout fonctionne
```bash
systemctl status discord-bot.service
```

**Si tout va bien, vous devriez voir:**
```
● discord-bot.service - Discord Music Bot
     Loaded: loaded (/etc/systemd/system/discord-bot.service; enabled)
     Active: active (running) since ...
```

Avec `Active: active (running)` en **VERT**

---

## 🎉 C'est terminé !

Votre bot est maintenant:
- ✅ En cours d'exécution en arrière-plan
- ✅ Démarrera automatiquement à chaque redémarrage du serveur
- ✅ Redémarrera automatiquement s'il crash (toutes les 10 secondes)

---

## 📊 Commandes utiles pour gérer votre bot

### Voir le statut du bot
```bash
systemctl status discord-bot.service
```

### Voir les logs en temps réel
```bash
journalctl -u discord-bot.service -f
```
*Appuyez sur `Ctrl + C` pour arrêter*

### Voir les 100 dernières lignes de logs
```bash
journalctl -u discord-bot.service -n 100
```

### Redémarrer le bot
```bash
systemctl restart discord-bot.service
```

### Arrêter le bot
```bash
systemctl stop discord-bot.service
```

### Démarrer le bot
```bash
systemctl start discord-bot.service
```

### Désactiver le démarrage automatique
```bash
systemctl disable discord-bot.service
```

### Réactiver le démarrage automatique
```bash
systemctl enable discord-bot.service
```

---

## 🔄 Si vous devez changer le token Discord

### 1. Éditer le fichier de service
```bash
nano /etc/systemd/system/discord-bot.service
```

### 2. Modifier la ligne Environment avec le nouveau token

### 3. Sauvegarder (Ctrl + O, Entrée, Ctrl + X)

### 4. Recharger et redémarrer
```bash
systemctl daemon-reload
systemctl restart discord-bot.service
```

### 5. Vérifier
```bash
systemctl status discord-bot.service
```

---

## 🐛 Dépannage

### Le bot ne démarre pas

**Voir les erreurs:**
```bash
journalctl -u discord-bot.service -n 50
```

**Tester manuellement:**
```bash
cd /root/discord-music-bot-yt/discord-music-bot-yt
export DISCORD_BOT_TOKEN='votre_token'
python3 bot.py
```

### Erreurs courantes

**1. Module discord non trouvé**
```bash
cd /root/discord-music-bot-yt/discord-music-bot-yt
pip3 install -r requirements.txt
```

**2. FFmpeg non trouvé**
```bash
apt install ffmpeg -y
```

**3. Token invalide**
- Vérifiez que votre token Discord est correct
- Allez sur https://discord.com/developers/applications
- Régénérez un nouveau token si nécessaire

**4. Permission denied**
- Comme vous êtes root, ce problème ne devrait pas arriver
- Vérifiez quand même: `ls -la /root/discord-music-bot-yt/discord-music-bot-yt/bot.py`

---

## 🔒 Note sur la sécurité

⚠️ Vous utilisez l'utilisateur **root** pour exécuter le bot. C'est fonctionnel mais pas idéal pour la sécurité.

**Recommandation (optionnel):**
Créez un utilisateur dédié pour le bot:

```bash
# Créer un utilisateur discord-bot
useradd -r -s /bin/bash -d /home/discord-bot discord-bot

# Déplacer le bot
mv /root/discord-music-bot-yt /home/discord-bot/
chown -R discord-bot:discord-bot /home/discord-bot/discord-music-bot-yt

# Modifier le fichier de service
nano /etc/systemd/system/discord-bot.service
# Changez User=root par User=discord-bot
# Changez les chemins /root/ par /home/discord-bot/

# Recharger et redémarrer
systemctl daemon-reload
systemctl restart discord-bot.service
```

Mais ce n'est pas obligatoire, le bot fonctionnera très bien avec root.

---

## 📝 Résumé des commandes à exécuter

```bash
# 1. Le fichier de service est déjà ouvert, collez la configuration et sauvegardez

# 2. Recharger systemd
systemctl daemon-reload

# 3. Activer le démarrage automatique
systemctl enable discord-bot.service

# 4. Démarrer le bot
systemctl start discord-bot.service

# 5. Vérifier le statut
systemctl status discord-bot.service

# 6. Voir les logs si besoin
journalctl -u discord-bot.service -f
```

---

**Votre bot devrait maintenant tourner 24/7 ! 🎉**

Si vous avez des questions ou des erreurs, regardez les logs avec:
```bash
journalctl -u discord-bot.service -n 100
```

