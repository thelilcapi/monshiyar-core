#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""منشیار | MonshiYar — نسخه عمومی (Open Core).

ربات تلگرام پاسخ‌گوی هوشمند بر اساس فایل دانش + جست‌وجوی فازی.
نسخه کامل تجاری (پنل ادمین تلگرام، هوش مصنوعی، اتصال SQL و ...) جدا عرضه می‌شود.

اجرا:
    bash run.sh
"""
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from core.config import load_config
from core.knowledge import KnowledgeBase
from core.matcher import Matcher
from core.sanitizer import sanitize

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO
)
log = logging.getLogger("monshiyar")

WELCOME = "سلام به منشیار خوش آمدید هر سوالی درباره محصولات و خدمات ما دارید همینجا بنویسید"


class MonshiYar:
    def __init__(self):
        self.cfg = load_config()
        self.kb = KnowledgeBase(self.cfg["knowledge"]["path"])
        self.matcher = Matcher(self.kb, self.cfg["matching"])
        self.rules = self.cfg["rules"]
        self.fallback = self.cfg["matching"]["fallback_answer"]

    def answer_for(self, text: str):
        entry, score = self.matcher.best_match(text)
        if entry:
            return sanitize(entry["answer"], self.rules), entry["id"], score
        return sanitize(self.fallback, self.rules), "fallback", score

    async def cmd_start(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(sanitize(WELCOME, self.rules))

    async def on_message(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        msg = update.message
        if not msg or not msg.text:
            return
        text = msg.text.strip()
        if not text or text.startswith("/"):
            return

        answer, match_id, score = self.answer_for(text)
        await msg.reply_text(answer)
        log.info("match=%s score=%.2f", match_id, score)

    def run(self):
        token = self.cfg["bot"]["token"]
        if not token:
            raise SystemExit(
                "توکن ربات تنظیم نشده است؛ فایل .env را از روی .env.example بسازید"
            )

        async def _post_init(app):
            me = await app.bot.get_me()
            log.info("ربات آنلاین شد: @%s", me.username)

        app = ApplicationBuilder().token(token).post_init(_post_init).build()
        app.add_handler(CommandHandler("start", self.cmd_start))
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_message)
        )
        log.info("شروع به کار با %d رکورد دانش", len(self.kb.faqs))
        app.run_polling()


if __name__ == "__main__":
    MonshiYar().run()
