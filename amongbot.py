# Automatically make roles if they are not there, also automatically add permissions (dead cannot speak in among us)
# Ignore capitalization
# Discord server owner setup initialization (input role names, channel names)
# unmute self, unmute specific persno, mute specific person
# set custom channel for each discord server
# add embeds 
from death import deathMessages
from death import endMessages

import os
import random
import discord
from discord.ext import commands
from discord.utils import get

players = []

with open('token.txt', 'r') as f:
    lines = f.readlines()
    TOKEN = lines[0].strip()

bot = commands.Bot(command_prefix='~')
bot.remove_command('help')

# Starts the bot, with a status.
@bot.event
async def on_ready():
    print('Amonger is online!')
    await bot.change_presence(status = discord.Status.online, activity=discord.Game('=help'))

# Error handling.
@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title='```ERROR```', description='Invalid argument.', colour=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(aliases=['h','help'])
async def _h(ctx):
    await ctx.send('```bot commands:' + '\n' 
    '=h for help' + '\n'
    '=m to mute all in voice channel' + '\n' 
    '=um to unmute all in voice channel```')

@bot.command(aliases=['gc','code','start'])
async def _gc(ctx, code):
    embed = discord.Embed(title='GAME CODE:', description='**'+code+'**', colour=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(aliases=['mute','m','ma'])
async def _m(ctx):
    global players
    players = []
    if discord.utils.get(ctx.guild.roles, name='Head Amonger') not in ctx.author.roles:
        await ctx.send('```Only users with the Head Amonger role may use the bot.```')
        return
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us')
    for member in voiceChannel.members:
        if discord.utils.get(ctx.guild.roles, name='Dead') not in member.roles:
            await member.edit(mute=True)
        else:
            await member.edit(mute=False)
            await member.move_to(discord.utils.get(ctx.guild.voice_channels, name='Dead'))
    embed = discord.Embed(description='All users in voice channel "' + str(ctx.author.voice.channel) + '" have been muted!', colour=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(aliases=['unmute','um','uma'])
async def _um(ctx):
    global players
    players = []
    if discord.utils.get(ctx.guild.roles, name='Head Amonger') not in ctx.author.roles:
        await ctx.send('```Only users with the Head Amonger role may use the bot.```')
        return
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us')
    deadChannel = discord.utils.get(ctx.guild.voice_channels, name='Dead')
    for member in deadChannel.members:
        # await member.edit(mute=True)
        await member.move_to(discord.utils.get(ctx.guild.voice_channels, name='Among Us'))
        await member.edit(mute=True)
    for member in voiceChannel.members:
        if discord.utils.get(ctx.guild.roles, name='Dead') not in member.roles:
            await member.edit(mute=False)
    embed = discord.Embed(description='All users in voice channel "' + str(ctx.author.voice.channel) + '" have been unmuted!', colour=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(aliases=['dead','d'])
async def _d(ctx, user:discord.Member):
    global players
    players = []
    if discord.utils.get(ctx.guild.roles, name='Head Amonger') not in ctx.author.roles:
        await ctx.send('```Only users with the Head Amonger role may use the bot.```')
        return
    # try:# users can mute themselves if they die
    embed = discord.Embed(description=user.name + random.choice(deathMessages), colour=discord.Color.orange())
    await ctx.send(embed=embed)
    await user.edit(mute=True)
    await user.add_roles(discord.utils.get(ctx.guild.roles, name='Dead'))

@bot.command(aliases=['end','gg','e']) 
async def _gg(ctx):
    global players
    players = []
    embed = discord.Embed(description=random.choice(endMessages), colour=discord.Color.orange())
    await ctx.send(embed=embed)
    deadChannel = discord.utils.get(ctx.guild.voice_channels, name='Dead')
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us')
    for member in deadChannel.members:
        await member.move_to(voiceChannel)
    for member in voiceChannel.members:
        await member.edit(mute=False)
    for member in ctx.guild.members:
        if discord.utils.get(ctx.guild.roles, name='Dead') in member.roles:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name='Dead'))

@bot.command(aliases=['play','p'])
async def _p(ctx):
    global players
    players.append(ctx.author.name)
    embed = discord.Embed(title=str(ctx.author.name) + ' wants to play Among Us!', description='There are ' + len(players) + ' in the party. Type =p to join!')
    await ctx.send(embed=embed)

@bot.command(aliases=['exit','e'])
async def _e(ctx):
    global players
    players.remove(ctx.author.name)
    embed = discord.Embed(description='You have been removed from the queue. Type =p to rejoin!')
    await ctx.send(embed=embed)

@bot.command(aliases=['queue','q'])
async def _q(ctx):
    global players
    embed = discord.Embed(title='**QUEUE:**',description=players + ' are all in the queue.')
    await ctx.send(embed=embed)

bot.run(os.environ(['TOKEN']))

# Feature + detect player status?
# Feature - player set waiting music, other stuff