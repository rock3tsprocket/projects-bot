import logging

from discord.app_commands import command
from discord.ext import commands

from typing import TYPE_CHECKING

from hux.templates.parse import extract_code, CODE_PATTERN

if TYPE_CHECKING:
    from hux.main import Hux

logger = logging.getLogger(__name__)

BF_PATTERN = r"```+[ \t]*(.*?)[ \t]*\n(.*?)```+[ \t]*\n?([^\n]*)?"


class Testing(commands.Cog):
    def __init__(self, bot: Hux):
        self.bot = bot
        self.eval_message_pairs = []

    @commands.command(name="leave_server")
    @commands.is_owner()
    async def leave_server(self, ctx: commands.Context, guild_id: int):
        guild = ctx.guild if guild_id is None else self.bot.get_guild(guild_id)
        logger.info(f"leave_server invoked by {ctx.author} in guild: {ctx.guild}")
        if guild is None:
            await ctx.send("Guild not found.")
            return
        await ctx.send(f"Leaving server **{guild.name}**")
        logger.info(f"Left the server {guild.name} with id {guild.id}")
        await guild.leave()

    @commands.command()
    async def parse_testing(self, ctx: commands.Context, *, code: str) -> None:
        await ctx.send("\n".join(extract_code(BF_PATTERN, code)))


async def setup(bot: Hux):
    await bot.add_cog(Testing(bot))
