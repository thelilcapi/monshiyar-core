# -*- coding: utf-8 -*-
"""بارگذاری تنظیمات (config.yaml + .env) — نسخه عمومی."""
import os

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path: str = None) -> None:
    path = path or os.path.join(BASE_DIR, ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def load_config(path: str = None) -> dict:
    load_env()
    path = path or os.path.join(BASE_DIR, "config.yaml")
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    token_env = cfg.get("bot", {}).get("token_env", "BOT_TOKEN")
    cfg["bot"]["token"] = os.environ.get(token_env, "").strip()

    kn = cfg.get("knowledge", {})
    if kn.get("path") and not os.path.isabs(kn["path"]):
        kn["path"] = os.path.join(BASE_DIR, kn["path"])

    return cfg
