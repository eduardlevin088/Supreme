# Aiogram Telegram Bot

A Telegram bot built with aiogram 3.x framework.

## Prerequisites

- Python 3.9 or higher
- A Telegram Bot Token (get it from [@BotFather](https://t.me/BotFather))

## Setup

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd Supreme
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your bot token:
     ```
     BOT_TOKEN=your_bot_token_here
     ADMIN_IDS=123456789,987654321
     ```

## Running the Bot

```bash
python bot.py
```

## Project Structure

```
Supreme/
├── bot.py              # Main bot file with handlers
├── config.py           # Configuration and environment variables
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Features

- Basic command handlers (/start, /help, /about)
- Echo handler for text messages
- Environment variable configuration
- Logging setup
- Admin IDs configuration

## Customization

You can extend the bot by:
- Adding new handlers in `bot.py`
- Creating separate handler files in a `handlers/` directory
- Adding middleware for authentication, logging, etc.
- Implementing database integration
- Adding inline keyboards and callbacks

## License

MIT

