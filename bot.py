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
    
    TARGET_CATEGORY_ID = 1516789211683098665
    
    if channel.category_id != TARGET_CATEGORY_ID:
        await interaction.response.send_message("❌ Par sécurité, ce bot ne peut supprimer que les salons situés dans la catégorie des travaux de groupes.", ephemeral=True)
        return # Le "return" arrête immédiatement la fonction ici
    
    if channel.permissions_for(interaction.user).manage_channels:
        
        await interaction.response.send_message("💥 Suppression du salon en cours...", ephemeral=True)
        await channel.delete()
        
    else:
        await interaction.response.send_message("❌ Tu n'es pas le propriétaire de ce salon, tu ne peux pas le supprimer.", ephemeral=True)

@bot.tree.command(name="cesihelp", description="Affiche la liste des commandes et comment les utiliser")
async def cesihelp(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛠️ Guide du Gestionnaire de Salons",
        description="Voici comment créer et gérer tes espaces privés de travail ou de jeu :",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="1️⃣ `/create_channel [channel_name]`",
        value="Crée instantanément un salon textuel secret dans la catégorie dédiée.\n*Exemple : `/create_channel channel_name: cube 2`*",
        inline=False
    )
    
    embed.add_field(
        name="2️⃣ `/add_member [member]`",
        value="Donne les clés de ton salon à un autre utilisateur.\n*Exemple : `/add_member member: @Matthieu`*",
        inline=False
    )
    
    embed.add_field(
        name="3️⃣ `/remove_member [member]`",
        value="Retire l'accès d'une personne à ton salon.\n*Exemple : `/remove_member member: @Arthur`*",
        inline=False
    )
    
    embed.add_field(
        name="4️⃣ `/delete_channel`",
        value="Supprime définitivement le salon actuel. (Uniquement possible si tu en es le créateur et qu'il est dans la bonne catégorie).",
        inline=False
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)
