import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import TYPE_CHECKING

from templates import embeds

if TYPE_CHECKING:
    from main import Hux

logger = logging.getLogger(__name__)


class Roles(commands.Cog):
    role_group = app_commands.Group(
        name="role", description="provides information about roles."
    )

    def __init__(self, bot: Hux) -> None:
        self.bot = bot

    @role_group.command(
        name="role", description="Displays information about a given role."
    )
    @app_commands.describe(role="Role which information will be displayed.")
    async def role(
        self, interaction: discord.Interaction, role: discord.Role | None = None
    ) -> None:
        if role is not None:
            logger.info(f"{interaction.user} requested information about role {role}")
            await interaction.response.send_message(embed=await embeds.roleEmbed(role))
        else:
            await interaction.response.send_message("Role not found.")

    @role_group.command(name="list")
    async def role_list(self, interaction: discord.Interaction) -> None:
        logger.info(f"{interaction.user} requested list of roles")
        await interaction.response.send_message(
            embed=await embeds.roleListEmbed(interaction)
        )

    @role_group.command()
    async def count(
        self, interaction: discord.Interaction, *, group: str | None = None
    ) -> None:
        pass


async def setup(bot: Hux) -> None:
    await bot.add_cog(Roles(bot))
