from discord.ext import commands
import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hux.main import Hux

logger = logging.getLogger(__name__)


class Testing(commands.Cog):
    def __init__(self, bot: Hux):
        self.bot = bot

    @commands.command(name="leave_server")
    @commands.is_owner()
    async def leave_server(self, ctx: commands.Context):
        if ctx.guild is not None:
            await ctx.send(f"Leaving server {ctx.guild.name}")
            await ctx.guild.leave()
            logger.info(f"Left the server {ctx.guild.name} with id **{ctx.guild.id}**")


async def setup(bot: Hux):
    await bot.add_cog(Testing(bot))
