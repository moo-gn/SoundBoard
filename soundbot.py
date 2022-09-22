import discord
from discord.ext import commands
import soundboardbot

import sys
sys.path.append("..")
import credentials

cogs = [soundboardbot.music]
client = commands.Bot(command_prefix='!', intents = discord.Intents.all(), case_insensitive = True, help_command=None)

TOKEN = credentials.Soundboard

for i in range(len(cogs)):
  cogs[i].setup(client)

#disconnect if no user is connected
@client.event
async def on_voice_state_update(member, before, after):
  if before.channel and not after.channel and not member.bot:
    x = member.guild.voice_client
    for y in x.channel.members:
      if not y.bot:
        return
    await x.disconnect()

    

client.run(TOKEN)
