from discord.ext import commands
from discord import app_commands
import discord


class EmojisCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    emojis = app_commands.Group(
        name="emojis",
        description="絵文字に関するコマンド",
        allowed_installs=app_commands.AppInstallationType(user=False, guild=True),
    )

    @emojis.command(
        name="avatar",
        description="ユーザーのアバターの絵文字を作成します。"
    )
    @app_commands.describe(user="discordのユーザーを入力")
    @app_commands.default_permissions(create_expressions=True)
    @app_commands.allowed_installs(guilds=True, users=False)
    async def avatar_emoji_command(
        self,
        interaction: discord.Interaction,
        user: discord.User = None
    ):
        await interaction.response.defer()

        user = user or interaction.user
        avatar = await user.display_avatar.read()

        try:
            emoji = await interaction.guild.create_custom_emoji(
                name=user.name.lower().replace(" ", "_").replace("　", "_"),
                image=avatar,
                reason=f"{interaction.user.name}により作成"
            )
        except Exception as e:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="予期しないエラーが発生しました。",
                    description=f"```{e}```",
                    color=discord.Color.red()
                )
            )
            return

        await interaction.followup.send(
            embed=discord.Embed(
                description=f"{emoji} {user.mention}のアバター絵文字を作成しました。",
                color=discord.Color.blue()
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(EmojisCog(bot))