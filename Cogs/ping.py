import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping",
                      usage=" ",
                      description="Return User's Ping")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
