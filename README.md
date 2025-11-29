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
