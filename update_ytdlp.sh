#!/bin/bash

# Script de mise à jour manuelle de yt-dlp
# Utilisez ce script si vous voulez mettre à jour yt-dlp sans redémarrer le bot

echo "🔍 Vérification de la version actuelle de yt-dlp..."
python3 -m pip show yt-dlp | grep Version

echo ""
echo "🔄 Mise à jour de yt-dlp..."
python3 -m pip install --upgrade yt-dlp

echo ""
echo "✅ Nouvelle version de yt-dlp:"
python3 -m pip show yt-dlp | grep Version

echo ""
echo "ℹ️  Pour que les changements prennent effet, redémarrez le bot:"
echo "   sudo systemctl restart discord-bot.service"

