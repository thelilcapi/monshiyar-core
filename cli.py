#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""پنل ساده ترمینال منشیار — نسخه عمومی.

اجرا:
    python3 cli.py
"""
from core.config import load_config
from core.knowledge import KnowledgeBase
from core.matcher import Matcher
from core.sanitizer import sanitize

HELP = """Commands:
  help            show this help
  test <question> simulate the bot's answer (no Telegram needed)
  list            list all knowledge-base records
  exit            exit
"""


def main() -> None:
    cfg = load_config()
    kb = KnowledgeBase(cfg["knowledge"]["path"])
    matcher = Matcher(kb, cfg["matching"])
    rules, fallback = cfg["rules"], cfg["matching"]["fallback_answer"]

    print("MonshiYar — community edition")
    print("Type 'help' for commands.\n")

    while True:
        try:
            raw = input("monshiyar> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if not raw:
            continue
        parts = raw.split(None, 1)
        cmd, arg = parts[0].lower(), (parts[1] if len(parts) > 1 else "")

        if cmd in ("exit", "quit", "q"):
            print("Bye!")
            break
        elif cmd in ("help", "h"):
            print(HELP)
        elif cmd == "test":
            if not arg:
                print('Example: test "what colors do the shirts come in?"')
                continue
            entry, score = matcher.best_match(arg)
            if entry:
                print("match: %s (%.2f)" % (entry["id"], score))
                print(sanitize(entry["answer"], rules))
            else:
                print("match: fallback")
                print(sanitize(fallback, rules))
        elif cmd in ("list", "ls"):
            for e in kb.faqs:
                print("- %s : %s" % (e.get("id"), e.get("question")))
        else:
            print("Unknown command — type 'help'")


if __name__ == "__main__":
    main()
