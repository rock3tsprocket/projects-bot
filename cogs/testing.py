import discord
from discord import app_commands
from discord.ext import commands

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Hux


class Testing(commands.Cog):
    def __init__(self, bot: Hux):
        self.bot = bot

    @app_commands.command(name="test", description="Doing funny stuff.")
    @app_commands.describe(text="What the bot will say is a slash command")
    async def test(self, interaction: discord.Interaction, text: str = "This"):
        await interaction.response.send_message(f"{text} is a slash command!")


async def setup(bot: Hux):
    await bot.add_cog(Testing(bot))

