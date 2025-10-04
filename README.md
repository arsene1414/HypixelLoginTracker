# Hypixel Login Tracker Bot

A Discord bot to track Hypixel player logins in real-time.

## Features

- Tracks multiple Hypixel players

- Notifies a Discord channel when a player logs in

- Slash commands to add/remove players and view the tracking list

- Fully asynchronous for smooth operation

- Safe use of environment variables for API keys and tokens

Every Python package needed :

```bash
pip install -r requirements.txt
```

## Configuration

#### Configure the bot

Rename the `example.env` file to `.env`


| Parameter | Description                |
| :-------- | :------------------------- |
| `BOT_TOKEN` | The Bot Token |
| `API_KEY` |Your Hypixel API key |
| `PING_DISCORD_CHANNEL_ID` | The Discord channel ID where you want to recieve notifications when a player log on Hypixel |