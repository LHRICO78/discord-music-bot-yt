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
    max_memory_restart: '500M',
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};

