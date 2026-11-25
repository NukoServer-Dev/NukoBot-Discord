import traceback
from discord.ext import commands
import discord
from tools import permissions_text

class ErrorHandleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @bot.tree.error
        async def on_app_command_error(
            interaction: discord.Interaction,
            error: discord.app_commands.AppCommandError,
        ):
            if isinstance(error, discord.app_commands.CommandOnCooldown):
                e = 0
                return e

            if isinstance(error, discord.app_commands.CommandNotFound):
                e = 0
                return e

            if isinstance(error, discord.app_commands.MissingPermissions):
                missing_perms = [
                    permissions_text.PERMISSION_TRANSLATIONS.get(perm, perm)
                    for perm in error.missing_permissions
                ]
                missing_perms_str = ", ".join(missing_perms)
                embed = discord.Embed(
                    title="コマンドを実行する権限がありません。",
                    description=f"不足している権限: {missing_perms_str}",
                    color=discord.Color.red()
                )
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        embed=embed,
                        ephemeral=True,
                    )
                return

            if isinstance(getattr(error, "original", error), discord.Forbidden):
                embed = discord.Embed(
                    title="権限エラーが発生しました。",
                    description="Botにこの操作を行うための権限（ロールやチャンネル権限）がありません。",
                    color=discord.Color.red()
                )
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        embed=embed,
                        ephemeral=True,
                    )
                else:
                    await interaction.followup.send(embed=embed)
                return

            traceback.print_exception(error)

            embed = discord.Embed(
                title="予期しないエラーが発生しました。",
                description=f"エラーコード```{error}```",
                color=discord.Color.red()
            )
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ErrorHandleCog(bot))