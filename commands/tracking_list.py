from discord import app_commands, Interaction, Embed

def setup_tracking_list_command(client, players_final):
    @client.tree.command(name="trackinglist", description="Show the list of tracked players")
    async def tracking_list(interaction: Interaction):
        embed = Embed(
            title="Tracked Players List",
            description="\n".join(sorted(players_final)) or "No players are currently being tracked.",
            color=0x22A568
        )
        embed.set_footer(text=f"Total: {len(players_final)} player(s)")
        await interaction.response.send_message(embed=embed)
