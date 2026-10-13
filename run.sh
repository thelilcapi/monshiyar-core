#!/usr/bin/env bash
# اجرای ربات منشیار — نسخه عمومی
cd "$(dirname "$0")"
if [ ! -f .env ]; then
  echo "فایل .env پیدا نشد؛ ابتدا از روی .env.example بسازید و توکن را بگذارید"
  exit 1
fi
set -a
. ./.env
set +a
exec python3 bot.py
