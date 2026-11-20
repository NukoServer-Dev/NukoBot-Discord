from discord.ext import commands
import discord
import dotenv
import os

dotenv.load_dotenv()

intents = discord.Intents.none()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def setup_hook():
    await bot.load_extension("cogs.download")
    await bot.load_extension("cogs.omikuji")
    await bot.load_extension("cogs.minecraft")
    await bot.tree.sync()

if __name__ == "__main__":
    bot.run(os.environ.get('DISCORD_TOKEN'))