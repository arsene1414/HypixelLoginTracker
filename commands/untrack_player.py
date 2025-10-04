from discord import app_commands, Interaction

def setup_untrack_command(client, players_final):
    @client.tree.command(name="untrackplayer", description="Remove a player from the tracking list")
    @app_commands.describe(player_name="Name of the player to remove")
    async def untrack_player(interaction: Interaction, player_name: str):
        await interaction.response.send_message(f"Removing `{player_name}` from the list...", ephemeral=True)

        if player_name in players_final:
            players_final.remove(player_name)
            with open("names.txt", "w") as f:
                f.write("\n".join(players_final))
            await interaction.edit_original_response(content=f":white_check_mark: `{player_name}` was successfully removed.")
        else:
            await interaction.edit_original_response(content=f":x: `{player_name}` is not in the list.")
