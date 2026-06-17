import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

class PrivateRoomBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self):
        await self.tree.sync()

bot = PrivateRoomBot()

@bot.event
async def on_ready():
    print(f'Bot connecté et prêt : {bot.user}')

@bot.tree.command(name="create_channel", description="Crée un salon textuel privé")
async def create_channel(interaction: discord.Interaction, channel_name: str):
    guild = interaction.guild
    
    # Configuration des permissions
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
        guild.me: discord.PermissionOverwrite(read_messages=True, view_channel=True, manage_channels=True),
        interaction.user: discord.PermissionOverwrite(
            read_messages=True, 
            view_channel=True, 
            send_messages=True, 
            manage_channels=True
        )
    }
    
    channel = await guild.create_text_channel(
        name=channel_name, 
        overwrites=overwrites, 
        category=interaction.channel.category
    )
    
await interaction.response.send_message(f"✅ Ton espace privé {channel.mention} a été créé !", ephemeral=True)

@bot.tree.command(name="add_member", description="Donne l'accès à un membre pour le salon textuel actuel")
async def add_member(interaction: discord.Interaction, member: discord.Member):
    channel = interaction.channel
    
    if channel.permissions_for(interaction.user).manage_channels:
        await channel.set_permissions(member, read_messages=True, view_channel=True, send_messages=True)
        await interaction.response.send_message(f"👋 Bienvenue {member.mention} ! Tu as été ajouté par {interaction.user.mention}.")
    else:
        await interaction.response.send_message("❌ Tu n'as pas l'autorisation d'ajouter des membres dans ce salon.", ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)
