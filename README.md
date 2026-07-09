# 📧 Personal AI Email Summarizer

A production-ready Python application that automatically reads emails from multiple inboxes, summarizes them using AI (Google Gemini or Grok), and sends concise summaries to Telegram.

---

## Features

- 📥 Read emails from multiple IMAP accounts
- 🤖 AI-powered email summarization
- 📨 Telegram notifications
- ⏰ Automatic hourly execution
- 📝 Structured logging
- ⚙️ Environment-based configuration
- 💾 SQLite database for tracking processed emails
- 🏗️ Modular and production-ready architecture

---

## Tech Stack

- Python 3.12+
- IMAP
- Google Gemini API
- Grok API (optional)
- Telegram Bot API
- SQLite
- APScheduler
- Loguru

---

## Project Structure

```text
Email-Summariser/
│
├── ai/
│   ├── gemini.py
│   ├── grok.py
│   └── prompts.py
│
├── email/
│   ├── reader.py
│   └── parser.py
│
├── telegram/
│   ├── bot.py
│   └── formatter.py
│
├── database/
│   └── db.py
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
├── data/
│   └── emails.db
│
├── logs/
│
├── tests/
│
├── config.py
├── scheduler.py
├── main.py
├── requirements.txt
├── README.md
├── .env
└── .env.example
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd Email-Summariser
```

Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate the environment

### PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Copy

```text
.env.example
```

to

```text
.env
```

Fill in all required credentials.

Example

```env
EMAIL_1=your_email@gmail.com
EMAIL_1_PASSWORD=your_app_password
EMAIL_1_IMAP_SERVER=imap.gmail.com
EMAIL_1_IMAP_PORT=993

GEMINI_API_KEY=YOUR_API_KEY

TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
```

---

## Running the Application

```bash
python main.py
```

Expected output

```text
Loading configuration...
Environment variables loaded.
Logger initialized.
Application started successfully.
```

---

## Development Principles

- Production-ready code
- Type hints everywhere
- PEP 8 compliant
- Modular architecture
- Environment-based configuration
- Comprehensive logging
- Loose coupling
- Single Responsibility Principle (SRP)


## License

This project is intended for personal learning and automation purposes.