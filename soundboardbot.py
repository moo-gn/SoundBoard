import discord
from discord.ext import commands
import yt_dlp
from search_yt import search
import json
from board import Board
import os

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.queue = []
    self.play_status = False
    self.cmnds1 = ['Board, B, SoundBoard: sends the sound board if user in voice channel', 'Add: saves attachment or searches for argument in youtube ', 'Leave, Stop: leaves the voice channel',  'Remove, D, Delete: removes a button by its name', 'Rename, R: renames the button']

      
#leaves the voice channel
  @commands.command(aliases = ['stop'])
  async def leave(self,ctx):
    await ctx.voice_client.disconnect() 
      
#saves attachment or searches for argument in youtube
  @commands.command(aliases = ['a'])
  async def add(self,ctx,*,arg = None):
      if ctx.message.attachments:
        url2 = ctx.message.attachments[0].url
      else:
        fetch = search(arg)
        with yt_dlp.YoutubeDL({'format':'bestaudio', 'outtmpl': 'file1.mp3'}) as ydl:
          info = ydl.extract_info(fetch[0], download=True)
        os.system('ffmpeg -i "file1.mp3" -to 00:00:05 file.mp3')
        msg = await ctx.send(file = discord.File('file.mp3'))
        url2 = msg.attachments[0].url
        os.remove('file.mp3')
        os.remove('file1.mp3')
      msgb = await ctx.reply('reply with the button name')
      msg = await  self.client.wait_for('message', check = lambda i : i.reference.message_id == msgb.id)

      with open('board.txt') as file:
        data = json.load(file)
      if len(data) < 25:
        data[msg.content.lower()] = url2
      else:
        await msgb.edit('Maximum size exceeded')
      with open('board.txt', 'w') as file:
        json.dump(data, file)
      await msgb.edit('added')

#sends the sound board if user in voice channel
  @commands.command(aliases = ['board', 'soundboard', 'join'])
  async def b(self,ctx):
    if ctx.author.voice is None:
      await ctx.send('Please join a voice channel!')
      return
    vc = ctx.author.voice.channel
    if ctx.voice_client is None:
      await vc.connect()
    else:
      await ctx.voice_client.move_to(vc)  
    await ctx.send(content='PLAY',view= Board())

#removes a button by its name
  @commands.command(aliases=['d', 'delete'])
  async def remove(self,ctx,*,message):
    with open('board.txt') as file:
        data = json.load(file)
    try:     
      del data[message.lower()]
      with open('board.txt', 'w') as file:
        json.dump(data, file)
      await ctx.reply("its been done")
    except KeyError: 
      await ctx.reply("its not here")

#rename button
  @commands.command(aliases=['r'])
  async def rename(self,ctx,arg1, arg2):
    with open('board.txt') as file:
          data = json.load(file)
    try:
      if len(data) < 25:
        url2 = data[arg1.lower()]
        del data[arg1.lower()]
        data[arg2.lower()] = url2
      else:
        await ctx.reply('Maximum size exceeded')
      with open('board.txt', 'w') as file:
        json.dump(data, file)
      await ctx.reply("its been done")
    except KeyError: 
      await ctx.reply("its not here")

    

#send an embed with the commands
  @commands.command(aliases = ['h'])
  async def help(self, ctx):
    embed = discord.Embed(title= 'List of Commands!')
    for item in self.cmnds1:
        embed.add_field(name = item.split(':')[0], value = item.split(':')[1], inline=False)
    await ctx.send(embed= embed)

  def setup(client):
    client.add_cog(music(client))