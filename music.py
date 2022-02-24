import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    self.isPlaying = False
    self.queue = []
    self.YDL_OPTIONS: {'format': 'bestaudio', 'noplaylist': 'True'}
    self.FFMPEG_OPTIONS: {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    self.vc = ''

  def search(self, item):
    with YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
      try:
        info = ydl.extract_info('ytsearch:%s' % item, download = False)['entries'][0]
      except Exception:
        return False

    return {'source': info['formats'][0]['url'], 'title': info['title']}

  def playNext(self):
    if len(self.queue) > 0:
      self.isPlaying = True

      url = self.queue[0][0]['source']
      self.queue.pop(0)

      self.vc.play(discord.FFmpegPCMAudio(url, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}), after = lambda x: self.playNext())
    else:
      self.isPlaying = False

  async def playMusic(self):
    if len(self.queue) > 0:
      self.isPlaying = True

      url = self.queue[0][0]['source']

      if self.vc == '' or not self.vc.is_connected():
        self.vc = await self.queue[0][1].connect()
      else:
        self.vc = await self.bot.move_to(self.queue[0][1])

      self.queue.pop(0)

      self.vc.play(discord.FFmpegPCMAudio(url, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}), after = lambda x: self.playNext())
    else:
      self.isPlaying = False

  @commands.command()
  async def p(self, ctx, *args):
    query = ' '.join(args)

    vc = ctx.author.voice.channel
    if vc is None:
      await ctx.send("You are not connected to a voice channel!")
    else:
      song = self.search(query)
      if type(song) == bool:
        await ctx.send("Can't play playlists or livestreams! Try another keyword.")
      else:
        if self.isPlaying == True:
          await ctx.send(song['title'] + " added to the queue.")
        else:
          await ctx.send("Now Playing " + song['title'])
        
        self.queue.append([song, vc])

        if self.isPlaying == False:
          await self.playMusic()

  @commands.command()
  async def q(self, ctx):
    theQueue = ''
    for i in range(len(self.queue)):
      theQueue += '* ' + self.queue[i][0]['title'] + '\n'

    if theQueue != '':
      await ctx.send(theQueue)
    else:
      await ctx.send("There is nothing in the queue")

  @commands.command()
  async def s(self, ctx):
    if self.vc != '':
      if len(self.queue) > 0:
        await ctx.send("Skipped! Now Playing " + self.queue[0][0]['title'])
      else:
        await ctx.send("Skipped!")
      self.vc.stop()
      await self.playMusic()
    else:
      await ctx.send('You are not connected to a voice channel!')

  @commands.command()
  async def l(self, ctx):
    await ctx.voice_client.disconnect()
    await ctx.send('Byee!')

  @commands.command()
  async def pause(self, ctx):
    if self.isPlaying == True:
      self.isPlaying == False
      await ctx.send('Paused ⏸')
      await ctx.voice_client.pause()
    else:
      await ctx.send('The song is already paused.')

  @commands.command()
  async def resume(self, ctx):
    if len(self.queue) > 0 or self.isPlaying == False:
      self.isPlaying == True
      await ctx.send('Playing...')
      await ctx.voice_client.resume()
    else:
      await ctx.send('Nothing to resume.')

  @commands.command()
  async def stop(self, ctx):
    if self.isPlaying == True:
      self.queue = []
      await ctx.send('Stopped ⏹')
      await ctx.voice_client.stop()
    else:
      await ctx.send('The song is already stopped.')

  @commands.command()
  async def h(self, ctx):
    await ctx.send("Hi! Let me show you what I can do 😁 \n -------------------------------- \n  p (song)     - Plays any song from youtube! \n  s                   - Skips the song. \n  pause          - Pauses the song. \n  resume       - Resumes the song. \n  stop             - Stops the song. \n  q                   - Shows the songs in the queue. \n  l                    - If you don't need me anymore 😔")