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
    
    target_category = guild.get_channel(1516789211683098665)
    
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
        category=target_category
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

@bot.tree.command(name="remove_member", description="Retire l'accès d'un membre à ce salon textuel")
async def remove_member(interaction: discord.Interaction, member: discord.Member):
    channel = interaction.channel
    
    if channel.permissions_for(interaction.user).manage_channels:
        
        if member == interaction.user:
            await interaction.response.send_message("❌ Tu ne peux pas te retirer toi-même de ton propre salon !", ephemeral=True)
            return
            
        await channel.set_permissions(member, overwrite=None)
        await interaction.response.send_message(f"🚪 {member.mention} a été retiré du salon.")
        
    else:
        await interaction.response.send_message("❌ Tu n'es pas le propriétaire de ce salon, tu ne peux virer personne.", ephemeral=True)

@bot.tree.command(name="delete_channel", description="Supprime définitivement ce salon textuel")
async def delete_channel(interaction: discord.Interaction):
    channel = interaction.channel
    
    if channel.permissions_for(interaction.user).manage_channels:
        
        await interaction.response.send_message("💥 Suppression du salon en cours...", ephemeral=True)
        
        await channel.delete()
        
    else:
        await interaction.response.send_message("❌ Tu n'es pas le propriétaire de ce salon, tu ne peux pas le supprimer.", ephemeral=True)
