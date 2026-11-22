import io

import aiohttp
from discord.ext import commands
from discord import app_commands
import discord
import urllib.parse

from models.mcJava import MCJavaVersion

class MinecraftCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    mc = app_commands.Group(name="mc", description="Minecraftに関するコマンド")

    @mc.command(name="skin", description="Minecraftプレイヤーのスキンを表示します。")
    @app_commands.describe(mcid="mcidを入力")
    async def skin_command(self, interaction: discord.Interaction, mcid: str):
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://mc-heads.net/body/{urllib.parse.quote(mcid)}/200") as skin:
                skin_res = await skin.read()
                skin_io = io.BytesIO(skin_res)
                await interaction.followup.send(file=discord.File(skin_io, filename="skin.png"), view=discord.ui.View(timeout=None).add_item(discord.ui.Button(label=f"{mcid}のスキン", disabled=True)))
                skin_io.close()

    async def version_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        auto_comp_list = []
        async with aiohttp.ClientSession() as session:
            async with session.get("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json") as resp:
                version_json = await resp.json()
                for version in version_json.get('versions', []):
                    versionClass = MCJavaVersion(**version)
                    if current in versionClass.id or not current:
                        auto_comp_list.append(app_commands.Choice(name=versionClass.id, value=versionClass.id))
        return auto_comp_list

    @mc.command(name="version", description="MinecraftJavaのバージョンを検索します。")
    @app_commands.describe(version="指定しない場合は最新バージョン")
    @app_commands.autocomplete(version=version_autocomplete)
    async def version_command(self, interaction: discord.Interaction, version: str = None):
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json") as resp:
                version_json = await resp.json()
                for version in version_json.get('versions', []):
                    versionClass = MCJavaVersion(**version)
                    if versionClass.id == version or not version:
                        await interaction.followup.send(
                            embed=discord.Embed(title=versionClass.id, color=discord.Color.green())
                            .add_field(name="タイプ", value=versionClass.type, inline=True)
                            .add_field(name="リリース時期", value=versionClass.releaseTime, inline=True)
                            .add_field(name="リリースの詳細URL", value=versionClass.url, inline=False)
                        )
                        return

                await interaction.followup.send(
                    embed=discord.Embed(description="バージョンが見つかりませんでした。", color=discord.Color.red())
                )

async def setup(bot: commands.Bot):
    await bot.add_cog(MinecraftCog(bot))
