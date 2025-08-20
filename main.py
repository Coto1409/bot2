# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')
    
@bot.command()
async def userinfo(ctx, member: discord.Member):
    """Displays information about a user."""
    embed = discord.Embed(title=f'User Info for {member.name}', color=discord.Color.blue())
    embed.add_field(name='ID', value=member.id)
    embed.add_field(name='Joined at', value=discord.utils.format_dt(member.joined_at))
    embed.add_field(name='Created at', value=discord.utils.format_dt(member.created_at))
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)
    
@bot.command()
async def serverinfo(ctx):
    """Displays information about the server."""
    embed = discord.Embed(title=f'Server Info for {ctx.guild.name}', color=discord.Color.green())
    embed.add_field(name='Server ID', value=ctx.guild.id)
    embed.add_field(name='Created at', value=discord.utils.format_dt(ctx.guild.created_at))
    embed.add_field(name='Member Count', value=ctx.guild.member_count)
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else ctx.guild.default_icon.url)
    await ctx.send(embed=embed)


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


bot.run('token')
