import re

import aiohttp

from bs4 import BeautifulSoup
from discord.ext import commands
from discord import app_commands
import discord

IRASUTOTA_REGEX = re.compile(r"https://www\.irasutoya\.com/.+/.+/.+\.html")

class DownloadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="いらすとや", description="いらすとやの画像をダウンロードします。")
    @app_commands.describe(url="いらすとやのurl")
    async def irasutoya_download_command(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()

        if not IRASUTOTA_REGEX.match(url):
            await interaction.followup.send(
                embed=discord.Embed(
                    description="正しいURLを入力してください。", color=discord.Color.red()
                ),
                ephemeral=True,
            )
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                bs4 = BeautifulSoup(await response.text(), "html.parser")
                img = bs4.select(".separator > a")[0]
                title = bs4.find("div", class_="title")

                await interaction.followup.send(embed=discord.Embed(color=discord.Color.green(), title=title.text).set_image(url=img.get("href")), view=discord.ui.View(timeout=None).add_item(discord.ui.Button(url=url, label=title.text)))

async def setup(bot: commands.Bot):
    await bot.add_cog(DownloadCog(bot))