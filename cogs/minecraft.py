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
            async with session.get(f'https://api.mojang.com/users/profiles/minecraft/{urllib.parse.quote(mcid)}') as uuid:
                if uuid.status != 200:
                    await interaction.followup.send(embed=discord.Embed(description=f"MojangAPIがダウンしています。", color=discord.Color.red()))
                    return

                uuid_json = await uuid.json()
                uuidGet = uuid_json.get('id')
                if not uuidGet:
                    await interaction.followup.send(embed=discord.Embed(description=f"UUIDの取得に失敗しました。", color=discord.Color.red()))
                    return

                await interaction.followup.send(embed=discord.Embed(title=f"{mcid}のスキン").add_field(name="UUID", value=uuidGet, inline=False).set_image(url=f"https://mc-heads.net/body/{mcid}/200"))

async def setup(bot: commands.Bot):
    await bot.add_cog(MinecraftCog(bot))