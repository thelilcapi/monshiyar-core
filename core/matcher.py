# -*- coding: utf-8 -*-
"""تطبیق هوشمند سوال کاربر با فایل دانش (کلیدواژه + شباهت فازی)."""
from .sanitizer import normalize_for_match

try:
    from rapidfuzz import fuzz

    def _ratio(a: str, b: str) -> float:
        return fuzz.ratio(a, b) / 100.0

    _ENGINE = "rapidfuzz"
except ImportError:  # جایگزین سبک بدون نیاز به نصب
    import difflib

    def _ratio(a: str, b: str) -> float:
        return difflib.SequenceMatcher(None, a, b).ratio()

    _ENGINE = "difflib"


class Matcher:
    def __init__(self, kb, cfg: dict):
        self.kb = kb
        self.threshold = float(cfg.get("threshold", 0.4))
        self.kw_weight = float(cfg.get("keyword_weight", 0.6))
        self.fz_weight = float(cfg.get("fuzzy_weight", 0.4))

    def score(self, query: str, entry: dict) -> float:
        q = normalize_for_match(query)
        if not q:
            return 0.0
        kws = [normalize_for_match(k) for k in entry.get("keywords", [])]
        hits = sum(1 for k in kws if k and k in q)
        kw_score = min(1.0, hits / 2.0)
        fz_score = _ratio(q, normalize_for_match(entry.get("question", "")))
        return self.kw_weight * kw_score + self.fz_weight * fz_score

    def best_match(self, query: str):
        """برمی‌گرداند: (بهترین رکورد یا None، امتیاز)"""
        best, best_score = None, 0.0
        for entry in self.kb.faqs:
            s = self.score(query, entry)
            if s > best_score:
                best, best_score = entry, s
        if best is not None and best_score >= self.threshold:
            return best, best_score
        return None, best_score
