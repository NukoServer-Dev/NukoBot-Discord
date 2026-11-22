from discord.ext import commands
import discord

class ChannelCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    channel = commands.Group(name="channel", aliases=["ch"], description="チャンネル系のコマンド（prefix）")

    @channel.command(name="text", description="テキストチャンネルを作成します。")
    @commands.has_guild_permissions(manage_channels=True)
    @commands.guild_only()
    async def text_create_channel_command(self, ctx: commands.Context, *, channel_name: str):
        try:
            await ctx.guild.create_text_channel(name=channel_name)
            await ctx.message.add_reaction("✅")
        except discord.Forbidden:
            await ctx.reply("権限がありません。")
        except Exception:
            await ctx.reply("エラーが発生しました。")
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelCog(bot))
