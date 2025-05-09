import discord
import asyncio
from discord import app_commands

active_pings = {}
exempt_users = {1370105638574751784,} #add exceptions (users that can't be pinged) but make sure to keep this id, unless you want the bot to be pinging itself.
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
intents.message_content = True
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user}")

@tree.command(name="ping", description="Ping a specific user until he responds") #change the message accordingly
async def ping(interaction: discord.Interaction, user: discord.User):
    
    if user.id in exempt_users
        await interaction.response.send_message(f"{user.mention} can't be pinged.") #change the message accordingly
        return

    if user == interaction.user:
        await interaction.response.send_message("You can't ping yourself!") #change the message accordingly
        return

    await interaction.response.send_message(f"Alright! {user.mention} will be pinged.") #change the message accordingly
    
    active_pings[user.id] = True

    while active_pings.get(user.id):
        await asyncio.sleep(5) #increase or decrease the time between ping as needed
        await interaction.channel.send(f"{user.mention} please respond to the ping") #change the message accordingly

@bot.event
async def on_message(message):
    if message.author.id in active_pings:
        active_pings[message.author.id] = False
        await message.channel.send(f"{message.author.mention} my work here is done.") #change the message accordingly

bot.run("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") #replace x with your bot id
