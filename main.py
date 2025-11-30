import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import logging
from datetime import datetime
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

# Functions
def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%d-%m-%Y").strftime('%d-%m-%Y'):
            raise ValueError
        return True
    except ValueError:
        return False

# Bot events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ID: {bot.user.id}")

# Bot commands
@bot.command()
async def log(ctx, time, *, date=None):
    try:
        time = int(time)
    except ValueError:
        embed = discord.Embed(title="Type error!", description="Please make sure that the time you inputed is an **integer number**.")
        await ctx.reply(embed=embed) 
        return
    if time <= 0:
        embed = discord.Embed(title="Wrong Input!", description="Please make sure that the time you inputed is **positive and not zero**.")
        await ctx.reply(embed=embed)
        return
    
    if date is None:
        date = datetime.now().strftime("%d-%m-%Y")
    elif not validate(date):
        embed = discord.Embed(title="Date Format Error!", description="Please make sure that the date you inputed is in the format **DD-MM-YYYY**.")
        await ctx.reply(embed=embed)
        return

    with open("data.csv", mode="a", newline="") as file:
        fieldnames = ["user_id", "time", "date"] 
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        writer.writerow({"user_id": ctx.author.id, "time": time, "date": date})
    embed = discord.Embed(title="Successfully logged!", description=f"You have logged **{time} minutes** on **{date}**!")
    await ctx.reply(embed=embed)

@bot.command()
async def history(ctx):
    try:
        with open("data.csv", mode="r") as file:
            reader = csv.DictReader(file)
            user_logs = [row for row in reader if row["user_id"] == str(ctx.author.id)]
            
            if not user_logs:
                embed = discord.Embed(title="No Logs Found!", description="You have no logged time yet.")
                await ctx.reply(embed=embed)
                return
            
            description = "\n".join([f"{i+1}. **{int(log['time']) // 60} hours** and **{int(log['time']) % 60} minutes** | {log["date"]}" for i, log in enumerate(reversed(user_logs))])
            embed = discord.Embed(title="Your Log History:", description=description)
            await ctx.reply(embed=embed)
    except FileNotFoundError:
        embed = discord.Embed(title="No Logs Found!", description="You have no logged time yet.")
        await ctx.reply(embed=embed)

@bot.command()
@has_permissions(administrator=True)
async def clear(ctx):
    if MissingPermissions == False:
        embed = discord.Embed(title="Permission Denied!", description="You do not have the required permissions to use this command.")
        await ctx.reply(embed=embed)
        return

    open("data.csv", mode="w").close()
    embed = discord.Embed(title="Data Cleared!", description="All logged data has been cleared.")
    await ctx.reply(embed=embed)


# Running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)



