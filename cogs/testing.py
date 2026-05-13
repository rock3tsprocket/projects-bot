import discord
from discord import app_commands
from discord.ext import commands

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test", description="Doing funny stuff.")
    @app_commands.describe(text="What the bot will say is a slash command")
    async def test(self, interaction: discord.Interaction, text: str = "This"):
        await interaction.response.send_message(f"{text} is a slash command!")
    



























async def setup(bot):
    await bot.add_cog(Testing(bot))