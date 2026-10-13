# -*- coding: utf-8 -*-
"""مدیریت فایل دانش (knowledge.json) — نسخه عمومی."""
import json
import os


class KnowledgeBase:
    def __init__(self, path: str):
        self.path = path
        self.business = {}
        self.faqs = []
        self.reload()

    def reload(self) -> None:
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)
        self.business = data.get("business", {})
        self.faqs = data.get("faqs", [])

    def get(self, faq_id: str):
        for e in self.faqs:
            if e.get("id") == faq_id:
                return e
        return None
