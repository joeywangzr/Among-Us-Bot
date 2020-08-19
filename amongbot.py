# Automatically make roles if they are not there
from death import deathMessages
from end import endMessages

import os
import random
import discord
from discord.ext import commands
from discord.utils import get

with open("token.txt", "r") as f:
    lines = f.readlines()
    TOKEN = lines[0].strip()

bot = commands.Bot(command_prefix='=')
bot.remove_command('help')

@bot.command(aliases=['h','help'])
async def _h(ctx):
    await ctx.send('```bot commands:' + '\n' 
    '=h for help' + '\n'
    '=m to mute all in voice channel' + '\n' 
    '=um to unmute all in voice channel```')

@bot.command(aliases=['gc','code','start'])
async def _gc(ctx, code):
    await ctx.send('The game code is ' + code)

@bot.command(aliases=['mute','m','ma'])
async def _m(ctx):
    if discord.utils.get(ctx.guild.roles, name="Head Amonger") not in ctx.author.roles:
        await ctx.send("Only users with the Head Amonger role may use the bot.")
        return
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us')
    for member in voiceChannel.members:
        if discord.utils.get(ctx.guild.roles, name="Dead") in member.roles:
            await member.move_to(discord.utils.get(ctx.guild.voice_channels, name='Dead'))
            await member.edit(mute=False)
        else:
            await member.edit(mute=True)

@bot.command(aliases=['unmute','um','uma'])
async def _um(ctx):
    if discord.utils.get(ctx.guild.roles, name="Head Amonger") not in ctx.author.roles:
        await ctx.send("Only users with the Head Amonger role may use the bot.")
        return
    # voiceChannel = ctx.author.voice.channel
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us')
    for member in voiceChannel.members:
        await member.edit(mute=False)
    deadChannel = discord.utils.get(ctx.guild.voice_channels, name='Dead')
    for deadMember in deadChannel.members:
        await deadMember.edit(mute=True)
        await deadMember.move_to(voiceChannel)
    await ctx.send('All users in voice channel "' + str(ctx.author.voice.channel) + '" have been unmuted!')

@bot.command(aliases=['dead','d'])
async def _d(ctx, user:discord.Member):
    if discord.utils.get(ctx.guild.roles, name="Head Amonger") not in ctx.author.roles:
        await ctx.send("Only users with the Head Amonger role may use the bot.")
        return
    try:
        await ctx.send(user.name + random.choice(deathMessages))
        await user.edit(mute=True)
        await user.add_roles(discord.utils.get(ctx.guild.roles, name="Dead"))
    except:
        await ctx.send('Error: user not connected to voice channel.')

@bot.command(aliases=['end','gg','e']) 
async def _gg(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us')
    deadChannel = discord.utils.get(ctx.guild.voice_channels, name='Dead')
    await ctx.send(random.choice(endMessages))
    for deadMember in deadChannel.members:
        await deadMember.move_to(voiceChannel)
    for member in ctx.guild.members:
        if discord.utils.get(ctx.guild.roles, name="Dead") in member.roles:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Dead"))
            await member.edit(mute=False)

bot.run(TOKEN)

# Feature + detect player status?
# Feature - player set waiting music, other stuff