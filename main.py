import discord
from discord.ext import commands
import os
from stayOn import stayOn
from music import music

# client = discord.Client()

# @client.event
# async def on_ready():
#   print("Logged on as {}".format(client.user))

# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return

#   if message.content == 'hi':
#     await message.channel.send('Hello!')

Bot = commands.Bot(command_prefix = '$')
Bot.add_cog(music(Bot))

stayOn()
Bot.run(os.environ['token'])
# client.run(os.environ['token'])