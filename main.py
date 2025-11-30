import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import csv

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
    
    with open("data.csv", mode="a", newline="") as file:
        fieldnames = ["user_id", "time"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({"user_id": ctx.author.id, "time": time})
    embed = discord.Embed(title="Successfully logged!", description=f"You have logged **{time} minutes**!")
    await ctx.send(embed=embed)

@bot.command()
async def history(ctx):
    try:
        with open("data.csv", mode="r") as file:
            reader = csv.DictReader(file)
            user_logs = [row for row in reader if row["user_id"] == str(ctx.author.id)]
            
            if not user_logs:
                embed = discord.Embed(title="No Logs Found!", description="You have no logged time yet.")
                await ctx.send(embed=embed)
                return
            
            description = "\n".join([f"{i+1}. **{int(log['time']) // 60} hours** and **{int(log['time']) % 60} minutes**" for i, log in enumerate(reversed(user_logs))])
            embed = discord.Embed(title="Your Log History:", description=description)
            await ctx.send(embed=embed)
    except FileNotFoundError:
        embed = discord.Embed(title="No Logs Found!", description="You have no logged time yet.")
        await ctx.send(embed=embed)


# Running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)



