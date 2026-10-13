<div align="center">

*🇮🇷 [نسخه فارسی](README.md)*

# MonshiYar

### The smart Telegram auto-responder for businesses — replace the secretary, not the salary!

*Just fill the knowledge file with your business info; the bot answers your customers by itself.*

![version](https://img.shields.io/badge/version-1.0%20community-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![python](https://img.shields.io/badge/python-3.10%2B-yellow)

[Quickstart](#-quickstart-5-minutes) •
[Features](#-features) •
[Commercial edition](#-full-commercial-edition)

</div>

---

## What does it do?

Imagine you run a clothing store or an immigration consultancy, and customers
keep asking the same questions on Telegram: "How much?", "What colors do you
have?", "Where are you located?" **MonshiYar** answers them automatically, in a
consistent tone — even when the question is phrased differently.

## ✨ Features

- 🧠 **Smart question matching** — keyword + fuzzy search combo; understands typos and different phrasings
- 📝 **Consistent, professional tone** — every answer follows your writing rules: no punctuation marks, no English terms, no numbering, single-line, no emojis (each toggleable)
- 📂 **Simple knowledge file** — just fill one `knowledge.json` with your business Q&A; no complex database needed
- 🖥️ **Terminal panel** — test answers and manage records from the command line
- 🚀 **5-minute setup** — only Python required
- 🆓 **Free & open source** — MIT licensed

## 🚀 Quickstart (5 minutes)

**1. Create a bot and get a token**

Message `@BotFather` on Telegram, send `/newbot`, and copy the token.

**2. Install**

```bash
git clone https://github.com/thelilcapi/monshiyar-core.git
cd monshiyar-core
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put your token inside `.env`:

```
BOT_TOKEN=your_bot_token_here
```

**3. Fill the knowledge file**

Fill `knowledge.json` with your business info:

```json
{
  "id": "shirt-colors",
  "question": "What colors do the shirts come in?",
  "keywords": ["shirt", "color", "colors"],
  "answer": "Our men's shirts come in red blue navy white and black"
}
```

**4. Run**

```bash
bash run.sh
```

Done! Message your bot on Telegram and try it out. 🎉

## 🖥️ Terminal panel

```bash
python3 cli.py
```

| Command | What it does |
|---|---|
| `test <question>` | Simulate the bot's answer without Telegram |
| `list` | List all knowledge-base records |
| `help` | Help |

## ⚙️ Project structure

```
monshiyar-core/
├── bot.py              Telegram bot entry point
├── cli.py              Simple terminal panel
├── core/
│   ├── config.py       Settings loader
│   ├── knowledge.py    Knowledge-file manager
│   ├── matcher.py      Smart matching (keywords + fuzzy)
│   └── sanitizer.py    Answer writing-rules engine
├── knowledge.json      Knowledge file (sample: clothing store)
├── config.yaml         Settings
└── requirements.txt
```

## 🆚 Community vs Commercial

| Feature | Community (here) | Commercial |
|---|---|---|
| Smart answering from knowledge file | ✅ | ✅ |
| Consistent writing rules | ✅ | ✅ |
| Terminal panel | basic | ✅ advanced (EN/Finglish, setup wizard) |
| In-Telegram admin panel (`/admin`) | ❌ | ✅ full, button-based |
| AI (OpenRouter / custom model) | ❌ | ✅ with daily quota |
| SQL database connection | ❌ | ✅ MySQL / PostgreSQL / SQLite |
| Conversation logs & stats | ❌ | ✅ |
| License | MIT (free) | commercial |

---

<div align="center">

## 💎 Full commercial edition

### Get the full commercial edition (complete Telegram admin panel, database management, and OpenRouter/Custom AI support) here:

# 👉 [t.me/thelilawmir](https://t.me/thelilawmir) 👈

*Installation and setup support is included with the commercial edition.*

</div>

---

## 📄 License

Released under the [MIT](LICENSE) license — use, modify and share freely.
