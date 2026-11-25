from discord.ext import commands
from discord import app_commands
import discord

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    def make_embed(self):
        return (discord.Embed(title="コマンドの使い方", color=discord.Color.blue())
        .add_field(name="Minecraft", value="`/mc skin` `/mc version`", inline=False)
        .add_field(name="ダウンロード", value="`/いらすとや`", inline=False)
        .add_field(name="楽しい機能", value="`/omikuji` `/emojis avatar`", inline=False)
        .add_field(name="Bot関連", value="`/help` `/owner`", inline=False)
        .set_footer(text=f"ぬこぬこBot / {len(self.bot.guilds)}サーバー")
        .set_thumbnail(url=self.bot.user.display_avatar.url))

    @app_commands.command(name="help", description="コマンドの使い方")
    async def help_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        await interaction.followup.send(
            embed=self.make_embed(),
            view=discord.ui.View(timeout=None).add_item(discord.ui.Button(label="公式サイト", url="https://nuko-server.xyz/"))
        )

    @commands.command(name="help", description="コマンドの使い方")
    async def help_prefix_command(self, ctx: commands.Context):
        await ctx.send(
            embed=self.make_embed(),
            view=discord.ui.View(timeout=None).add_item(discord.ui.Button(label="公式サイト", url="https://nuko-server.xyz/"))
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))