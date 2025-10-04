import discord
from discord.ext import commands
from discord import Intents
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

from hypixel_api import HypixelAPI
from commands.track_player import setup_track_command
from commands.untrack_player import setup_untrack_command
from commands.tracking_list import setup_tracking_list_command

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

with open("names.txt", "a") as f:
    pass

with open("names.txt", "r") as f:
    players_final = list({line.strip() for line in f if line.strip()})

intents = Intents.all()
client = commands.Bot(command_prefix="%", help_command=None, intents=intents)
api = HypixelAPI(HYPIXEL_API_KEY)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Hypixel Login Tracker v2"))
    print(f"Bot connected as {client.user}")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} commands synced.")
    except Exception as e:
        print(f"Command sync error: {e}")

    channel = client.get_channel(CHANNEL_ID)
    session = aiohttp.ClientSession()

    try:
        while True:
            for player in players_final:
                data = await api.get_player_data(player, session)
                if data and api.is_player_online(data):
                    print(f"{player} is online")
                    if channel:
                        await channel.send(f"@everyone `{player}` is currently online on Hypixel!")
                else:
                    print(f"{player} is offline")
                await asyncio.sleep(2)
            await asyncio.sleep(300)
    finally:
        await session.close()

setup_track_command(client, players_final, api)
setup_untrack_command(client, players_final)
setup_tracking_list_command(client, players_final)

client.run(DISCORD_TOKEN)
