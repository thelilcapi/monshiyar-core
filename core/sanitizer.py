# -*- coding: utf-8 -*-
"""موتور قوانین نگارشی پاسخ‌ها.

قوانین پیش‌فرض (قابل تنظیم در config.yaml):
- بدون علائم نگارشی
- بدون واژه‌های انگلیسی (حروف لاتین)
- بدون شماره‌گذاری خاص
- تک‌خط (بدون رفتن به خط بعد)
- بدون ایموجی
"""
import re

_AR_DIACRITICS = re.compile(r"[\u064B-\u0652\u0670]")
_PERSIAN_MAP = str.maketrans({"ي": "ی", "ك": "ک", "ۀ": "ه"})

_EMOJI = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # شکلک‌ها
    "\U0001F300-\U0001F5FF"  # نمادها
    "\U0001F680-\U0001F6FF"  # حمل‌ونقل و نقشه
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "\u2B00-\u2BFF"
    "\uFE0F"  # انتخاب‌گر نمایشی
    "]+",
    flags=re.UNICODE,
)

_LATIN_WORD = re.compile(r"[A-Za-z]+")

# علائم نگارشی فارسی و انگلیسی (نیم‌فاصله و ارقام فارسی دست نمی‌خورند)
_PUNCT = ".,!?;:،؛؟«»‹›„“”‘’'\"()[]{}<>…—–‐-/*\\|@#$%^&*~`+=_"
_PUNCT_RE = re.compile("[" + re.escape(_PUNCT) + "]")

# شماره‌گذاری ابتدای خط: «1. » «۲) » «- » «• »
_LINE_NUM = re.compile(r"(?m)^\s*[0-9۰-۹]+[\.\)\:\-–—]\s*")
_BULLET = re.compile(r"(?m)^\s*[•▪◦‣\-\*]+\s+")
# شماره‌گذاری داخل متن: «۱. قرمز ۲. آبی»
_INLINE_NUM = re.compile(r"(?<![0-9۰-۹])[0-9۰-۹]+[\.\)\:]")


def normalize_persian(text: str) -> str:
    """یکدست‌سازی حروف فارسی (ي/ك عربی، کشیده، اعراب)."""
    t = (text or "").translate(_PERSIAN_MAP)
    t = t.replace("ـ", "")
    t = _AR_DIACRITICS.sub("", t)
    return t


def normalize_for_match(text: str) -> str:
    """نرمال‌سازی متن برای تطبیق با فایل دانش."""
    t = normalize_persian(text).lower()
    t = _PUNCT_RE.sub(" ", t)
    t = _EMOJI.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def sanitize(text: str, rules: dict) -> str:
    """اعمال قوانین نگارشی روی پاسخ نهایی."""
    t = normalize_persian(text or "")

    if rules.get("no_emoji", True):
        t = _EMOJI.sub("", t)

    if rules.get("no_numbering", True):
        t = _LINE_NUM.sub("", t)
        t = _BULLET.sub("", t)
        t = _INLINE_NUM.sub(" ", t)

    if rules.get("no_punctuation", True):
        t = _PUNCT_RE.sub("", t)

    if rules.get("no_english_terms", True):
        t = _LATIN_WORD.sub("", t)

    if rules.get("single_line", True):
        t = t.replace("\r", " ").replace("\n", " ")
        t = re.sub(r"\s+", " ", t)
    else:
        t = re.sub(r"[ \t]+", " ", t)

    return t.strip()
