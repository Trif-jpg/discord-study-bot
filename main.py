import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
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

# Data file constant
DATA_FILE = "data.csv"

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
async def helpme(ctx):
    embed = discord.Embed(title="List of commands:", description="Here are the available commands:")
    embed.add_field(name="-log *<time in minutes>* *[date in DD-MM-YYYY]*", value="Logs your study time. If no date is provided, today's date is used.", inline=False)
    embed.add_field(name="-history", value="Displays your logged study history.", inline=False)
    embed.add_field(name="-stats", value="Displays your total logged study time.", inline=False)
    embed.add_field(name="-leaderboard", value="Displays the top 10 users with the highest logged study time.", inline=False)
    if ctx.author.guild_permissions.administrator:
        embed.add_field(name="-clear", value="*(Admin only)* Clears all logged data.", inline=False)
    await ctx.reply(embed=embed)

@bot.command()
async def log(ctx, time, *, date=None):
    try:
        time = int(time)
    except ValueError:
        embed = discord.Embed(title="Type error!", description="Please make sure that the time you inputted is an **integer number**.")
        await ctx.reply(embed=embed) 
        return
    if time <= 0:
        embed = discord.Embed(title="Wrong Input!", description="Please make sure that the time you inputted is **positive and not zero**.")
        await ctx.reply(embed=embed)
        return
    
    if date is None:
        date = datetime.now().strftime("%d-%m-%Y")
    elif not validate(date):
        embed = discord.Embed(title="Date Format Error!", description="Please make sure that the date you inputted is in the format **DD-MM-YYYY**.")
        await ctx.reply(embed=embed)
        return

    with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as file:
        fieldnames = ["user_id", "time", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({"user_id": str(ctx.author.id), "time": time, "date": date})
    embed = discord.Embed(title="Successfully logged!", description=f"You have logged **{time} minutes** on **{date}**!")
    await ctx.reply(embed=embed)

@bot.command()
async def stats(ctx, user: discord.Member = None):
    total_time = 0
    try:
        with open(DATA_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    if row.get("user_id") == str(user.id if user else ctx.author.id):
                        total_time += int(row.get("time", 0))
                except (ValueError, TypeError):
                    continue
    except FileNotFoundError:
        total_time = 0

    hours = total_time // 60
    minutes = total_time % 60
    if user:
        embed = discord.Embed(title=f"{user.name}'s Study Stats:", description=f"{user.name} has logged a total of **{hours} hours** and **{minutes} minutes**.")
    else:   
        embed = discord.Embed(title="Your Study Stats:", description=f"You have logged a total of **{hours} hours** and **{minutes} minutes**.")
    await ctx.reply(embed=embed)

@bot.command()
async def leaderboard(ctx):
    user_times = {}
    try:
        with open(DATA_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = row.get("user_id")
                try:
                    time = int(row.get("time", 0))
                except (ValueError, TypeError):
                    continue
                if not user_id:
                    continue
                user_times[user_id] = user_times.get(user_id, 0) + time
    except FileNotFoundError:
        embed = discord.Embed(title="No Data!", description="No logged data found.")
        await ctx.reply(embed=embed)
        return

    sorted_users = sorted(user_times.items(), key=lambda x: x[1], reverse=True)[:10]
    lines = []
    for i, (user_id, time) in enumerate(sorted_users):
        try:
            user = await bot.fetch_user(int(user_id))
            user_name = user.name
        except Exception:
            user_name = "Unknown User"
        hours = time // 60
        minutes = time % 60
        lines.append(f"{i+1}. **{user_name}** - {hours} hours and {minutes} minutes")

    description = "\n".join(lines) if lines else "No logged data."
    embed = discord.Embed(title="Leaderboard:", description=description)
    await ctx.reply(embed=embed)

@bot.command()
async def history(ctx, user: discord.Member = None):
    try:
        with open(DATA_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            user_logs = []
            for row in reader:
                if row.get("user_id") == str(user.id if user else ctx.author.id):
                    try:
                        t = int(row.get("time", 0))
                    except (ValueError, TypeError):
                        continue
                    user_logs.append({"time": t, "date": row.get("date", "unknown")})

            if not user_logs:
                if user:
                    embed = discord.Embed(title="No Logs Found!", description=f"{user.name} has no logged time yet.")
                else:
                    embed = discord.Embed(title="No Logs Found!", description="You have no logged time yet.")
                await ctx.reply(embed=embed)
                return

            description_lines = []
            for i, log_ in enumerate(reversed(user_logs)):
                hours = log_["time"] // 60
                minutes = log_["time"] % 60
                description_lines.append(f"{i+1}. **{hours} hours** and **{minutes} minutes** | {log_['date']}")

            description = "\n".join(description_lines)
            if user:
                embed = discord.Embed(title=f"{user.name}'s Log History:", description=description)
            else:
                embed = discord.Embed(title="Your Log History:", description=description)
            await ctx.reply(embed=embed)
    except FileNotFoundError:
        if user:
            embed = discord.Embed(title="No Logs Found!", description=f"{user.name} has no logged time yet.")
        else:
            embed = discord.Embed(title="No Logs Found!", description="You have no logged time yet.")
        await ctx.reply(embed=embed)

# Admin commands
@bot.command()
@has_permissions(administrator=True)
async def clear(ctx):
    open(DATA_FILE, mode="w", encoding="utf-8").close()
    embed = discord.Embed(title="Data Cleared!", description="All logged data has been cleared.")
    await ctx.reply(embed=embed)


# Running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)



