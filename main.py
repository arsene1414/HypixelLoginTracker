import discord
import requests
from discord.ext import commands
from discord import Intents
from discord import app_commands
import asyncio

TOKEN = "BOT_TOKEN"
apikey = "API_KEY"
channelID = int("PING_DISCORD_CHANNEL_ID")

#open the names file and convert it to a list with all names
file=open('names.txt', 'a')
file.close()
file=open('names.txt', 'r')
players = []
players2 = []
for line in file:
    line_strip=line.strip()
    line_split=line_strip.split()
    players.append(line_split)
    for i in players:
        for j in i:
            players2.append(j)

#remove duplicates
players_final = []
for item in players2:
    if item not in players_final:
        players_final.append(item)

file.close()


intents = Intents.all()
intents.members = True
client = commands.Bot(command_prefix='%', help_command=None, intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Hypixel Login Tracker.'))
    print("Bot strated with the name of {0.user}".format(client))
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} command")
    except Exception as e:
        print(e)
    while 1 == 1:
        try:
            for item in players_final:
                requestlink = str("https://api.hypixel.net/player?key=" + apikey + "&name=" + item)
                hydata = requests.get(requestlink).json()
                APIcooldown = hydata["success"]
                if APIcooldown is False:
                    print(f"{item}'s API is in COOLDOWN")
                    pass
                elif APIcooldown is True:
                    apiOK = hydata["player"].get("lastLogin")
                    if apiOK == None:
                        pass
                    else:
                        lastlogin = hydata["player"]["lastLogin"]
                        lastlogout = hydata["player"]["lastLogout"]
                        if lastlogin > lastlogout:
                            print(f"{item} is online")
                            channel = client.get_channel(channelID)
                            await channel.send(f"@everyone , `{item}` is online on hypixel right now !")
                        else:
                            pass
                else:
                    pass
            await asyncio.sleep(300)
        except TypeError or KeyError:
            print("An error has occured, API is probably in cooldown.")
            pass


@client.tree.command(name="trackplayer")
@app_commands.describe(player_name = "Player name")
async def addsnipe(interaction: discord.Interaction, player_name: str):
    await interaction.response.send_message(f"Adding `{player_name}` to the tracking list...", ephemeral=True)
    if player_name in players_final:
        await interaction.edit_original_response(content=f":warning: {interaction.user.mention}, Player `{player_name}` is already on the tracking list !")
        print(f"Player {player_name} is already here")
    else:
        requestlink = str("https://api.hypixel.net/player?key=" + apikey + "&name=" + player_name)
        try:
            hydata = requests.get(requestlink).json()
            APIcooldownAdd = hydata["success"]
            if APIcooldownAdd == True:
                ValidName = hydata["player"]
                if ValidName is None:
                    await interaction.edit_original_response(content=f":x: {interaction.user.mention}, `{player_name}` isn't a valid username !")
                else:
                    await interaction.edit_original_response(content=f":white_check_mark: Player `{player_name}` was successfully added to the tracking list !")
                    players_final.append(player_name)
                    with open("names.txt", "w") as outfile:
                        listeprint = '\n'.join(players_final)
                        outfile.writelines(listeprint)
                    print(f"added player {player_name} to the sniping list")
            else:
                await interaction.edit_original_response(content=f":x: {interaction.user.mention}, `{player_name}`'s API is in cooldown, please try again later.")
        except TypeError or KeyError:
            await interaction.edit_original_response(content=f":x: {interaction.user.mention}, an error has occurred, please try again later !")
            pass


@client.tree.command(name="untrackplayer")
@app_commands.describe(player_name = "Player name")
async def removesnipe(interaction: discord.Interaction, player_name: str):
    await interaction.response.send_message(f"Removing `{player_name}` from the tracking list...", ephemeral=True)
    if player_name in players_final:
        players_final.remove(player_name)
        with open("names.txt", "w") as outfile:
            listeprint = '\n'.join(players_final)
            outfile.writelines(listeprint)
        await interaction.edit_original_response(content=f":radioactive: Player `{player_name}` was successfully removed from the tracking list !")
        print(f"removed player {player_name} from the tracking list")
    else:
        await interaction.edit_original_response(content=f":x: {interaction.user.mention}, the username `{player_name}` wasn't found in the tracking list !")
        print(f"player {player_name} wasn't found on the tracking list")


@client.tree.command(name="trackinglist")
async def snipelist(interaction: discord.Interaction):
    SPnumber = len(players_final)
    embedlist = discord.Embed(title="Tracked players list :", description="\n".join(sorted(players_final)), color=0x22a568)
    if SPnumber == 1:
        embedlist.set_footer(text=f"Currently tracking {SPnumber} player.")
    else:
        embedlist.set_footer(text=f"Currently tracking {SPnumber} players.")
    await interaction.response.send_message(embed=embedlist)


client.run(TOKEN)
