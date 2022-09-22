import discord
import json
import math

class buttons(discord.ui.Button):
    def __init__(self, key,aud,row):
        super().__init__(label=key, style=discord.ButtonStyle.blurple, row = row)
        self.aud = aud

    async def callback(self, interaction: discord.Interaction):
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-t 5 -vn'}
            source = await discord.FFmpegOpusAudio.from_probe(self.aud, **FFMPEG_OPTIONS)
            interaction.user.guild.voice_client.stop()
            interaction.user.guild.voice_client.play(source)
            
            await interaction.response.edit_message(content='PLAY',view = Board())
            



class Board(discord.ui.View):
 
    def __init__(self):
        super().__init__(timeout=None)
        with open('board.json') as file:
            data = json.load(file)
        m = len(data) 
        x = 0
        y = 0
        rowmax = math.ceil(math.sqrt(m))
        for key in data:
            x+=1
            self.add_item(buttons(key, data[key], y))
            if (x % rowmax) == 0:
                y += 1
        
        

            