"""Made by: Austin Ares, Fabian Kuzbiel"""


import discord, time, os, shutil, youtube_dl, youtubesearchpython, json, datetime, requests, random, multiprocessing

from discord.ext import commands, tasks
from discord.utils import get
from discord import Spotify


TOKEN = "TOKEN_IS_NOT_PUBLIC"

"""Location Variables"""

global file_path, music_location, ydl_opts, words, res_location, config_location, playlist_location, metadata_location

file_path = os.path.dirname(os.path.realpath(__file__))

vorbis_img = "https://cdn.discordapp.com/attachments/800136030228316170/802961405296902154/icon2.jpg"

intents = discord.Intents.all()
intents.members = True
intents.guilds = True

music_location = file_path+"\\Music"
queue_location = file_path+"\\Queue"
temp_location = file_path+"\\Temp"
res_location = file_path+"\\Resources"
config_location = file_path+"\\Config"
playlist_location = file_path+"\\Playlists"
metadata_location = file_path+"\\Metadata"
user_location = file_path+"\\Members"
cog_location = file_path+"\\Cogs"
guild_location = file_path+"\\Guilds"

words = ["\\", "/", ":", "<", ">", "*", "?", '"', "|", "."]

ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '256',

        }],

    }

def make_asset(file : os.PathLike, mode : str, data : dict, indention : int):

    with open(file, mode) as make_json:
        json.dump(data, make_json, indent=indention)
        make_json.close()

def filt_str(string : str):

    filtered_1 = ''.join(filter(lambda char: char != '"', string))
    filtered_2 = ''.join(filter(lambda char: char != ':', filtered_1))
    filtered_3 = ''.join(filter(lambda char: char != '|', filtered_2))
    filtered_4 = ''.join(filter(lambda char: char != '.', filtered_3))
    filtered_5 = ''.join(filter(lambda char: char != ']', filtered_4))
    filtered_6 = ''.join(filter(lambda char: char != '[', filtered_5))
    filtered_7 = ''.join(filter(lambda char: char != "'", filtered_6))

    return filtered_7

def clear_temp():
    try:
        os.chdir(temp_location)

        for y in range(len(os.listdir())):
            os.remove(os.listdir()[0])
    
        os.chdir(music_location)

        for z in range(len(os.listdir())):
            os.remove(os.listdir()[0])

        os.chdir(file_path)

    except PermissionError:
        pass
clear_temp()
"""Functions"""

def return_data(file : str, tabel : str, sub_tabel : str):

    with open(f"{file}") as data:

        RwText_Data = data.read()
        RwJSON_Data = json.loads(RwText_Data)

        return RwJSON_Data[tabel][sub_tabel]

CLIENT_PREFIX = return_data(file=config_location+"\\prefix.json", tabel="pfx", sub_tabel="setting1")
client = commands.AutoShardedBot(shard_count=3, command_prefix=CLIENT_PREFIX, case_insenstive=True, guild_subscriptions=True, intents=intents)

"""Embed Colours"""

WHITE = discord.Color.from_rgb(255, 255, 255)
TERQ = discord.Color.from_rgb(49,171,159)
RED = discord.Color.from_rgb(255, 0, 0)
YELLOW = discord.Color.from_rgb(255, 255, 0)
LIGHT_BLUE = discord.Color.from_rgb(155, 155, 255)
MEDIUM_PURPLE = discord.Color.from_rgb(147, 112, 219)
"""Bot Code"""

@client.remove_command("help")
@client.event
async def on_ready():
    print("Online!")
    
    main_channel = client.get_channel(781983211710316575)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f'{CLIENT_PREFIX}help'))
    

@client.command(aliases=['help', 'h', 'a'])
async def assist(ctx):
    
    
    """Help Command"""

    embed = discord.Embed(
        color = TERQ
    )

    embed.set_author(name=f"Commands")
    
    embed.add_field(name=f"{CLIENT_PREFIX}assist ● ", value="This Command")
    embed.add_field(name=f"{CLIENT_PREFIX}purge ● ", value="Clears A Channel")
    embed.add_field(name=f"{CLIENT_PREFIX}pause ● ", value="Pauses Currently Playing Song")
    embed.add_field(name=f"{CLIENT_PREFIX}resume ● ", value="Resumes Currently Playing Song")
    embed.add_field(name=f"{CLIENT_PREFIX}play ● ", value="Plays Selected Song")
    embed.add_field(name=f"{CLIENT_PREFIX}songs ● ", value="Lists all Songs in Queue")
    embed.add_field(name=f"{CLIENT_PREFIX}clear ● ", value="Clears all Songs from Queue")
    embed.add_field(name=f"{CLIENT_PREFIX}queueplaylist ● ", value="Queues a playlist")
    embed.add_field(name=f"{CLIENT_PREFIX}playlist ● ", value="Makes a playlist")
    embed.add_field(name=f"{CLIENT_PREFIX}playlists ● ", value="Shows a playlists contents")
    embed.add_field(name=f"{CLIENT_PREFIX}playq ● ", value="Plays the first song in the queue")
    embed.add_field(name=f"{CLIENT_PREFIX}deleteplaylist ● ", value="Deletes a playlist")
    embed.add_field(name=f"{CLIENT_PREFIX}usage ● ", value="Shows Usage of All Commands")
    embed.add_field(name=f"{CLIENT_PREFIX}queue ● ", value="Queues song(s)")
    embed.add_field(name=f"{CLIENT_PREFIX}join ● ", value="Joins channel User is currently in")
    embed.add_field(name=f"{CLIENT_PREFIX}disconnect ● ", value="disconnects from channel User is currently in")
    embed.add_field(name=f"{CLIENT_PREFIX}volume ● ", value="Sets volume of Bot")
    embed.add_field(name=f"{CLIENT_PREFIX}song ● ", value="Shows Current song (If one is playing)")
    embed.add_field(name=f"{CLIENT_PREFIX}profile ● ", value="Shows infomation about specified user")
    
    

    embed.set_thumbnail(url=vorbis_img)
    curnt_time = str(datetime.datetime.now())
    embed.set_footer(text=curnt_time.split(".")[0])

    await ctx.send(embed=embed)

