import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# Getting the bot token from environment variables
load_dotenv()
token = os.getenv("token")

# Setting up logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Setting up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Creating the bot instance
bot = commands.Bot(command_prefix='-', intents=intents)

# Bot events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ID: {bot.user.id}")

# Bot commands
@bot.command()
async def log(ctx, time):
    try:
        time = int(time)
    except ValueError:
        embed = discord.Embed(title="Type error!", description="Please make sure that the time you inputed is an **integer number**.")
        await ctx.send(embed=embed) 
        return
    if time <= 0:
        embed = discord.Embed(title="Wrong Input!", description="Please make sure that the time you inputed is **positive and not zero**.")
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(title="Successfully logged!", description=f"You have logged **{time} minutes**!")
    await ctx.send(embed=embed)


# Running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)



