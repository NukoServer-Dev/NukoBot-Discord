import io

import aiohttp
from discord.ext import commands
from discord import app_commands
import discord
import urllib.parse

class MinecraftCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="skin", description="Minecraftスキンを表示します。")
    @app_commands.describe(mcid="mcidを入力")
    async def skin_command(self, interaction: discord.Interaction, mcid: str):
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://mc-heads.net/body/{urllib.parse.quote(mcid)}/200") as skin:
                skin_res = await skin.read()
                skin_io = io.BytesIO(skin_res)
                await interaction.followup.send(file=discord.File(skin_io, filename="skin.png"), view=discord.ui.View(timeout=None).add_item(discord.ui.Button(label=f"{mcid}のスキン", disabled=True)))
                skin_io.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(MinecraftCog(bot))