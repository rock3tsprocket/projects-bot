import discord
from discord.ext import commands
import logging
import os
import asyncio
import subprocess
from dotenv import load_dotenv
from data.database import Database

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

COGS = [
    "cogs.info",
    "cogs.moderation",
    "cogs.fun",
    "cogs.projects",
    "cogs.snippets",
    "cogs.warns",
    "cogs.testing",
    "cogs.code",
]


class Hux(commands.Bot):
    db: Database

    def __init__(self, prefix: str):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.typing = True
        intents.presences = True
        intents.guilds = True
        intents.moderation = True
        self.prefix = prefix

        super().__init__(
            command_prefix=commands.when_mentioned_or(self.prefix), intents=intents
        )

    async def on_ready(self) -> None:
        print(f"{self.user} is ready and online!")

    async def setup_hook(self) -> None:
        self.db = Database("data/bot.db")
        await self.db.setup()

        for cog in COGS:
            await self.load_extension(cog)

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands.")

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do this!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("User not found!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument: `{error.param.name}`")
        elif isinstance(error, discord.Forbidden):
            await ctx.send("I don't have permission to do that.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "Command has a bad argument. Check all parameter are correct."
            )
        elif isinstance(error, commands.NotOwner):
            await ctx.send("Only Saber can access this command.")
        elif isinstance(error, subprocess.TimeoutExpired):
            await ctx.send("Subprocess timed out.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("The command is still in cooldown.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The comamnd can only be used on a server.")
        elif isinstance(error, commands.CommandNotFound):
            pass


async def main() -> None:
    discord.utils.setup_logging(handler=handler, level=logging.DEBUG)
    token = str(os.getenv("TOKEN"))
    async with Hux("!") as hux:
        await hux.start(token)


asyncio.run(main())