@client.command(aliases=['pu'])
async def purge(ctx, amt : int):
    if amt > 249:
        return await ctx.send("You cannot delete more than 250 messages at a time") 
    amt = amt+1

    await ctx.channel.purge(limit=amt)
    await ctx.send(f"Purged {ctx.channel} by {amt} messages")

    time.sleep(3)
    await ctx.channel.purge(limit=1)

@client.command(aliases=['pl'])
async def play(ctx, *, url : str):

    multiple_songs = url.split(',')
    max_length = 3
    guild = f"\\{ctx.message.guild.id}"

    full_path = music_location+guild
    queue_full_path = queue_location+guild
    meta_full_path = metadata_location+guild
    config_full_path = config_location+guild
    server = client.get_guild(ctx.message.guild.id)
    embed = discord.Embed(
        colour = LIGHT_BLUE
    )

    print(multiple_songs)

    if multiple_songs[0].startswith("<@!"):
        
        i = multiple_songs[0].split('!')
        i = i[1].split('>')[0]
        
        user = server.get_member(int(i))
        print(user.activities)
        
        for activity in user.activities:
            if isinstance(activity, Spotify):
                url = str(activity.title)
            else:
                embed.color = RED
                embed.set_author(name="User is not playing any song!")

                return await ctx.send(embed=embed)

            
                

    os.chdir(full_path)

    

    voice = get(client.voice_clients, guild=ctx.guild)
    url = youtubesearchpython.SearchVideos(url, offset=1, mode='dict', max_results=1)
    
    if voice and voice.is_playing():
        
        embed.color = RED
        embed.set_author(name="Already Playing, (If there is no audio, it's because it's paused)")

        return await ctx.send(embed=embed)
    client_volume = return_data(config_full_path+"\\volume.json", "volume", "vol")

    if voice and voice.is_connected():
        pass
    else:
        try:

            channel = ctx.message.author.voice.channel
            await channel.connect()

        except AttributeError:
            embed.color = RED
            embed.set_author(name="You're not connected to A Voice Channel")

            return await ctx.send(embed=embed)

    try:
        voice = get(client.voice_clients, guild=ctx.guild)
        video = str(url.links[0])
        views = str(url.views[0])
        title = str(url.titles[0])
        length = str(url.durations[0])
        channel = str(url.channels[0])
    except IndexError:
        embed.color = RED
        embed.set_author(name="I have found no song with that name on YouTube")

        return await ctx.send(embed=embed)
    with open(meta_full_path+f"\\metadata.json", "w+") as write_data:

        metadata = {}

        metadata['metadata'] = ({
            "name": title,
            "views": views,
            "author": ctx.author.name
        })

        json.dump(metadata, write_data, indent=4)

    if int(len(length.split(':')[0])) >= 2 and int(len(length.split(':'))) >= 3:
        
        embed.color = RED
        embed.set_author(name=f"Cannot Download Song, Song is {length.split(':')[0]} hours! Limit is 2 hours!")
        
        return await ctx.send(embed=embed)

    embed.set_author(name=f'Playing "{title}"')
    embed.add_field(name=f"Views ● ",value=views)
    embed.add_field(name=f"Link ● ",value=video, inline=False)
    embed.add_field(name=f"Length ● ",value=length, inline=False)
    embed.add_field(name=f"Channel ● ",value=channel, inline=False)
    embed.set_footer(text=f"Client Volume ● {int(client_volume)}")

    await ctx.send(embed=embed)
    
    def check_queue():
        
        music_file = full_path+"\\music.wav"
        file_to_move = queue_full_path+f"\\music.wav"
        

        os.chdir(queue_full_path)
    
        if len(os.listdir()) <= 0:
            print("No more queued songs.")
            if os.path.isfile(music_file):
                os.remove(music_file)
        else:
            next_song = queue_full_path+f"\\{os.listdir(queue_full_path)[0]}"
            if os.path.isfile(music_file):
                os.remove(music_file)

            next_song_nfext = os.listdir(queue_full_path)[0].split(".wav")
            default_filename = youtubesearchpython.SearchVideos(keyword=next_song_nfext, offset=1, mode="dict", max_results=1)

            print(next_song_nfext)

            name = str(default_filename.titles[0])
            view = str(default_filename.views[0])
            channels = str(default_filename.channels[0])
            
            with open(meta_full_path+"\\metadata.json", 'w+') as write_metadata:
                
                video_metadata = {}

                video_metadata['metadata'] = ({
                    "name": next_song_nfext[0],
                    "views": view,
                    "author": ctx.author.name
                })

                json.dump(video_metadata, write_metadata, indent=4)
            
            try:
                os.rename(next_song, "music.wav")
            except FileExistsError:
                os.remove("music.wav")
                os.rename(next_song, "music.wav")

            shutil.move(file_to_move, full_path)

            if voice and voice.is_playing() and voice.is_paused():
                voice.stop()
            
            voice.play(discord.FFmpegPCMAudio(music_file), after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = client_volume

    if os.path.isfile(full_path+f"\\music.wav"):
        
        voice = get(client.voice_clients, guild=ctx.guild)

        voice.stop()

        os.remove("music.wav")
    else:
        pass

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video])

        os.rename(os.listdir()[0], "music.wav")

        if voice and voice.is_playing() or voice.is_paused():
            voice.stop()
        
        voice.play(discord.FFmpegPCMAudio(full_path+"\\music.wav"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = client_volume

@client.command(aliases=['qpl'])
async def queueplaylist(ctx, *, playlist):

    clear_temp()

    embed = discord.Embed(color=LIGHT_BLUE)
    ctx_author = ctx.author.name+"#"+ctx.author.discriminator   
    url = None
    guild = f"\\{ctx.message.guild.id}"

    full_temp_path = temp_location+guild
    full_queue_path = queue_location+guild
    
    os.chdir(full_temp_path)

    if os.path.isdir(playlist_location+f"\\{playlist}"):
        pass
    else:
        embed.color = RED
        embed.set_author(name=f'"{playlist}" is not a playlist!')

        return await ctx.send(embed=embed)
    
    with open(playlist_location+f"\\{playlist}\\{playlist}.json") as queued_playlist:

        text = queued_playlist.read()
        json_text = json.loads(text)

        json_text_file = json_text['info']
        json_meta = json_text['metadata']

        privacy_setting = json_text_file['privicy']
        author = json_meta['playlist-author']
        songs = json_text_file['playlist'].split(',')

        if privacy_setting == "public" or ctx.author.id == author:

            embed.set_author(name=f'Queued the Playlist ● "{playlist}"')

            await ctx.send(embed=embed)

            for x in range(len(songs)):

                if len(os.listdir(full_queue_path)) > 14:
                    embed.color = RED
                    embed.set_author(name="Queue is at song limit! (Limit is 15)")

                    return await ctx.send(embed=embed)

                url = youtubesearchpython.SearchVideos(songs[x], offset=1, mode='dict', max_results=1)

                link = str(url.links[0])
                title = str(url.titles[0])
                channel = str(url.channels[0])
                length = str(url.durations[0])

                len_split = length.split(":")

                if int(len(len_split)) >= 3 and int(len_split[0]) >= 1:

                    embed.color = RED
                    embed.set_author(name=f"Song / Video is too long! Limit is 1 hour! (Song is {int(len_split[0])})")

                    return await ctx.send(embed=embed)

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:

                    filtered = filt_str(title)
                
                    ydl.download([link])

                    os.rename(os.listdir()[0], filtered+".wav")
                    shutil.move(os.listdir()[0], full_queue_path)


                    
        else:
            embed.color = RED
            embed.set_author(name="This playlist is private!")

            return await ctx.send(embed=embed)

            

@client.command(pass_context=True, aliases=['j'])
async def join(ctx):

    embed = discord.Embed(
        color = discord.Color.from_rgb(255, 255, 255)
    )
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await voice.move_to(channel)
    else:
        embed.set_author(name=f"Connected to {channel}")
        await ctx.send(embed=embed)
        voice = await channel.connect()

@client.command(aliases=['p'])
async def pause(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice != None:
        if voice.is_playing():
            embed.set_author(name="Paused!")
            voice.pause()
        else:
            embed.set_author(name="I am already paused!")
    else:
        embed.set_author(name="I am not connected to a Voice Channel!")

    await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=['d'])
async def disconnect(ctx):

    """Sets Up Embed and Voice Variable"""

    embed = discord.Embed(
        color = discord.Color.from_rgb(255, 255, 255)
    )
    try:
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)
    except AttributeError:
        return
    """If Bot is in Voice Channel is Connect, it disconnects"""

    if voice and voice.is_connected():

        embed.set_author(name=f"Disconnected from {channel}")
        await ctx.send(embed=embed)
        await voice.disconnect(force=False)
        
    else:
        """If bot is already disconnected from the voice channel, it sends the following message"""
        embed.set_author(name="I am not in any Voice Channel!")
        embed.color = RED
        await ctx.send(embed=embed)
    
@client.command(pass_context=True, aliases=['q'])
async def queue(ctx, *, url):

    guild = f"\\{ctx.message.guild.id}"
    full_queue_path = queue_location+guild
    full_temp_path = temp_location+guild

    clear_temp()

    multiple_songs = url.split(',')

    if len(multiple_songs) > 1:
        await ctx.send(f"Downloading {len(multiple_songs)} song(s)")
    
    
    for x in range(len(multiple_songs)):
        
        url = multiple_songs[x]
        
        """Queue Command"""
        
        embed = discord.Embed(
            colour = YELLOW
        )

        if len(os.listdir(full_queue_path)) > 14:

            embed.set_author(name="Queue has reached limit in songs, limit is 15 songs!")
            embed.color = RED

            return await ctx.send(embed=embed)
    
        """YouTube API"""
        
        
        queued_song = youtubesearchpython.SearchVideos(url, offset=1, mode='dict', max_results=1)

        """Splits YouTube Search API into Variables"""
        
        video = str(queued_song.links[0])
        views = str(queued_song.views[0])
        thumbnail = queued_song.thumbnails[0]
        title = str(queued_song.titles[0])
        lenght = str(queued_song.durations[0])
        channel = str(queued_song.channels[0])

        if os.path.isfile(f"{queue_location}\\{ctx.message.guild.id}\\{title}.wav"):

            embed.color = RED
            embed.set_author(name="This song is already queued!")

            return await ctx.send(embed=embed)
        else:
            print("Song is not already queued, continuing..")


        """Checks if the song is below 1 Hour"""

        if int(len(lenght.split(':')[0])) >= 1 and int(len(lenght.split(':'))) >= 3:
        

            embed.color = RED
            embed.set_author(name=f"Cannot Download Song, Song is too long > {lenght} > Limit is 1 hour!")
        

            return await ctx.send(embed=embed)

        """Sets up the Embed"""
        if len(multiple_songs) == 1:
            embed.set_author(name=f'Queueing "{title}"')
            embed.set_image(url=thumbnail[0])
            embed.add_field(name="Title > ", value=title)
            embed.add_field(name="Views > ", value=views, inline=False)
            embed.add_field(name="Channel > ", value=channel, inline=False)
            embed.add_field(name="Link > ", value=video, inline=False)
            embed.add_field(name="Song Downloaded > ", value=x+1)
        else:
            embed.color = LIGHT_BLUE
            embed.set_author(name=f"Queueing ● {title} ● {channel}")
            

        await ctx.send(embed=embed)

        """Uses YouTube_DL to download the URL Parameter"""

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
            
                os.chdir(full_temp_path)
                ydl.download([video])

                filtered = filt_str(title)

                """Sets up download variables"""

                temp_song_location = full_temp_path+f"\\temp.wav"
                queued_name = filtered+".wav"
                temp_song = os.listdir()[0]

                """Moves and renames downloaded file to the queue"""

                os.rename(temp_song, queued_name)
                shutil.move(temp_song_location, full_queue_path)
                await ctx.send(embed=embed)

            except OSError:

                """If the download file contains illigal file name letters, this Exception Filters them."""

                os.chdir(full_temp_path)
            
                try:
                    file_dest = os.listdir()[0]
                    
                    if file_dest.endswith(".wav"):
                    
                        """Gets the illigal file"""

                        filtered_name = title.split()
                        filtered_str = filt_str(title)
                        final_file_name = filtered_str+".wav"
                    
                        """Renames and moves to the queue folder"""

                        os.rename(file_dest, final_file_name)
                        shutil.move(full_temp_path+"\\"+os.listdir()[0], full_queue_path)
                    
                        
                        embed.set_author(name=f'Queued "{title}"')

                        if len(multiple_songs) == 1:
                            embed.color = LIGHT_BLUE
                            await ctx.send(embed=embed)

                        """Writes JSON Data"""
                    else:
                        raise FileNotFoundError("Music File Not Found")

                except (OSError, FileNotFoundError) as errno:
                    embed.color = RED

                    """Error Handler"""

                    embed.set_author(name=errno)

                    await ctx.send(embed=embed)

                    os.remove(os.listdir()[0])
        

@client.command(aliases=['s'])
async def skip(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)
    

    embed.set_author(name="Skipping Current Song")

    await ctx.send(embed=embed)

    if voice and voice.is_playing():
        print("Skipping")

        voice.pause()
        voice.stop()
    else:
        print("Skipping..")

        voice.pause()
        voice.stop()
        

@client.command(aliases=['v'])
async def volume(ctx, volume_float : float):
    guild = f"\\{ctx.message.guild.id}"
    full_config_path = config_location+guild

    embed = discord.Embed(colour=LIGHT_BLUE)
    with open(full_config_path+"\\volume.json", "w") as vol:

        New_vol = {}
        New_vol['volume'] = ({
            "vol": volume_float
        })

        json.dump(New_vol, vol, indent=4)

    embed.set_author(name=f"Changed volume to > {volume_float}")

    await ctx.send(embed=embed)

@client.command(aliases=['unpause', 'u'])
async def resume(ctx):
    embed = discord.Embed(color=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice != None:

        if voice and voice.is_playing():
            embed.set_author(name="Already Playing!")
        else:
            embed.set_author(name="Resumed!")

            voice.resume()
    else:
        embed.set_author(name="I am not connected to a Voice Channel!")

    await ctx.send(embed=embed)

@client.command(aliases=['sn'])
async def songs(ctx):

    os.chdir(queue_location+f"\\{ctx.message.guild.id}")
    embed = discord.Embed(color=LIGHT_BLUE)
    

    if len(os.listdir()) == 0:
        embed.set_author(name="No Songs")
        return await ctx.send(embed=embed)
    else:
        for x in range(len(os.listdir())):
            y = os.listdir()[x].split('.wav')
            embed.set_author(name=y[0])
            await ctx.send(embed=embed)
    
    

@client.command(aliases=['c'])
async def clear(ctx):

    os.chdir(queue_location+f"\\{ctx.message.guild.id}")
    embed = discord.Embed(color=TERQ)

    for x in range(len(os.listdir())):
        os.remove(os.listdir()[0])

    embed.set_author(name="Cleared Song Queue")

    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def stop(ctx):
    embed = discord.Embed(color=RED)

    embed.set_author(name="Shutting Down")

    await ctx.send(embed=embed)

    await client.close()

@client.command()
async def playlist(ctx, *, args : str):

    arguments = args.split(". ")

    os.chdir(playlist_location)

    global song_len, final_len, song_list

    id_letters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', '_', '-', '!']
    song_list = []
    song_len = []
    final_len = 0


    playlist_name = arguments[0]
    mode = arguments[1]
    url = arguments[2]

    playlist_id = random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)
    mod_url = url.split(", ")

    for y in range(len(os.listdir())):
        with open(playlist_location+"\\"+os.listdir()[y]+"\\"+os.listdir()[y]+".json") as check_id:

            text = check_id.read()
            json_text = json.loads(text)

            check_plyst_id = json_text['metadata']['playlist-id']

            if playlist_id == check_plyst_id:
                playlist_id = random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)
                check_id.close()
            else:
                pass
        break

    for x in range(len(mod_url)):
        convt_url = youtubesearchpython.SearchVideos(keyword=mod_url[x], offset=1, mode="dict", max_results=1)

        thumbnail = convt_url.thumbnails[0]
        title = convt_url.titles[0]
        length = int(convt_url.durations[0].split(':')[0])

        song_len.append(length)
        song_list.append(title)

        final_len = final_len+song_len[x]
    
    final_songs = filt_str(str(song_list))

    print(mod_url)
    
    conv_url_ = youtubesearchpython.SearchVideos(keyword=random.choice(mod_url), offset=1, mode="dict", max_results=1)

    thumbnail = conv_url_.thumbnails[0]

    print(thumbnail)    

    embed = discord.Embed(color=LIGHT_BLUE)
    playlist_ = playlist_location+f"\\{playlist_name}"
    full_author = ctx.author.name+"#"+ctx.author.discriminator

    if mode == "public" or mode == "private":

        pass
    else:
        embed.color = RED
        embed.set_author(name=f'"{mode}"is not a privicy mode! Chose either: private / public')
        return await ctx.send(embed=embed)

    os.chdir(playlist_location)

    if os.path.isdir(playlist_):

        embed.color = RED
        embed.set_author(name="A Playlist with that name already exists!")

        return await ctx.send(embed=embed)

    else:
        os.mkdir(playlist_)
    
        with open(playlist_+f"\\{playlist_name}.json", "w+") as new_playlist:

            playlist_info = {}
            

            playlist_info['info'] = ({
                "playlist": final_songs,
                "privicy": mode
            })

            playlist_info['metadata'] = ({
                "playlist-author": ctx.author.id,
                "playlist-cover": thumbnail[1],
                "playlist-length": final_len,
                "playlist-id": playlist_id,
                "playlist-author-name": ctx.author.name

            })

            

            json.dump(playlist_info, new_playlist, indent=4)
            

            embed.set_author(name=f'Made new Playlist ● "{playlist_name}"')
            embed.add_field(name="Author ● ", value=full_author, inline=False)
            embed.add_field(name="Songs ● ", value=final_songs, inline=False)
            embed.add_field(name="Privacy Setting ● ", value=mode)

            embed.set_image(url=thumbnail[1])
            embed.set_thumbnail(url=vorbis_img)

            await ctx.send(embed=embed)

        
