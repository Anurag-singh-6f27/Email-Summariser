# 📧 Personal AI Email Summarizer

```{=html}
<p align="center">
```
An AI-powered email automation platform that monitors multiple inboxes,
summarizes emails using modern LLMs, stores processing history, and
delivers concise notifications directly to Telegram.
```{=html}
</p>
```
```{=html}
<p align="center">
```
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Admin-green?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram)
![Railway](https://img.shields.io/badge/Deploy-Railway-purple?style=for-the-badge&logo=railway)

```{=html}
</p>
```

------------------------------------------------------------------------

# 📚 Table of Contents

-   Features
-   Key Highlights
-   Architecture
-   Application Preview
-   Tech Stack
-   Project Structure
-   Installation
-   Configuration
-   Running
-   Admin Dashboard
-   Deployment
-   Testing
-   Future Improvements
-   License
-   Author

------------------------------------------------------------------------

# ✨ Features

## 📥 Email Processing

-   Multiple IMAP email accounts
-   HTML & Plain Text parsing
-   MIME decoding
-   UTF-8 support
-   Multipart email support
-   Duplicate detection
-   Automatic scheduled polling

## 🤖 AI Summarization

Supports:

-   Google Gemini
-   Groq
-   NVIDIA NIM

Includes:

-   Automatic provider selection
-   Retry mechanism
-   Configurable prompts
-   Configurable summary length

## 📨 Telegram Integration

-   Beautiful formatted summaries
-   Markdown support
-   Retry mechanism
-   Delivery confirmation
-   Error handling

## 📊 Admin Dashboard

-   Dashboard
-   Statistics
-   Email History
-   Scheduler
-   AI Providers
-   Configuration
-   Logs Viewer

## 🔐 Authentication

-   Session-based authentication
-   Protected routes
-   Secure admin login

## ⚙️ Scheduler

-   APScheduler
-   Hourly automation
-   Manual execution
-   Startup execution
-   Configurable schedule

## 💾 Database

SQLite database storing:

-   Processed emails
-   Message IDs
-   Processing timestamps
-   Duplicate protection

------------------------------------------------------------------------

# 🚀 Key Highlights

-   Multi-account email processing
-   AI-powered summarization
-   FastAPI Admin Dashboard
-   Railway deployment
-   Telegram notifications
-   Production-ready architecture
-   Modular codebase
-   Environment-based configuration

------------------------------------------------------------------------

# 🏗 Architecture

``` text
IMAP Accounts
      │
      ▼
 Email Reader
      │
      ▼
 Email Parser
      │
      ▼
AI Provider
(Gemini / Groq / NVIDIA)
      │
      ▼
Telegram Notification
      │
      ▼
SQLite Database
      │
      ▼
Admin Dashboard
```

------------------------------------------------------------------------

# 📸 Application Preview

> Add screenshots to `assets/screenshots/`

-   🔐 Login (`login.png`)
-   📊 Dashboard (`dashboard.png`)
-   📈 Statistics (`statistics.png`)
-   📧 Email History (`email-history.png`)
-   ⏰ Scheduler (`scheduler.png`)
-   🤖 AI Providers (`providers.png`)
-   ⚙️ Configuration (`configuration.png`)
-   📝 Logs (`logs.png`)
-   📨 Telegram Notification (`telegram-summary.png`)

------------------------------------------------------------------------

# 🛠 Tech Stack

  Category     Technology
  ------------ ----------------------
  Language     Python 3.13
  Backend      FastAPI
  Templates    Jinja2
  Scheduler    APScheduler
  Database     SQLite
  AI           Gemini, Groq, NVIDIA
  Email        IMAP
  Messaging    Telegram Bot API
  Logging      Loguru
  Deployment   Railway

------------------------------------------------------------------------

# 📂 Project Structure

``` text
Email-Summariser/
├── admin/
├── ai/
├── database/
├── mail/
├── telegram/
├── utils/
├── testing/
├── logs/
├── data/
├── config.py
├── scheduler.py
├── pipeline.py
├── main.py
├── requirements.txt
├── README.md
└── .env.example
```

------------------------------------------------------------------------

# 🚀 Installation

``` bash
git clone https://github.com/Anurag-singh-6f27/Email-Summariser.git
cd Email-Summariser
python -m venv .venv
```

### Windows

``` powershell
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

``` bash
source .venv/bin/activate
```

Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# ⚙️ Configuration

Copy:

``` text
.env.example
```

to

``` text
.env
```

Configure:

-   Email Accounts
-   AI Provider Keys
-   Telegram Credentials
-   Admin Credentials
-   Scheduler Settings

------------------------------------------------------------------------

# ▶ Running

``` bash
python main.py
```

The application automatically:

-   Reads emails
-   Generates summaries
-   Sends Telegram notifications
-   Stores processing history
-   Starts the scheduler
-   Launches the Admin Dashboard

------------------------------------------------------------------------

# 🌐 Admin Dashboard

Default:

    http://127.0.0.1:8000/login

Features:

-   Dashboard
-   Statistics
-   Email History
-   Scheduler
-   AI Providers
-   Configuration
-   Logs

------------------------------------------------------------------------

# 🚄 Deployment

Successfully deployed on Railway.

Supports:

-   Automatic GitHub Deployments
-   HTTPS
-   Environment Variables
-   Session Authentication

------------------------------------------------------------------------

# 🧪 Testing

Run all tests:

``` bash
pytest
```

Tests cover:

-   Email Parsing
-   Database
-   AI Providers
-   Telegram Service
-   Scheduler
-   Configuration

------------------------------------------------------------------------

# 📌 Future Improvements

-   Docker support
-   PostgreSQL
-   Attachment summarization
-   OCR support
-   Live dashboard updates
-   Analytics charts
-   Multi-user support
-   AI provider benchmarking

------------------------------------------------------------------------

# 📜 License

This project is intended for educational, portfolio, and personal
automation purposes.

------------------------------------------------------------------------

# 👨‍💻 Author

**Anurag Singh**

GitHub: https://github.com/Anurag-singh-6f27

LinkedIn: https://www.linkedin.com/in/anurag-singh-53bb3935b/
