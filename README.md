# Mercari-JP-Discord-Alert-Bot

A lightweight Playwright-powered Mercari Japan watcher that monitors search results and sends Discord notifications whenever a new listing appears.

## Features

* Monitors Mercari JP search results
* Discord webhook notifications
* Duplicate prevention using a local cache
* Supports one or multiple search queries
* Configurable polling interval
* Supports long-running execution
* Lightweight and easy to self-host
* Supports macOS, Linux, and Windows

---

## Example Notification

Each new listing includes:

* Listing title
* Price
* Product image
* Direct Mercari link

---

## Requirements

* Python 3.10 or newer
* Playwright
* Discord webhook
* Internet connection

Check your Python version:

### macOS or Linux

```bash
python3 --version
```

### Windows PowerShell

```powershell
py --version
```

You can also try:

```powershell
python --version
```

---

# Installation

You can install the project by downloading the ZIP file or cloning it with Git.

## Option 1: Download the ZIP

1. Open the repository on GitHub.
2. Click **Code**.
3. Click **Download ZIP**.
4. Extract the ZIP file.
5. Open a terminal inside the extracted project folder.

Do not try to enter the ZIP file directly with `cd`. The ZIP must be extracted first.

### macOS or Linux

Example:

```bash
cd ~/Downloads/Mercari-JP-Discord-Alert-Bot-main
```

### Windows PowerShell

Example:

```powershell
cd "$HOME\Downloads\Mercari-JP-Discord-Alert-Bot-main"
```

Skip Option 2 and continue to **Create a virtual environment**.

---

## Option 2: Clone with Git

### macOS, Linux, or Windows

```bash
git clone https://github.com/YOUR_USERNAME/Mercari-JP-Discord-Alert-Bot.git
cd Mercari-JP-Discord-Alert-Bot
```

Replace `YOUR_USERNAME` with the correct GitHub username.

---

# Create a Virtual Environment

The activation command is different on macOS/Linux and Windows.

## macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Windows PowerShell

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

You can also create the environment using:

```powershell
python -m venv .venv
```

After activation, the terminal prompt should begin with:

```text
(.venv)
```

Do not use this command in Windows PowerShell:

```bash
source .venv/bin/activate
```

That command is only for macOS and Linux shells.

## Windows Command Prompt

When using Command Prompt instead of PowerShell:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

---

# Install Dependencies

Make sure the virtual environment is activated before continuing.

## macOS or Linux

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Depending on your system, `python` may also work:

```bash
python -m pip install -r requirements.txt
```

## Windows PowerShell

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

# Install Playwright Chromium

## macOS or Linux

```bash
python3 -m playwright install chromium
```

If your activated virtual environment uses `python`:

```bash
python -m playwright install chromium
```

## Windows PowerShell

```powershell
python -m playwright install chromium
```

---

# Configuration

Create a `.env` file inside the project folder.

## macOS or Linux

Run:

```bash
cat > .env <<'EOF'
DISCORD_WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_URL
SEARCH_QUERY=koji kuga,20471120,beauty:beast
POLL_SECONDS=10
EOF
```

## Windows PowerShell

Run:

```powershell
@"
DISCORD_WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_URL
SEARCH_QUERY=koji kuga,20471120,beauty:beast
POLL_SECONDS=10
"@ | Set-Content -Encoding UTF8 .env
```

Replace:

```text
YOUR_DISCORD_WEBHOOK_URL
```

with your actual Discord webhook URL.

Example:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxxxx/xxxxxxxx
SEARCH_QUERY=koji kuga,20471120,beauty:beast
POLL_SECONDS=10
```

Never publish or commit your real Discord webhook URL.

---

## Multiple Search Queries

Monitor multiple searches by separating keywords with commas:

```env
SEARCH_QUERY=koji kuga,20471120,beauty:beast
```

The bot checks each query during every polling cycle and sends alerts for new listings from any query.

Do not add spaces around the commas unless those spaces are intended to be part of the search terms.

---

## Getting a Discord Webhook URL

1. Open Discord.
2. Create a server or use an existing server.
3. Create a text channel, such as `#mercari-alerts`.
4. Open the channel settings.
5. Select **Integrations**.
6. Select **Webhooks**.
7. Click **Create Webhook**.
8. Click **Copy Webhook URL**.
9. Paste the URL into the `DISCORD_WEBHOOK_URL` value in `.env`.

Example:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxxxx/xxxxxxxx
```

Keep this URL private. Anyone with the URL may be able to send messages through the webhook.

---

# Verify the Configuration

## macOS or Linux

```bash
cat .env
```

## Windows PowerShell

```powershell
Get-Content .env
```

You should see:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxxxx/xxxxxxxx
SEARCH_QUERY=koji kuga,20471120,beauty:beast
POLL_SECONDS=10
```

---

# Environment Variables

| Variable              | Description                                             |
| --------------------- | ------------------------------------------------------- |
| `DISCORD_WEBHOOK_URL` | Discord webhook URL                                     |
| `SEARCH_QUERY`        | One or more Mercari search keywords separated by commas |
| `POLL_SECONDS`        | Number of seconds between polling cycles                |

`POLL_SECONDS` controls how often Mercari is checked.

A very low polling interval may increase the risk of rate limiting or temporary blocking. A value such as `30` or `60` may be safer for long-running use.

---

# Running the Bot

Make sure the virtual environment is activated.

## macOS or Linux

```bash
source .venv/bin/activate
python mercari_alert.py
```

If `python` is unavailable:

```bash
python3 mercari_alert.py
```

## Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
python mercari_alert.py
```

Keep the terminal window open while the bot is running.

Stop the bot by pressing:

```text
Ctrl+C
```

---

# Running Continuously on macOS or Linux

You can use `tmux` to keep the bot running after closing the terminal session.

## Install tmux on macOS

```bash
brew install tmux
```

## Install tmux on Ubuntu or Debian Linux

```bash
sudo apt update
sudo apt install tmux
```

## Create a tmux Session

```bash
tmux new -s mercari
```

Activate the virtual environment and run the bot:

```bash
source .venv/bin/activate
python mercari_alert.py
```

Detach from the session:

```text
Ctrl+B
D
```

Reattach later:

```bash
tmux attach -t mercari
```

List available sessions:

```bash
tmux ls
```

Stop the session:

```bash
tmux kill-session -t mercari
```

---

# Running Continuously on Windows

The bot continues running while:

* The computer is powered on
* Windows is not sleeping or hibernating
* The PowerShell window remains open
* The Python process remains running
* The internet connection remains active

## Disable Sleep While Plugged In

Open PowerShell and run:

```powershell
powercfg -change -standby-timeout-ac 0
powercfg -change -hibernate-timeout-ac 0
```

A value of `0` means **Never** while connected to AC power.

Verify the sleep setting:

```powershell
powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE
```

Verify the hibernation setting:

```powershell
powercfg /query SCHEME_CURRENT SUB_SLEEP HIBERNATEIDLE
```

Look for:

```text
Current AC Power Setting Index: 0x00000000
```

That means the setting is configured as **Never** while plugged in.

The monitor may turn off without stopping the bot. Sleep, hibernation, shutdown, restarting Windows, or closing PowerShell will stop the bot

# Disclaimer

This project is intended for personal monitoring and research purposes.

Mercari may change its website structure, anti-bot protections, or search-result format at any time. Such changes may require updates to the Playwright selectors or scraping logic.

Use a reasonable polling interval and comply with applicable website terms, rules, and laws.
