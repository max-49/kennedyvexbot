import os
import asyncio
import pytz
import discord
from datetime import datetime
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='^', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}!")

@bot.event
async def on_message(ctx):
    if ctx.content.startswith('^') and ctx.author.id != bot.user.id:
        current_time = datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")
        print(f"({current_time}) {ctx.author.name}: {ctx.content}")
    await bot.process_commands(ctx)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        not_found = str(error).split('"')[1]
        await ctx.send(f"Command **`{not_found}`** not found.", allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))

async def main():
    async with bot:
        for filename in os.listdir('cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
        await bot.start(os.getenv('VEXTOKEN'))

asyncio.run(main())