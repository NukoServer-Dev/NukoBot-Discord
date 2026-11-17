import secrets

from discord.ext import commands
from discord import app_commands
import discord

class OmikujiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="omikuji", description="おみくじを引きます。")
    async def omikuji_command(self, interaction: discord.Interaction):
        await interaction.response.defer()

        res = secrets.choice(["大吉", "中吉", '小吉', '吉', '末吉', '凶', '大凶'])

        await interaction.followup.send(embed=discord.Embed(description=f"<:omikuji:1572069002065481810> {res}", color=discord.Color.blue()))

async def setup(bot: commands.Bot):
    await bot.add_cog(OmikujiCog(bot))