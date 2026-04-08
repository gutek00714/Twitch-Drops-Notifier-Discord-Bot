<!---
# Twitch Drops Notifier — Discord Bot

A simple Discord bot written in Python that notifies users about new Twitch Drops for the games they track.

The bot:
- Stores user-added game names in a local SQLite database
- Periodically checks the Twitch Drops API
- Detects new rewards (`reward_id`) that were not previously notified
- Sends a Discord embed to a chosen channel
- Prevents duplicate notifications using a separate `rewards` table

---

## Features

- `/add <game>` — add a game to the tracked list  
- `/remove <game>` — remove a game  
- `/game_list` — list all tracked games  
- Automatic periodic Twitch Drops scanning  
- Sends embed messages with:
  - Game name  
  - Reward name  
  - End time as a Discord timestamp  
  - Reward image  
- Tracks previously sent reward IDs to prevent duplicates

---

## Installation

### 1. Create '.env' file
Create a `.env` file:
BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN

### 2. Initialize the Database

Run:
python games_db.py

---

## Running the Bot


The bot will automatically:
- Sync slash commands  
- Start the Twitch Drops checking loop  

Make sure the channel ID in `app.py` is correct:

```python
channel = client.get_channel(1353889308926545933)
```

---

## How It Works (Simple Overview)

1. Users add games using the /add <game> command.
2. The bot stores all tracked game names in a local SQLite database (games table).

3. Every hour, the bot:
   - Fetches the latest Twitch Drops API data.
   - Checks only the games that exist in the SQLite database.

4. For each tracked game, the bot compares the API drop data to see if it applies.

5. Each drop contains a unique reward ID.
   The bot checks whether this reward ID already exists in the rewards table.

6. If the reward ID is new:
   - The bot sends a Discord embed with:
     • Game name
     • Reward name
     • End time (Discord timestamp)
     • Reward image
   - The bot then saves the reward ID to the rewards table.

7. If the reward ID already exists, the bot does nothing.
   This prevents duplicate notifications.
   -->
# Twitch Drops Notifier — Discord Bot

A simple Discord bot written in Python that notifies users about new Twitch Drops for the games they track.

---

## Motivation

Keeping up with Twitch Drops manually is tedious — you have to check each game's drop page individually and hope you don't miss a limited-time reward. This bot automates that entirely. It watches the Twitch Drops API on your behalf, detects new rewards as soon as they appear, and delivers a clean Discord embed straight to your server — so you never miss a drop again.

---

## Features

- `/add <game>` — add a game to the tracked list
- `/remove <game>` — remove a game
- `/game_list` — list all tracked games
- Automatic periodic Twitch Drops scanning
- Sends embed messages with:
  - Game name
  - Reward name
  - End time as a Discord timestamp
  - Reward image
- Tracks previously sent reward IDs to prevent duplicates

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/twitch-drops-notifier
cd twitch-drops-notifier
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file
BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN

### 4. Initialize the database

```bash
python games_db.py
```

### 5. Run the bot

```bash
python app.py
```

Make sure the channel ID in `app.py` is set to your target Discord channel:

```python
channel = client.get_channel(YOUR_CHANNEL_ID)
```

---

## Usage

Once the bot is running and invited to your server, use the following slash commands:

| Command | Description |
|---|---|
| `/add <game>` | Start tracking a game for Twitch Drops |
| `/remove <game>` | Stop tracking a game |
| `/game_list` | View all currently tracked games |

The bot runs a check every hour automatically. Here's what happens under the hood:

1. Users add games via `/add <game>` — stored in a local SQLite database.
2. Every hour, the bot fetches the latest Twitch Drops API data.
3. For each tracked game, it checks for drop rewards it hasn't seen before (by `reward_id`).
4. If a new reward is found, the bot sends a Discord embed and saves the `reward_id` to prevent duplicate notifications.

---

## Contributing

### Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/twitch-drops-notifier
cd twitch-drops-notifier
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the bot locally

```bash
python app.py
```

### Submit a pull request

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.
