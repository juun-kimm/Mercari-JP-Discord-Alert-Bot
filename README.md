# Mercari-JP-Discord-Alert-Bot
A lightweight Playwright-powered Mercari Japan watcher that monitors search results and sends Discord notifications whenever a new listing appears.

## Features

* Monitors Mercari JP search results
* Discord webhook notifications
* Duplicate prevention using local cache
* Configurable search query
* Configurable polling interval
* Supports long-running execution via tmux
* Lightweight and easy to self-host

---

## Example Notification

Each new listing includes:

* Listing title
* Price
* Product image
* Direct Mercari link

---

## Requirements

* Python 3.10+
* Playwright
* Discord webhook

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/mercari-alerts.git
cd Mercari-JP-Discord-Alert-Bot
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright Chromium:

```bash
playwright install chromium
```

---

## Configuration

Create a `.env` file by running:

```bash
echo "DISCORD_WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_URL

SEARCH_QUERY=koji kuga

SEARCH_SIZE=42
SEARCH_REGION=US
SEARCH_SORT=recent
SEARCH_FILTER=all
SEARCH_PRICE_MIN=0
SEARCH_PRICE_MAX=10000

POLL_SECONDS=10" > .env
```

Replace `YOUR_DISCORD_WEBHOOK_URL` with your Discord webhook URL.

### Getting a Discord Webhook URL

1. Open Discord.
2. Create a server (or use an existing one).
3. Create a text channel (e.g. `#mercari-alerts`).
4. Click the ⚙️ next to the channel.
5. Go to **Integrations** → **Webhooks**.
6. Click **Create Webhook**.
7. Click **Copy Webhook URL**.
8. Replace `YOUR_DISCORD_WEBHOOK_URL` in the command above with the copied URL.

### Verify Your Configuration

Run:

```bash
cat .env
```

You should see something similar to:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxxxx/xxxxxxxx

SEARCH_QUERY=koji kuga

SEARCH_SIZE=42
SEARCH_REGION=US
SEARCH_SORT=recent
SEARCH_FILTER=all
SEARCH_PRICE_MIN=0
SEARCH_PRICE_MAX=10000

POLL_SECONDS=10
```

⚠️ Never commit your `.env` file or webhook URL to GitHub.

### Notes

* `SEARCH_QUERY` is the keyword monitored on Mercari JP.
* `POLL_SECONDS` controls how often Mercari is checked for new listings.
* Lower polling intervals may increase the likelihood of rate limiting.
* Never commit your `.env` file or Discord webhook URL to GitHub.


You can find your webhook URL by creating a new channel:
Create a Discord server (or use one you own).
Create a channel like #mercari-alerts.
In Discord:
Edit Channel → Integrations → Webhooks
Create Webhook
Copy the webhook URL

### Environment Variables

| Variable            | Description              |
| ------------------- | ------------------------ |
| DISCORD_WEBHOOK_URL | Discord webhook URL      |
| SEARCH_QUERY        | Mercari search keyword   |
| SEARCH_SIZE         | Search size parameter    |
| SEARCH_REGION       | Search region            |
| SEARCH_SORT         | Sort order               |
| SEARCH_FILTER       | Search filter            |
| SEARCH_PRICE_MIN    | Minimum price            |
| SEARCH_PRICE_MAX    | Maximum price            |
| POLL_SECONDS        | Poll interval in seconds |

---

## Running

```bash
source .venv/bin/activate
python mercari_alert.py
```

---

## Running 24/7 With tmux

Install tmux:

```bash
brew install tmux
```

Create a session:

```bash
tmux new -s mercari
```

Run the bot:

```bash
source .venv/bin/activate
python mercari_alert.py
```

Detach:

```text
Ctrl+B
D
```

Reattach later:

```bash
tmux attach -t mercari
```

---

## First Run Behavior

On first startup, the bot may alert for currently visible listings because the cache file does not yet exist.

Listings are stored in:

```text
seen.json
```

Deleting this file resets the cache.

---

## Security

Never commit:

* `.env`
* Discord webhook URLs
* API keys
* Session files

The included `.gitignore` excludes these automatically.

---

## Disclaimer

This project is intended for personal monitoring and research purposes.

Mercari may change its site structure at any time, which can require updates to scraping selectors.