@client.command()
async def playlists(ctx, *, playlist):

    playlist_ = playlist_location+f"\\{playlist}\\"
    embed = discord.Embed(color=LIGHT_BLUE)

    print(playlist_+f"{playlist}.json")
    if os.path.isfile(playlist_+f"{playlist}.json") == True:
        
        with open(playlist_+f"{playlist}.json") as read_playlist:

            text = read_playlist.read()
            json_data = json.loads(text)
            playlist_json = json_data['info']
            playlist_metadata = json_data['metadata']
            full_author = ctx.author.name+"#"+ctx.author.discriminator
                
            if playlist_json["privicy"] == "public" or playlist_metadata["playlist-author"] == ctx.author.id:
                
                embed.set_author(name=f'Here is the playlist "{playlist}"')
                embed.set_image(url=playlist_metadata['playlist-cover'])

                embed.add_field(name=f"Author of Playlist > ", value=playlist_metadata['playlist-author-name'])
                embed.add_field(name="Songs > ", value=playlist_json['playlist'], inline=False)
                embed.add_field(name="Length of Playlist (Minutes) > ", value=playlist_metadata['playlist-length'], inline=False)

                

            else:
                embed.color = RED
                embed.set_author(name="This Playlist is Private!")

            await ctx.send(embed=embed)
    else:
        embed.color = RED
        embed.set_author(name="The playlist you're looking for does not exist!")
        await ctx.send(embed=embed)

