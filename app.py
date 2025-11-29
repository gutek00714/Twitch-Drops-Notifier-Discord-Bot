import discord
import sqlite3
from discord import app_commands
import os
import dotenv
import requests
from discord.ext import tasks
from datetime import datetime

# Load environment variables
dotenv.load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Create Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Slash command tree
tree = app_commands.CommandTree(client)


# ===========================
# Slash command: Add a game
# ===========================
@tree.command(
    name="add",
    description="Add a game to a list",
)
async def add_command(interaction: discord.Interaction, game: str):
    """Adds a game for the requesting user to the database"""
    user_id = str(interaction.user.id)

    con = sqlite3.connect("games.db")
    cur = con.cursor()

    cur.execute("INSERT INTO games (user_id, game_name) VALUES (?, ?)", (user_id, game))
    con.commit()
    con.close()

    await interaction.response.send_message(f"Game {game} added")


# ===========================
# Slash command: Remove a game
# ===========================
@tree.command(
    name="remove",
    description="Remove a game from a list",
)
async def remove_command(interaction: discord.Interaction, game: str):
    """Removes a game from user’s tracked game list"""
    user_id = str(interaction.user.id)

    con = sqlite3.connect("games.db")
    cur = con.cursor()

    cur.execute("DELETE FROM games WHERE user_id = ? AND game_name = ?", (user_id, game))
    con.commit()
    con.close()

    await interaction.response.send_message(f"Game {game} removed")


# ===========================
# Slash command: Show user's games
# ===========================
@tree.command(
    name="game_list",
    description="Show game list",
)
async def list_command(interaction: discord.Interaction):
    """Shows all games tracked by any users (global list)"""
    await interaction.response.defer()

    con = sqlite3.connect("games.db")
    cur = con.cursor()

    cur.execute("SELECT DISTINCT game_name FROM games")
    game_list = [row[0] for row in cur.fetchall()]
    con.close()

    await interaction.followup.send(game_list)


# ===========================
# Bot ready event
# ===========================
@client.event
async def on_ready():
    """Runs when the bot logs in"""
    await tree.sync()
    print(f'Logged in as {client.user}')

    # Predefined channel where drop alerts are sent
    global channel
    channel = client.get_channel(1353889308926545933)

    # Start scheduled drop checker
    drop_check.start()


# ===========================
# Scheduled Twitch drop checker
# Runs every hour
# ===========================
@tasks.loop(hours=1)
async def drop_check():
    """
    Checks Twitch Drops API:
    - Fetches live drops
    - Compares with tracked games
    - Avoids duplicate notifications by storing reward IDs in DB
    - Sends embed when a new drop is found
    """

    # Fetch API data
    try:
        data = requests.get("https://twitch-drops-api.sunkwi.com/drops").json()
    except Exception as e:
        print("Failed to fetch Twitch Drops API:", e)
        return

    # Connect to database
    con = sqlite3.connect("games.db")
    cur = con.cursor()

    # Fetch tracked games from DB
    cur.execute("SELECT DISTINCT game_name FROM games")
    user_games = [row[0] for row in cur.fetchall()]

    # Fetch already notified reward IDs
    cur.execute("SELECT DISTINCT rewards_id FROM rewards")
    user_rewards = [row[0] for row in cur.fetchall()]

    print("Tracked games:", user_games)

    # Main drop check loop
    for game_name in user_games:
        for drop in data:

            api_game = drop['gameDisplayName']

            # Compare game names case-insensitively
            if api_game.lower() == game_name.lower():

                api_reward_id = drop['rewards'][0]['id']

                if api_reward_id not in user_rewards:

                    # Store reward to avoid duplicate notifications
                    cur.execute(
                        "INSERT INTO rewards (game_name, rewards_id) VALUES (?, ?)",
                        (game_name.lower(), api_reward_id)
                    )
                    con.commit()

                    # Convert ISO timestamp → Discord timestamp
                    # Example input: "2025-11-30T23:29:59.998Z"
                    raw = drop['endAt'].split('.')[0]  # remove ms
                    dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
                    ts = int(dt.timestamp())

                    # Build embed message
                    embed = discord.Embed(
                        title=drop['gameDisplayName'],
                        description=f"{drop['rewards'][0]['name']}\nEnds <t:{ts}:R>",
                        colour=0x00b0f4
                    )

                    embed.set_author(name="Nowy Twitch drop:")
                    embed.set_image(url=drop['rewards'][0]['imageURL'])

                    # Send notification
                    await channel.send(embed=embed)

    con.close()


# Run the bot
client.run(TOKEN)
