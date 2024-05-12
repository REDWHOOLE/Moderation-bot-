import discord
from discord.ext import commands
import json

# Load the bot configuration from config.json
with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Define your commands here

@bot.command(name='afk')
@commands.has_permissions(administrator=True)
async def afk_command(ctx):
    await ctx.send(f"{ctx.author.mention} is now AFK.")

@bot.command(name='steal')
@commands.has_permissions(manage_emojis=True)
async def steal_command(ctx, emoji: discord.PartialEmoji, *, name=None):
    await ctx.guild.create_custom_emoji(name=name or emoji.name, image=await emoji.read())
    await ctx.send(f"Emoji {name or emoji.name} stolen!")

@bot.command(name='purge')
@commands.has_permissions(manage_messages=True)
async def purge_command(ctx, count: int = None):
    if count is not None:
        await ctx.channel.purge(limit=count)
    else:
        await ctx.send("You need to specify the number of messages to purge.")

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.display_name} has been banned from the server.")

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.display_name} has been kicked from the server.")

@bot.command(name='temp_role')
@commands.has_permissions(manage_roles=True)
async def temp_role_command(ctx, member: discord.Member, days: int):
    role = await ctx.guild.create_role(name="Temporary Role")
    await member.add_roles(role)
    await ctx.send(f"Temporary role added to {member.mention} for {days} days.")
    # Implement a way to remove the role after the specified time.

@bot.command(name='timer')
async def timer_command(ctx, seconds: int):
    await ctx.send(f"Timer set for {seconds} seconds.")
    # Implement the actual timer functionality.

@bot.command(name='createslot')
@commands.has_permissions(manage_channels=True)
async def createslot_command(ctx, member: discord.Member, *, slot_name):
    category_id = int(config['category_id'])
    category = discord.utils.get(ctx.guild.categories, id=category_id)
    if category:
        new_channel = await ctx.guild.create_text_channel(slot_name, category=category)
        await new_channel.set_permissions(member, read_messages=True, send_messages=True)
        await ctx.send(f"Slot channel '{slot_name}' created for {member.mention}.")
    else:
        await ctx.send("The category ID provided in the config is not valid.")

@bot.command(name='ar')
async def ar_command(ctx):
    if 'ticket' in ctx.message.content.lower():
        await ctx.send("Hi! Welcome To Vintage Shop. Please Discuss Tos and warr with the seller before purchasing and use mm to prevent scams.")
    elif 'slot' in ctx.channel.name.lower():
        await ctx.send("**SLOT RULES**\n"
                       "1. We don't offer any refunds.\n"
                       "2. You can't sell or share your slot.\n"
                       "3. If you promote any server your slot will be revoked.\n"
                       "4. If you scam your slot will get revoked and you will get banned.\n"
                       "5. We can put your slot on hold at any time.\n"
                       "6. If you do not save the transcript of the ticket when you bought it if you or our server will get termed you will not get your slot back.\n"
                       "7. We recommend using MM, if the slot user denies MM, we have the right to revoke your slot.\n"
                       "8. You are not allowed to advertise your server invite or telegram invite.\n"
                       "9. Ping reset: every 24 hours.\n"
                       "10. Positions are never fixed.\n"
                       "11. If we see that your slot is inactive and is hardly used, we have the right to revoke your slot without a refund.\n"
                       "12. We can change the rules whenever we want without further notice.\n"
                       "13. Overpinging will lead to an instant slot revoke without any refund.\n"
                       "14. Inactivity for more than 2 days will result in the removal of the slot (you will be warned first).\n"
                       "15. This slot belongs in 1 category it means slot owner can ping 1 everyone ping and 3 here pings.")

@bot.command(name='adddonater')
@commands.is_owner()
async def adddonater_command(ctx, member: discord.Member):
    donater_role_id = int(config['donater_role_id'])
    donater_role = ctx.guild.get_role(donater_role_id)
    if donater_role:
        await member.add_roles(donater_role)
        await ctx.send(f"{member.mention} has been given the Donater role.")
    else:
        await ctx.send("The Donater role ID provided in the config is not valid.")

@bot.command(name='addslot')
@commands.has_permissions(manage_channels=True)
async def addslot_command(ctx, member: discord.Member):
    slot_channel_name = f"{member.display_name.lower()}-slot"
    slot_channel = discord.utils.get(ctx.guild.text_channels, name=slot_channel_name)
    if slot_channel:
        await slot_channel.set_permissions(member, read_messages=True, send_messages=True)
        await ctx.send(f"Slot owner {member.mention} has been added to their slot channel.")
    else:
        await ctx.send("Slot channel not found.")

@bot.command(name='addpremium')
@commands.has_permissions(manage_roles=True)
async def addpremium_command(ctx, member: discord.Member):
    premium_role_id = int(config['premium_role_id'])
    premium_role = ctx.guild.get_role(premium_role_id)
    if premium_role:
        await member.add_roles(premium_role)
        await ctx.send(f"{member.mention} has been given the Premium User role.")
    else:
        await ctx.send("The Premium User role ID provided in the config is not valid.")

# Error handling and other functionalities

# Run the bot
bot.run(config['token'])
