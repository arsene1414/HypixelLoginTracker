from discord import app_commands, Interaction
import aiohttp

def setup_track_command(client, players_final, api):
    @client.tree.command(name="trackplayer", description="Add a player to the tracking list")
    @app_commands.describe(player_name="Hypixel player name")
    async def track_player(interaction: Interaction, player_name: str):
        await interaction.response.send_message(f"Adding `{player_name}` to the tracking list...", ephemeral=True)

        if player_name in players_final:
            await interaction.edit_original_response(content=f":warning: `{player_name}` is already being tracked.")
            return

        async with aiohttp.ClientSession() as session:
            data = await api.get_player_data(player_name, session)

        if data and data.get("player"):
            players_final.append(player_name)
            with open("names.txt", "w") as f:
                f.write("\n".join(players_final))
            await interaction.edit_original_response(content=f":white_check_mark: `{player_name}` has been added successfully.")
        else:
            await interaction.edit_original_response(content=f":x: `{player_name}` is invalid or the API is unavailable.")
