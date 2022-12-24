import discord
from discord.ext import commands
from discord.errors import Forbidden


async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="help",
                      usage=" ",
                      description="Shows all available commands")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def help(self, ctx: commands.Context, *input):
        if not input:
            emb = discord.Embed(
                title=f"Bot Command Lists",
                description=f'Use `{self.bot.command_prefix}help <command>` to gain more information about that command '
                f':smiley:\n',
                color=discord.Color.blue())

            for cog in self.bot.cogs:
                for command in self.bot.get_cog(cog).get_commands():
                    if not command.hidden:
                        emb.add_field(
                            name=f"`{self.bot.command_prefix}{command.name}`",
                            value=f"{command.description}",
                            inline=False)

        elif len(input) == 1:
            for cog in self.bot.cogs:
                for command in self.bot.get_cog(cog).get_commands():
                    if command.name.lower() == input[0].lower():
                        emb = discord.Embed(
                            title=f"{command.name}",
                            description=f"`{self.bot.command_prefix}{command.help}`",
                            color=discord.Color.green())
                        break
            else:
                emb = discord.Embed(
                    title="What's that?!",
                    description=f"I've never heard a command called `{input[0]}` before :scream:",
                    color=discord.Color.orange())

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(
                title="That's too much.",
                description="Please request only one command at once :sweat_smile:",
                color=discord.Color.orange())

        else:
            emb = discord.Embed(
                title="It's a magical place.",
                description="I don't know how you got here. But you should've not coming at all.\n",
                color=discord.Color.red())

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)


async def setup(bot: commands.Bot):
    bot.remove_command('help')
    await bot.add_cog(Help(bot))