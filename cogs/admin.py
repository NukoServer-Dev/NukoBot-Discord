from discord.ext import commands
from discord import app_commands
import discord

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.OWNER_ID=1569217425663328276

    @app_commands.command(name="admin", description="Bot管理者用コマンド")
    async def admin_command(self, interaction: discord.Interaction, key: str, value: str, ephemeral: bool = True):
        await interaction.response.defer(ephemeral=ephemeral)

        if interaction.user.id != self.OWNER_ID:
            await interaction.followup.send(embed=discord.Embed(description="Bot管理者のみが使用できます。", color=discord.Color.red()))

        if key == "reload":
            await self.bot.reload_extension("cogs." + value)
            await interaction.followup.send(embed=discord.Embed(description=f"`{value}`をリロードしました。", color=discord.Color.green()))
        elif key == "load":
            await self.bot.load_extension("cogs." + value)
            await interaction.followup.send(embed=discord.Embed(description=f"`{value}`をロードしました。", color=discord.Color.green()))
        elif key == "unload":
            await self.bot.unload_extension("cogs." + value)
            await interaction.followup.send(embed=discord.Embed(description=f"`{value}`をアンロードしました。", color=discord.Color.green()))
        elif key == "sync":
            await self.bot.tree.sync()
            await interaction.followup.send(embed=discord.Embed(description=f"スラッシュコマンドを同期しました。", color=discord.Color.green()))
        elif key == "echo":
            await interaction.followup.send(value)
        else:
            await interaction.followup.send(embed=discord.Embed(description="コマンド: `reload` `load` `unload` `sync`", color=discord.Color.blue()))
        
async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))