@client.command()
async def playq(ctx):

    clear_temp()

    embed = discord.Embed(color=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel
    guild = f"\\{ctx.message.guild.id}"

    if voice == None:

        embed.color = RED
        embed.set_author(name="I'm not connected to a Voice Channel.")

        return await ctx.send(embed=embed)

    if voice.is_playing() or voice.is_paused():

        embed.color = RED
        embed.set_author(name="I am already playing music! (If no music is playing, it's because it's paused)")

        return await ctx.send(embed=embed)

    os.chdir(queue_location+guild)

    def check_queue():

        os.chdir(queue_location+guild)

        music_file = music_location+guild+"\\music.wav"
        file_to_move = queue_location+guild+f"\\music.wav"

        if len(os.listdir()) <= 0:
            print("No more queued songs.")
            if os.path.isfile(music_file):
                os.remove(music_file)
        else:
            next_song = queue_location+guild+f"\\{os.listdir()[0]}"
            if os.path.isfile(music_file):
                os.remove(music_file)
            
            try:           
                next_song_nfext = os.listdir(queue_location+guild)[0].split(".")
                default_filename = youtubesearchpython.SearchVideos(keyword=next_song_nfext, offset=1, mode="dict", max_results=1)
                view = str(default_filename.views[0])
            except IndexError:
                view = "No Views"

            with open(metadata_location+guild+"\\metadata.json", 'w+') as write_metadata:
                
                video_metadata = {}

                video_metadata['metadata'] = ({
                    "name": next_song_nfext[0],
                    "views": view,
                    "author": ctx.author.name
                })

                json.dump(video_metadata, write_metadata, indent=4)
            
            try:
                os.rename(next_song, "music.wav")
                shutil.move(file_to_move, music_location)
            except shutil.Error:
                if voice.is_playing():
                    voice.stop()
                os.remove(music_location+guild+"\\music.wav")

            
            voice.play(discord.FFmpegPCMAudio(music_file), after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = return_data(config_location+"\\volume.json", "volume", "vol")

    if voice and voice.is_connected():
        pass
    else:
        await channel.connect()
        
    if len(os.listdir()) > 0:

        os.chdir(queue_location+guild)

        next_song_nfext = os.listdir()[0].split(".wav")
        default_filename = youtubesearchpython.SearchVideos(keyword=next_song_nfext, offset=1, mode="dict", max_results=1)
        view = str(default_filename.views[0])
    
        with open(metadata_location+guild+"\\metadata.json", 'w+') as write_metadata:
                
            video_metadata = {}

            video_metadata['metadata'] = ({
                "name": next_song_nfext[0],
                "views": view,
                "author": ctx.author.name
            })

            json.dump(video_metadata, write_metadata, indent=4)

        os.rename(os.listdir()[0], "music.wav")

        if os.path.isfile(music_location+guild+"\\music.wav"):
            os.remove(music_location+guild+"\\music.wav")

        shutil.move(queue_location+guild+f"\\music.wav", music_location+guild)
        
        voice.play(discord.FFmpegPCMAudio(music_location+guild+f"\\music.wav"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = return_data(config_location+guild+"\\volume.json", "volume", "vol")
    
    else:
        embed.set_author(name="No songs in queue")

        await ctx.send(embed=embed)

@client.command()
async def deleteplaylist(ctx, *, playlist):

    embed = discord.Embed(color=LIGHT_BLUE)
    user = ctx.author.name+"#"+ctx.author.discriminator

    async def delete():
        
        os.remove(playlist_location+f"\\{playlist}\\{playlist}.json")
        os.rmdir(playlist_location+f"\\{playlist}")

        embed.set_author(name=f'Deleted Playlist: "{playlist}"')

        return await ctx.send(embed=embed)


    with open(playlist_location+f"\\{playlist}\\{playlist}.json") as delete_playlist:

        text = delete_playlist.read()
        json_text = json.loads(text)

        json_text_form = json_text['info']
        json_metadata_form = json_text['metadata']

        author = json_metadata_form['playlist-author']
        
        delete_playlist.close()
        
        if ctx.author.id == author:

            await delete()

        else:
            embed.color = RED
            embed.set_author(name="You're not the owner of this playlist!")

            return await ctx.send(embed=embed)

@client.command()
async def usage(ctx):

    embed = discord.Embed(color=TERQ)

    embed.set_author(name="Command Usage")

    embed.add_field(name=f"{CLIENT_PREFIX}help > ", value=f"{CLIENT_PREFIX}help")
    embed.add_field(name=f"{CLIENT_PREFIX}purge > ", value=f"{CLIENT_PREFIX}purge <Amount of Messages>")
    embed.add_field(name=f"{CLIENT_PREFIX}play > ", value=f"{CLIENT_PREFIX}play <YouTube Video URL or Name>")
    embed.add_field(name=f"{CLIENT_PREFIX}queue > ", value=f"{CLIENT_PREFIX}queue <YouTube Video URLs or Name>")
    embed.add_field(name=f"{CLIENT_PREFIX}playlist > ", value=f"{CLIENT_PREFIX}playlist <Playlist Name>. <Privacy Mode (public/private)>. <YouTube Video URLs or Name>")
    embed.add_field(name=f"{CLIENT_PREFIX}playlists > ", value=f"{CLIENT_PREFIX}playlists <Playlist Name>")
    embed.add_field(name=f"{CLIENT_PREFIX}deleteplaylist > ", value=f"{CLIENT_PREFIX}deleteplaylist <Playlist Name>")
    embed.add_field(name=f"{CLIENT_PREFIX}playq > ", value=f"{CLIENT_PREFIX}playq")
    embed.add_field(name=f"{CLIENT_PREFIX}join > ", value=f"{CLIENT_PREFIX}join")
    embed.add_field(name=f"{CLIENT_PREFIX}disconnect", value=f"{CLIENT_PREFIX}disconnect")
    embed.add_field(name=f"{CLIENT_PREFIX}clear > ", value=f"{CLIENT_PREFIX}clear")
    embed.add_field(name=f"{CLIENT_PREFIX}songs > ", value=f"{CLIENT_PREFIX}songs")
    embed.add_field(name=f"{CLIENT_PREFIX}resume > ", value=f"{CLIENT_PREFIX}resume")
    embed.add_field(name=f"{CLIENT_PREFIX}pause > ", value=f"{CLIENT_PREFIX}pause")
    embed.add_field(name=f"{CLIENT_PREFIX}volume > ", value=f"{CLIENT_PREFIX}volume <1-10>")
    embed.add_field(name=f"{CLIENT_PREFIX}queueplaylist > ", value=f"{CLIENT_PREFIX}queueplaylist <Playlist Name>")
    embed.add_field(name=f"{CLIENT_PREFIX}usage > ", value=f"{CLIENT_PREFIX}usage")
    embed.add_field(name=f"{CLIENT_PREFIX}song > ", value=f"{CLIENT_PREFIX}song")
    embed.add_field(name=f"{CLIENT_PREFIX}profile > ", value=f"{CLIENT_PREFIX}profile <@user>")

    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/762338721051050024/799379888784015390/P1020461.jpg")

    await ctx.send(embed=embed)

@client.command()
async def song(ctx):
    
    try:
        voice = get(client.voice_clients, guild=ctx.guild)
        embed = discord.Embed(color=TERQ)
        full_meta_path = f"{metadata_location}\\{ctx.message.guild.id}"

    
    
        if voice.is_playing() == True or voice.is_paused() == True or os.path.isfile(music_location+"\\music.wav") == True:
            pass
        else:
            embed.set_author(name="No song is playing")

            return await ctx.send(embed=embed)


        video = return_data(f"{full_meta_path}\\metadata.json", tabel="metadata", sub_tabel="name")
        views = return_data(f"{full_meta_path}\\metadata.json", tabel="metadata", sub_tabel="views")
        author = return_data(f"{full_meta_path}\\metadata.json", tabel="metadata", sub_tabel="author")
        

        embed.set_author(name=f"Current Playing Song")

        embed.add_field(name="Song > ", value=video, inline=False)
        embed.add_field(name="Views > ", value=views, inline=False)
        embed.add_field(name="Song Requested By > ", value=author, inline=False)

        await ctx.send(embed=embed)

    except AttributeError:
        
        embed.set_author(name="I am not connected to a voice channel")

        await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def prefix(ctx, prefix : str):

    embed = discord.Embed(colour=LIGHT_BLUE)
    with open(config_location+"\\prefix.json", "w") as pfx:

        New_pfx = {}
        New_pfx['pfx'] = ({
            "setting1": prefix
        })

        json.dump(New_pfx, pfx, indent=4)

    embed.set_author(name=f"Changed Prefix to > {prefix}")

    await ctx.send(embed=embed)

@client.command()
async def profile(ctx, member : discord.User):
    try:

        embed = discord.Embed(color=TERQ)
        user_id = member.id

        full_usr_path = f"{user_location}\\{ctx.message.guild.id}"

        with open(f"{full_usr_path}\\{user_id}\\{user_id}-exp.json") as read_level_data:

            text = read_level_data.read()
            json_readable = json.loads(text)

            json_tabel = json_readable[str(user_id)]

            current_level = json_tabel['member-level']
            current_exp = json_tabel['member-exp']
            until_next_levelup = json_tabel['member-until-next-lvl']
    
        with open(f"{full_usr_path}\\{user_id}\\{user_id}.json") as read_user:

            text = read_user.read()
            json_formatted = json.loads(text)
        
            user_info = json_formatted[str(user_id)]

            embed.set_author(name=f'Here is "{user_info["member-name"]}" Profile')
            embed.add_field(name=f"User Name  |   {user_info['member-name']}", value="|", inline=False)
            embed.add_field(name=f"User ID   |   {user_info['member-id']}", value="|", inline=False)
            embed.add_field(name=f"User Join Date   |   {user_info['member-joindate'].split('.')[0]}", value="|", inline=False)
            embed.add_field(name=f"Current User Level   |   {current_level}", value="|", inline=False)
            embed.add_field(name=f"Current User Experience   |   {current_exp}", value="|", inline=False)
            embed.add_field(name=f"Until Next Level Up   |   {int(until_next_levelup-current_exp)}", value="|", inline=False)
            embed.set_image(url=user_info['member-avatar'])

            await ctx.send(embed=embed)

    except (FileNotFoundError, commands.UserNotFound):
        embed.color = RED
        embed.set_author(name=f"No Member the name {member}")

        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason):

    name = f"{member.name}#{member.discriminator}"
    embed = discord.Embed(color=MEDIUM_PURPLE)

    await member.ban(reason=reason)

    embed.set_author(name=f"Banned {name}")
    embed.add_field(name="Reason: ", value=reason)
    embed.set_thumbnail(url=vorbis_img)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason):

    name = f"{member.name}#{member.discriminator}"
    embed = discord.Embed(color=MEDIUM_PURPLE)

    await member.kick(reason=reason)

    embed.set_author(name=f"Kicked {name}")
    embed.add_field(name="Reason: ", value=reason)
    embed.set_thumbnail(url=vorbis_img)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):

    embed = discord.Embed(color=MEDIUM_PURPLE)
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
  
    if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        
        embed.set_author(name=f"Unbanned {member}")

        await ctx.send(embed=embed)
        
@client.command()
@commands.has_permissions(administrator=True)
async def setup(ctx, *, args):

    embed = discord.Embed(color=MEDIUM_PURPLE)
    commands = ["help", "join_role", "max_warnings"]
    arg = args.split(", ")

    if arg[0] == commands[0]:
        embed.set_author(name="Setup Help")

        embed.add_field(name="Note > ", value="This may seem complicated, but don't worry! just follow the examples!")
        embed.add_field(name="join_role", value="Example > /setup join_role, <The role to give when a player joins>")

    elif arg[0] == commands[1]:

        role = arg[1]
        print(role)

        role_to_give = discord.utils.get(client.get_guild(ctx.message.guild.id).roles, name=role)
        print(role_to_give)
        if role_to_give is None:
            print("Role does not exist")
            embed.set_author(name=f'"{role}" is not a role!')

            
        else:
            with open(f"{config_location}\\{ctx.message.guild.id}\\join_role.json", "w+") as make_join_role:

                data = {}

                data["join_role"] = ({
                    "role": f"{role_to_give}"
                })

                json.dump(data, make_join_role, indent=4)

                embed.set_author(name=f"I have made {role_to_give} the role to give new members!")

    elif arg[0] == commands[2]:

        new_max_warnings = int(arg[1])

        data = {}
        data["setting1"] = {
            "warnings": new_max_warnings
        }

        make_asset(file=config_location+ctx.guild.id+"max_warnings.json", mode="w+", data=data, indent=4)

        embed.set_author(name=f"I have set the Max Warnings to {new_max_warnings}")

    await ctx.send(embed=embed)
    
for filename in os.listdir(cog_location):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')    

client.run(TOKEN)
