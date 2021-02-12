import os
import json
import datetime

# Load in data files here:
os.chdir('data')
with open('presentations.json', 'r') as f:
    presentations = json.load(f)
os.chdir('../')

CURRENT_TERM = 'spring2021'

formattedPresentations = []
for i in presentations[CURRENT_TERM]:
    formattedPresentations.append([
        datetime.datetime(i[0], i[1], i[2], 12, 0),
        i[3]
    ])

from discord import errors
from discord.ext import commands
from discord import utils
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='commands', help='Returns the list of possible bot commands')
async def getCommands(ctx):
    commands = (
            '!github: returns the github link for the bot! \n'
            '!createTextChannel [insert name]: create a discord text channel with a given name\n'
            '!createVoiceChannel [insert name]: create a discord voice channel with a given name\n'
        )
    await ctx.send(commands)

@bot.command(name='github', help='Provides a link to the Discord server bot source code')
async def github(ctx):
    githubLink = (
            'Interested in how this bot functions? Head over to the github repository containing the source code below: \n'
            'Github: https://github.com/aday913/BSL-Discord-Bot'
        )

    await ctx.send(githubLink)

@bot.command(name='createTextChannel', help='Will create a text channel if a user with admin privileges wants to')
async def createTextChannel(ctx, channelName):
    guild = ctx.guild
    existing_channel = utils.get(guild.channels, name=channelName)
    if not existing_channel:
        await guild.create_text_channel(channelName)

@bot.command(name='createVoiceChannel', help='Will create a voice channel if a user with admin privileges wants to')
async def createVoiceChannel(ctx, channelName):
    guild = ctx.guild
    existing_channel = utils.get(guild.channels, name=channelName)
    if not existing_channel:
        await guild.create_voice_channel(channelName)

@bot.command(name='presentations', help='Lists all presentations for the current term')
async def getPresentations(ctx):
    responseText = 'Presentation schedule:\n'
    for date in formattedPresentations:
        temp = '{}/{} - {}\n'.format(
            date[0].month, date[0].day, date[1]
        )
        responseText = responseText + temp
    await ctx.send(responseText)

@bot.command(name='nextPresentation', help='Gets the next schedules presentation topic/presenter')
async def getNext(ctx):
    responseText = ''
    current = datetime.datetime.now()
    for date in formattedPresentations:
        if current < date[0]:
            responseText = '{}/{} - {}'.format(
                date[0].month, date[0].day, date[1]
            )
            break
        else:
            responseText = "There's no more scheduled presentations!"
    await ctx.send(responseText)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

print('Attempting to log in the bot...')
try:
    bot.run(TOKEN)
except errors.LoginFailure:
    print('The bot could not log in, check the token!')