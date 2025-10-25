import discord
import asyncio
from discord import app_commands
from discord import user

active_pings = {}
disabled_users = {1021802390745264229,1370105638574751784}
# set to True to enable activity debug output (console + ephemeral followups when available)
DEBUG_ROBLOX = False
intents = discord.Intents.default()
# enable message content and presence/member intents so we can detect if someone is playing Roblox
intents.message_content = True
intents.members = True
intents.presences = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user} - Slash commands registered!")

@tree.command(name="ping", description="Wypinguj uzytkownika na smierc")
async def ping(interaction: discord.Interaction, user: discord.User):
    
    if user.id in disabled_users:
        await interaction.response.send_message(f"{user.mention} jest odporny... L BOZO")
        return

    # Special case
    if user.id == 712668777938026517:  # Replace with specific user ID
        await interaction.response.send_message(f"{user.mention} Jestes u matyldy, i am angery!")
    if user.id == 1138892016273588224:  # Replace with specific user ID
        await interaction.response.send_message(f"{user.mention} jestes nolife poki nie wylaczysz robloxa")
    else:
        await interaction.response.send_message(f"Alrighty! {user.mention} Szykuj sie na smierc!")
    
    # Only enforce the "playing Roblox" requirement for the specific user.
    target_id = 1138892016273588224
    if user.id == target_id:
        # try to get a Member so we can check current activities
        member = None
        if interaction.guild:
            member = interaction.guild.get_member(user.id)
            if member is None:
                try:
                    member = await interaction.guild.fetch_member(user.id)
                except Exception:
                    member = None

        # DEBUG: show raw activities so we can see what Discord reports
        if DEBUG_ROBLOX:
            try:
                print(f"DEBUG: member={member} activities={getattr(member, 'activities', None)}")
                # send an ephemeral followup so it's visible only to the command user (if allowed)
                acts = getattr(member, 'activities', None)
                act_repr = ', '.join([repr(a) for a in acts]) if acts else '[]'
                await interaction.followup.send(f"DEBUG activities: {act_repr}", ephemeral=True)
            except Exception as e:
                print(f"DEBUG: could not send followup debug: {e}")

        # if the member isn't visible or isn't playing Roblox right now, don't start the ping
        if not member or not _is_playing_roblox(member):
            # use followup because we already used response earlier
            await interaction.followup.send(f"{user.mention} nie gra w bobloxa...")
            return

    # store the channel id where we started the ping so presence handler can notify/stop it
    active_pings[user.id] = interaction.channel.id

    while active_pings.get(user.id):
        await asyncio.sleep(0.1)
        if user.id == 712668777938026517:  # Replace with specific user ID
            await interaction.channel.send(f"{user.mention} napisz 'nie jestem u matyldy'")
        if user.id == 1138892016273588224:  # Replace with specific user ID
            await interaction.channel.send(f"{user.mention} wylacz tego robloxa")
        else:
            await interaction.channel.send(f"{user.mention} jetes gej dopuki nie odpowiesz")


def _is_playing_roblox(member):
    """Return True if member is currently playing Roblox (case-insensitive)."""
    activities = getattr(member, "activities", None)
    if not activities:
        return False
    for act in activities:
        # some activities may not have .type or .name depending on the activity class
    
        try:
            if getattr(act, "type", None) == discord.ActivityType.playing and act.name and "roblox" in act.name.lower():
                return True
        except Exception:
            continue
    return False


@bot.event
async def on_presence_update(before, after):
    """Stop pinging user 1138892016273588224 when they stop playing Roblox."""
    target_id = 1138892016273588224
    uid = after.id
    # only care about the specific user
    if uid != target_id:
        return

    # if we don't have an active ping for them, nothing to do
    channel_id = active_pings.get(uid)
    if not channel_id:
        return

    was_playing = _is_playing_roblox(before)
    is_playing = _is_playing_roblox(after)

    # if they were playing but now stopped, stop the ping
    if was_playing and not is_playing:
        active_pings[uid] = False
        ch = bot.get_channel(channel_id)
        if ch:
            await ch.send(f"<@{uid}> nareszcie nie nolifi w robloxa")

@bot.event
async def on_message(message):
    # Prevent the specific user from stopping their ping by typing.
    target_id = 1138892016273588224
    # If the pinged user types and they're the protected target, ignore them here.
    if message.author.id == target_id and message.author.id in active_pings and active_pings[message.author.id]:
        return

    # only react to messages if the message author is currently being pinged (truthy channel id)
    if message.author.id in active_pings and active_pings[message.author.id]:
        # Special case for another user id
        if message.author.id == 712668777938026517:
            if message.content.lower() == "nie jestem u matyldy":
                active_pings[message.author.id] = False
                await message.channel.send(f"{message.author.mention}, kłamiesz")
        else:
            active_pings[message.author.id] = False
            await message.channel.send(f"{message.author.mention} ok, moja robota zostala skonczona tutaj")

bot.run("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")