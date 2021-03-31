"""Made by: Austin Ares, Fabian Kuzbiel"""


import discord, time, os, shutil, youtube_dl, youtubesearchpython, json, datetime, random, logging, asyncio, lyricsgenius

from discord.ext import commands, tasks
from discord.utils import get
from discord import Spotify

TOKEN = None

CLIENT_ID = "Spotify ID"
CLIENT_SECRET = "Another secret"
GENIUS_ID = "Some ID"
GENIUS_SECRET = "Did you read the Variable name? It's a secret."
GENIUS_ACCESS_TOKEN = "Nunya"

"""Location Variables"""

global file_path, music_location, ydl_opts, res_location, config_location, playlist_location, metadata_location

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
global_profile = file_path+"\\GlobalProfiles"

"""Logger parameters"""

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="vorbis_info.log", encoding='utf-8', mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

"""Music Download Parameters"""

ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '256',

        }],

    }

colour_opts = {
    "red": [255, 0, 0],
    "blue": [0, 0, 255],
    "green": [0, 255, 0],
    "white": [255, 255, 255],
    "yellow": [255, 255, 0],
    "light blue": [0,128,255]
}

"""Genius Parameters"""

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, skip_non_songs=True, remove_section_headers=True)

"""Functions"""

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
    filtered_8 = ''.join(filter(lambda char: char != ",", filtered_7))
    filtered_9 = ''.join(filter(lambda char: char != "/", filtered_8))

    return filtered_9

def filt_str_mod(string : str):

    filtered_1 = ''.join(filter(lambda char: char != '"', string))
    filtered_2 = ''.join(filter(lambda char: char != ':', filtered_1))
    filtered_3 = ''.join(filter(lambda char: char != '|', filtered_2))
    filtered_4 = ''.join(filter(lambda char: char != '.', filtered_3))
    filtered_5 = ''.join(filter(lambda char: char != ']', filtered_4))
    filtered_6 = ''.join(filter(lambda char: char != '[', filtered_5))
    filtered_7 = ''.join(filter(lambda char: char != "'", filtered_6))


    return filtered_7

def filt_str_url(string : str):

    filtered_1 = ''.join(filter(lambda char: char != '"', string))
    filtered_2 = ''.join(filter(lambda char: char != '|', filtered_1))
    filtered_3 = ''.join(filter(lambda char: char != ']', filtered_2))
    filtered_4 = ''.join(filter(lambda char: char != '[', filtered_3))
    filtered_5 = ''.join(filter(lambda char: char != "'", filtered_4))


    return filtered_5

def return_data(file : str, tabel : str=None, sub_tabel : str=None):
    try:
        if tabel is None:
            with open(file) as data:

                RwText_Data = data.read()
                RwJSON_Data = json.loads(RwText_Data)

                return RwJSON_Data

        elif tabel is not None and sub_tabel is not None:
            with open(f"{file}") as data:

                RwText_Data = data.read()
                RwJSON_Data = json.loads(RwText_Data)

                return RwJSON_Data[tabel][sub_tabel]

        elif tabel is not None and sub_tabel is None:
            with open(f"{file}") as data:

                RwText_Data = data.read()
                RwJSON_Data = json.loads(RwText_Data)

                return RwJSON_Data[tabel]


    except (FileNotFoundError, OSError, KeyError):
        return None

def check_channel(guild_id : int, original_guild_id : int, channel_id : int, original_channel_id : int, author_id : int, original_author_id : int):

    if guild_id == original_guild_id and channel_id == original_channel_id and author_id == original_author_id:
        return True
    else:
        return False

def parseArgs(context : discord.Message=None, Type=None):

    if context is None:
        return None

    else:
        content = context.message.content

        if Type == "url":
            args = filt_str_url(str(content.split(" ")))

        else:
            args = filt_str_mod(str(content.split(" ")))

        parsedArgs = args.split(", ")
        parsedArgs.pop(0)

        parsedArgs = " ".join(parsedArgs)
        parsedArgs = parsedArgs.split(", ")

        return parsedArgs

async def sendEmbed(errorEmbed : discord.Embed, context : any=None, msg : str=None):

    errorEmbed.set_author(name=f"{msg}")

    await context.send(embed=errorEmbed)

async def recomendPlaylistTimer():

    print("Activated Recomended Playlist Timer")

    highestValue = 0
    listOfPlaylists = {}
    nameList = []
    recommendedPlaylist = {}
    recommendedPlaylist['src'] = {}

    while True:
        nameList.clear()

        for x in range(len(os.listdir(playlist_location))):
            try:

                playlistName = f"{os.listdir(playlist_location)[x]}"
                playlist = return_data(f"{playlist_location}\\{playlistName}\\{playlistName}.json")

                if playlist["info"]["privicy"] == "public":
                    try:

                        playlistPlaybackCount = playlist["metadata"]["queue-count"]
                        playlistAuthorName = playlist["metadata"]["playlist-author-name"]
                        playlistID = playlist["metadata"]["playlist-id"]

                        nameList.append(playlistName)
                        listOfPlaylists[f"{playlistName}"] = [playlistName, playlistPlaybackCount, playlistID]
                    except KeyError:
                        pass
                else:
                    continue
            except (PermissionError, json.decoder.JSONDecodeError):
                pass

        for y in range(len(nameList)):

            highestValueOld = highestValue
            highestValueTemp = listOfPlaylists[f"{nameList[y]}"]
            highestValueStr = listOfPlaylists[f"{nameList[y]}"][0]

            if highestValueTemp[1] >= highestValueOld:
                highestValue = highestValueTemp[1]
                highestValueName = highestValueTemp[0]
                highestValueID = highestValueTemp[2]

                recommendedPlaylist["src"]["playlist-name"] = highestValueName
                recommendedPlaylist["src"]["playlist-id"] = highestValueID

                make_asset(f"{file_path}\\recommendedPlaylist.json", "w", recommendedPlaylist, 4)


            else:
                pass

        await asyncio.sleep(3600)

def checkPlaylistExistance(playlistName):

    if os.path.isfile(f"{playlist_location}\\{playlistName}\\{playlistName}.json"):
        return True
    else:
        return False

def checkPlaylistPrivacy(playlistName):
    if checkPlaylistExistance(playlistName):

        playlistPrivacy = return_data(f"{playlist_location}\\{playlistName}\\{playlistName}.json")["info"]["privicy"]

        if playlistPrivacy == "public":
            return "public"
        elif playlistPrivacy == "private":
            return "private"
        elif playlistPrivacy == "server":
            return "server"
        else:
            return False

    else:
        return None

def findPlaylistTags(tags):

    playlistList = filt_str_mod(str(os.listdir(playlist_location)))



    blacklistedPlaylists = []
    acceptedPlaylists = []
    maxInt = [0, 1]

    for x in range(len(os.listdir(playlist_location))):



        playlistName = os.listdir(playlist_location)[x]
        playlistData = return_data(f"{playlist_location}\\{playlistName}\\{playlistName}.json")

        if playlistData["info"]["privicy"] == "public":
            if tags in playlistData["metadata"]["tags"]:
                try:
                    if playlistName != blacklistedPlaylists and int(playlistData["metadata"]["queue-count"]) > int(maxInt[0]) and int(playlistData["metadata"]["queue-count"]) > int(maxInt[1]):
                        acceptedPlaylists.append(playlistName)
                        maxInt.pop()
                        maxInt.append(int(playlistData["metadata"]["queue-count"]))
                    else:
                        continue

                except IndexError:
                    pass

    return acceptedPlaylists

def image(img):

    if str(img).startswith("https") and str(img).endswith(".png") or str(img).endswith(".jpg"):
        return True
    else:
        return False

class getPlaylistInfo():

    def __init__(self, playlist, check=True):

        self.playlist = playlist
        self.path = f"{playlist_location}\\{playlist}\\{playlist}.json"
        self.playlistData = return_data(self.path)
        self.playlistID = self.playlistData["metadata"]["playlist-id"]
        self.playlistAuthors = self.playlistData["metadata"]["playlist-author"]
        self.playlistAuthorName = self.playlistData["metadata"]["playlist-author-name"]
        self.playlistTags = self.playlistData["metadata"]["tags"]
        self.playlistTrustedGuilds = self.playlistData["metadata"]["server-playlist"]
        self.playlistQueueCount = self.playlistData["metadata"]["queue-count"]
        self.playlistCoverArt = self.playlistData["metadata"]["playlist-cover"]
        self.playlistLengthMinutes = self.playlistData["metadata"]["playlist-length"]
        self.playlistSongContents = self.playlistData["info"]["playlist"]
        self.playlistPrivicySetting = self.playlistData["info"]["privicy"]
        self.checkSetting = check

    def playlistname(self):
        return self.playlist
    def path(self):
        return self.path
    def rawplaylist(self):
        return self.playlistData
    def playlistid(self):
        return self.playlistID
    def playlistauthor(self):
        return self.playlistAuthors
    def playlistauthorname(self):
        return self.playlistAuthorName
    def playlistags(self):
        return self.playlistTags
    def playlisttrustguilds(self):
        return self.playlistTrustedGuilds
    def playlistqueuecount(self):
        return self.playlistQueueCount
    def playlistcoverart(self):
        return self.playlistCoverArt
    def playlistlength(self):
        return self.playlistLengthMinutes
    def playlistsongcontents(self):
        return self.playlistSongContents
    def playlistprivacy(self):
        return self.playlistPrivicySetting


def check_owner(playlist : str, owner_id : int):
    try:
        if checkPlaylistExistance(playlist):
            playlist_data = return_data(file=f"{playlist_location}\\{playlist}\\{playlist}.json")

            if int(owner_id) in playlist_data['metadata']['playlist-author']:
                return True
            else:
                return False
        else:
            raise OSError("Playlist Not Existing")
    except:
        return None
CLIENT_PREFIX = "/"
#return_data(file=config_location+"\\prefix.json", tabel="pfx", sub_tabel="setting1")
client = commands.AutoShardedBot(shard_count=1, command_prefix="/", case_insenstive=True, guild_subscriptions=True, intents=intents)

"""Embed Colours"""

WHITE = discord.Color.from_rgb(255, 255, 255)
TERQ = discord.Color.from_rgb(49,171,159)
RED = discord.Color.from_rgb(255, 0, 0)
YELLOW = discord.Color.from_rgb(255, 255, 0)
LIGHT_BLUE = discord.Color.from_rgb(0,128,255)
MEDIUM_PURPLE = discord.Color.from_rgb(147, 112, 219)
GOLD = discord.Color.from_rgb(207,181,59)

"""Bot Code"""

@client.remove_command("help")
@client.event
async def on_ready():
    print("Vorbis is Online")

    await client.change_presence(status=discord.Status.online, activity=discord.Game(f'{CLIENT_PREFIX}help'))
    asyncio.create_task(recomendPlaylistTimer())

@client.command(aliases=['help', 'h', 'a'])
async def assist(ctx):
    embed = discord.Embed(color=MEDIUM_PURPLE)
    try:
        content = parseArgs(ctx)
        arg = content[0]

        if int(arg) == 2:
            embed.set_author(name=f"≥ Commands 2")

            embed.add_field(name=":eject:  More Playlist Commands  :eject:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}prtrust ● ", value='Removes permissions for the selected player to use private playlists (AKA: If your playlist privacy is set to "private" this command will take permissions from the selected member to use your playlist)')
            embed.add_field(name=f"{CLIENT_PREFIX}pprivacy ● ", value="Will change privacy setting (Depending on what you set it as, private, public or server) (AKA: public means anyone can use your playlist, even people in other servers, private means only you can use it, and server means only the members of the server you're in can use it)")
            embed.add_field(name=f"{CLIENT_PREFIX}paserver ● ", value='Whitelists selected server on to the selected playlists whitelist (AKA: This means, if your playlist privacy is set to "server", you can allow another server to use the playlist as well)')
            embed.add_field(name=f"{CLIENT_PREFIX}rsong ● ", value='Removes A song from A playlist, (AKA: You can do this via the song name, or what position it is in the playlist, Example: song1, song2, song3. song3 would be position 3, so if you cannot be bothered to type it, or its in another language, do that)')
            embed.add_field(name=f"{CLIENT_PREFIX}prname ● ", value='Renames A playlist, (AKA: You can rename a playlist, you can rename it to swear words, or account info, or just anything, but if you get hacked, do not blame me, blame yourself, no two playlist names can be the same, so the name you chose is uniquely yours!)')
            embed.add_field(name=f"{CLIENT_PREFIX}atag ● ", value=f'Adds A tag onto your playlist, (AKA: you or other people can search for your playlist with the tag you put on your playlist, you can put as many tags as you like, You have to put one tag at a time, An alias for this command is {CLIENT_PREFIX}at)')
            embed.add_field(name=f"{CLIENT_PREFIX}playliststag", value=f'Finds A playlist via tag (AKA: Finds a playlist via tag, will return Nothing if that tag has not been used at all. The command can return up to 5 playlists at once, An alias for this command is {CLIENT_PREFIX}pt)')
            embed.add_field(name=f"{CLIENT_PREFIX}eplaylist", value=f'Edits basic parts of your profile (AKA: You can change aspects your playlist, like your playlist thumbnail (Has to be a URL), the description, and the colour')
            embed.add_field(name=f"{CLIENT_PREFIX}link", value=f'Will link your profile to another guild, (NOTE: you can only link your server to one guild at a time, and Vorbis has to be in the guild. And as of now, this feature is not ready)')
            embed.add_field(name=f":musical_note: More Music Commands :musical_note:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}lyrics", value=f"Will return specified song lyrics by a specified artist, (AKA: Will return song lyrics, does this via Genius™ API, if you do not pass Artist name or a song, will return A command Failure.)")

            return await ctx.send(embed=embed)
    except ValueError:
        pass

    """Help Command"""




    embed.set_author(name=f"≥ Commands")
    embed.add_field(name=":soccer:  General Commands  :soccer:", value="\u200b", inline=False)
    embed.add_field(name=f"{CLIENT_PREFIX}assist ● ", value="This Command")
    embed.add_field(name=f"{CLIENT_PREFIX}usage ● ", value="Shows Usage of All Commands")
    embed.add_field(name=f"{CLIENT_PREFIX}join ● ", value="Joins channel User is currently in")
    embed.add_field(name=f"{CLIENT_PREFIX}disconnect ● ", value="disconnects from channel User is currently in")
    embed.add_field(name=f"{CLIENT_PREFIX}profile ● ", value="Shows infomation about specified user")
    embed.add_field(name=f"{CLIENT_PREFIX}this ● ", value="Shows infomation about the server")
    embed.add_field(name=":musical_note:  Music Commands  :musical_note:", value="\u200b", inline=False)
    embed.add_field(name=f"{CLIENT_PREFIX}pause ● ", value="Pauses Currently Playing Song")
    embed.add_field(name=f"{CLIENT_PREFIX}resume ● ", value="Resumes Currently Playing Song")
    embed.add_field(name=f"{CLIENT_PREFIX}play ● ", value="Plays Selected Song")
    embed.add_field(name=f"{CLIENT_PREFIX}songs ● ", value="Lists all Songs in Queue")
    embed.add_field(name=f"{CLIENT_PREFIX}clear ● ", value="Clears all Songs from Queue")
    embed.add_field(name=f"{CLIENT_PREFIX}queue ● ", value="Queues song(s)")
    embed.add_field(name=f"{CLIENT_PREFIX}volume ● ", value="Sets volume of Bot")
    embed.add_field(name=f"{CLIENT_PREFIX}song ● ", value="Shows Current song (If one is playing)")
    embed.add_field(name=f"{CLIENT_PREFIX}spotify ● ", value="Shows infomation about what the specified user is playing on Spotify")
    embed.add_field(name=":eject:  Playlist Commands  :eject:", value="\u200b", inline=False)
    embed.add_field(name=f"{CLIENT_PREFIX}asong ● ", value="Will append songs on to the selected playlist (AKA: Will add songs will a selected playlist)")
    embed.add_field(name=f"{CLIENT_PREFIX}playlist ● ", value="Makes a playlist (AKA: Makes a playlist will your own unique songs, name, and privacy settings)")
    embed.add_field(name=f"{CLIENT_PREFIX}playlists ● ", value="Shows a playlists contents (AKA: Shows infomation about the selected playlist)")
    embed.add_field(name=f"{CLIENT_PREFIX}queueplaylist ● ", value="Queues a playlist (AKA: Will queue the selected playlist for playback, this could take awhile depending on how big your playlist is, and what songs are in it)")
    embed.add_field(name=f"{CLIENT_PREFIX}deleteplaylist ● ", value="Deletes a playlist (AKA: Will delete a selected playlist, Thus, nor you or anyone else can use the selected playlist, this command cannot be un-done)")
    embed.add_field(name=f"{CLIENT_PREFIX}ptrust ● ", value='Gives permissions for the selected player to use private playlists, (AKA: If your playlist privacy is set to "private" this command will allow the selected member to use your playlist)')
    embed.add_field(name=f"Note:", value='do "/help 2" for more commands')

    curnt_time = str(datetime.datetime.now())
    embed.set_footer(text=curnt_time.split(".")[0])

    await ctx.send(embed=embed)

@client.command(aliases=['pu'])
async def purge(ctx, amt : int=None):

    """Purge Command"""

    if amt is None:

        await ctx.send("You need to specify an amount of messages to purge (Maximum Amount: 250)")
    elif amt > 249:
        await ctx.send("You cannot delete more than 250 messages at a time")
    else:
        amt = amt+1

        await ctx.channel.purge(limit=amt)
        await ctx.send(f"Purged {ctx.channel} by {amt} messages")

        time.sleep(3)
        await ctx.channel.purge(limit=1)

@client.command(aliases=['pl'])
async def play(ctx, *, url : str=None):

    """Variables Needed for the play Command"""
    guild_id = ctx.guild.id
    guild = f"\\{ctx.message.guild.id}"
    guild_ = client.get_guild(guild_id)
    embed = discord.Embed(colour=LIGHT_BLUE)

    if url is None:

        embed.set_author(name="You need to specify a song to play.")

        return await ctx.send(embed=embed)

    multiple_songs = url.split(',')
    full_path = music_location+guild
    queue_full_path = queue_location+guild
    meta_full_path = metadata_location+guild
    config_full_path = config_location+guild
    server = client.get_guild(ctx.message.guild.id)
    embed = discord.Embed(colour=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)
    client_volume = return_data(config_location+f"\\{ctx.guild.id}\\config.json", "config", "vol")

    if client_volume is None:
        return await ctx.send(f"You have not set a default volume, you can do this with {CLIENT_PREFIX}volume <Integer Value> like 1 or 2")

    """Code"""

    """Checks if the multiple_songs variable (URL) is equal to a player"""

    if voice and voice.is_playing():

        embed.color = RED
        embed.set_author(name="Already Playing, (If there is no audio, it's because it's paused)")

        return await ctx.send(embed=embed)

    if voice and voice.is_connected():
        pass
    else:
        try:

            channel = ctx.message.author.voice.channel
            return await channel.connect()

        except AttributeError:
            embed.color = RED
            embed.set_author(name="You're not connected to A Voice Channel")

            return await ctx.send(embed=embed)

    if multiple_songs[0].startswith("<@!"):

        i = multiple_songs[0].split('!')
        i = i[1].split('>')[0]

        user = server.get_member(int(i))
        print(user.activities)

        """Gets Spotify Status from chosen player (if user is playing a song on spotify)"""

        for activity in user.activities:
            if isinstance(activity, Spotify):
                url = str(activity.title)
            else:
                embed.color = RED
                embed.set_author(name="User is not playing any song!")

                return await ctx.send(embed=embed)

    os.chdir(full_path)


    url = youtubesearchpython.SearchVideos(url, offset=1, mode='dict', max_results=1)

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

    if int(len(length.split(':'))) >= 2 and int(len(length.split(':'))) >= 3:


        embed.color = RED
        embed.set_author(name=f"Cannot Download Song, Song is {length.split(':')[0]} hours! Limit is 2 hours!")

        return await ctx.send(embed=embed)

    embed.set_author(name=f'Playing "{title}"')
    embed.add_field(name=f"Views Ø ",value=views)
    embed.add_field(name=f"Link Ø ",value=video, inline=False)
    embed.add_field(name=f"Length Ø ",value=length, inline=False)
    embed.add_field(name=f"Channel Ø ",value=channel, inline=False)
    embed.set_footer(text=f"Client Volume Ø {int(client_volume)}")

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

            try:
                client_volume = return_data(config_location+f"\\{ctx.guild.id}\\config.json", "config", "vol")

                voice.play(discord.FFmpegPCMAudio(music_file), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = client_volume

            except discord.errors.ClientException:
                pass

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
async def queueplaylist(ctx, *, playlist=None):

    """queueplaylist command"""

    embed = discord.Embed(color=LIGHT_BLUE)
    ctx_author = ctx.author.name+"#"+ctx.author.discriminator
    url = None
    guild = f"\\{ctx.message.guild.id}"

    if playlist is None:

        embed.set_author(name="You need to specify a playlist.")

        return await ctx.send(embed=embed)

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
        playCount = int(json_meta['queue-count'])+1
        songs = json_text_file['playlist'].split(',')

        async def queue_playlist():

            embed.set_author(name=f'Queueing the Playlist Ø "{playlist}"')

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
                    try:
                        try:
                            filtered = filt_str(title)

                            ydl.download([link])
                        except youtube_dl.utils.DownloadError as e:
                            return await ctx.send(f'Could not download song "{filtered}"\n\nDebug Infomation Ø {e}')
                        try:
                            os.rename(os.listdir()[0], filtered+".wav")
                            shutil.move(os.listdir()[0], full_queue_path)
                        except FileExistsError:
                            os.remove(temp_location+f"\\{ctx.guild.id}\\{os.listdir()[0]}")



                    except shutil.Error:
                        pass
        if privacy_setting == "public" or ctx.author.id == author:
            await queue_playlist()

            playlist_path = f"{playlist_location}\\{playlist}\\{playlist}.json"
            playlist_data = return_data(playlist_path)
            playlist_data["metadata"]["queue-count"] = playCount
            globalData = return_data(global_profile+f"\\{ctx.author.id}\\{ctx.author.id}.json")

            try:

                playlistID = playlist_data["metadata"]["playlist-id"]

                if playlistID in globalData["global"]["listened-playlist-list"]:
                    pass
                else:
                    globalData["global"]["listened-playlist-list"].append(playlistID)

                globalData["global"]["playlist-list"][f"{playlistID}"] = {
                    "playlist-id": playlistID,
                    "playlist": playlist,
                    "play-count": int(globalData["global"]["playlist-list"][f"{playlistID}"]["play-count"]+1)
                }

            except (TypeError, KeyError):
                globalData["global"]["playlist-list"][f"{playlistID}"] = {
                    "playlist-id": playlistID,
                    "playlist": playlist,
                    "play-count": 0
                }
            finally:
                make_asset(playlist_path, "w", playlist_data, 4)
                make_asset(global_profile+f"\\{ctx.author.id}\\{ctx.author.id}.json", "w", globalData, 4)

        elif privacy_setting == "server":
            if int(ctx.guild.id) in json_meta['server-playlist']['playlist-guild']:
                await queue_playlist()
            else:
                embed.color = RED
                embed.set_author(name="This Playlist is server only (meaning, the playlist is whitelisted, and only selected servers can use this playlist)")
        else:
            embed.color = RED
            embed.set_author(name="This playlist is private!")

        embed.set_author(name=f'Queued the playlist Ø "{playlist}"')
        return await ctx.send(embed=embed)



@client.command(pass_context=True, aliases=['j'])
async def join(ctx):

    try:
        embed = discord.Embed(color=LIGHT_BLUE)
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)

    except AttributeError:

        embed.color = LIGHT_BLUE
        embed.set_author(name="You're not connected to a voice channel.")

        return await ctx.send(embed=embed)

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

    embed = discord.Embed(color = LIGHT_BLUE)
    try:
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)
    except AttributeError:

        embed.color = LIGHT_BLUE
        embed.set_author(name="I'm not in a channel.")

        return await ctx.send(embed=embed)
    """If Bot is in Voice Channel is Connect, it disconnects"""

    if voice and voice.is_connected():

        embed.set_author(name=f"Disconnected from {channel}")
        await ctx.send(embed=embed)

        await voice.disconnect(force=True)


    else:
        """If bot is already disconnected from the voice channel, it sends the following message"""
        embed.set_author(name="I am not in any Voice Channel!")
        embed.color = RED
        await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=['q'])
async def queue(ctx, *, url=None):

    guild = f"\\{ctx.message.guild.id}"
    full_queue_path = queue_location+guild
    full_temp_path = temp_location+guild
    embed = discord.Embed(colour=YELLOW)

    if url is None:

        embed.color = LIGHT_BLUE
        embed.set_author(name="You need to specify some songs.")

        return await ctx.send(embed=embed)

    multiple_songs = url.split(',')

    if len(multiple_songs) > 1:
        await ctx.send(f"Downloading {len(multiple_songs)} song(s)")


    for x in range(len(multiple_songs)):

        url = multiple_songs[x]

        """Queue Command"""




        if len(os.listdir(full_queue_path)) > 14:

            embed.set_author(name="Queue has reached limit in songs, limit is 15 songs!")
            embed.color = RED

            return await ctx.send(embed=embed)

        """YouTube API"""


        queued_song = youtubesearchpython.SearchVideos(url, offset=1, mode='dict', max_results=1)

        """Splits YouTube Search API into Variables"""

        try:
            video = str(queued_song.links[0])
            views = str(queued_song.views[0])
            thumbnail = queued_song.thumbnails[0]
            title = str(queued_song.titles[0])
            lenght = str(queued_song.durations[0])
            channel = str(queued_song.channels[0])

        except IndexError:
            return await sendEmbed(embed, ctx, f'No song / video with the name "{url}" (I have stopped queueing songs)')
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

    guild_queue = f"{queue_location}\\{ctx.guild.id}"
    first_song = None

    if len(os.listdir(guild_queue)) > 0:
        first_song = os.listdir(guild_queue)[0].split(".wav")[0]
    embed = discord.Embed(color=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)


    embed.set_author(name="Skipping Current Song")



    if voice and voice.is_playing():

        if first_song is None:
            embed.set_author(name="No more songs")

        else:
            embed.set_author(name=f"Now Playing: {first_song}")

        voice.pause()
        voice.stop()
    else:
        embed.set_author(name="No song to be skipped")

    await ctx.send(embed=embed)

@client.command(aliases=['v'])
async def volume(ctx, volume_float : float=None):

    guild = f"\\{ctx.message.guild.id}"
    full_config_path = config_location+guild
    embed = discord.Embed(colour=LIGHT_BLUE)

    if volume_float is None:
        embed.set_author(name="You need to set a volume. (In a float value, like: 0.1, 0.6, 1.7)")

    else:

        New_vol = {}
        New_vol['volume'] = ({
            "vol": volume_float
        })

        make_asset(file=full_config_path+"\\volume.json", mode="w", data=New_vol, indention=4)

        embed.set_author(name=f"Changed volume to > {volume_float}")

    await ctx.send(embed=embed)

@client.command(aliases=['unpause', 'u'])
async def resume(ctx):
    embed = discord.Embed(color=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice != None:

        if voice.is_playing():
            embed.set_author(name="Already Playing")

        elif voice.is_paused():
            embed.set_author(name="Resumed")

            voice.resume()
        else:
            embed.set_author(name="I'm not playing audio")
    else:
        embed.set_author(name="I am not connected to a Voice Channel!")

    await ctx.send(embed=embed)

@client.command(aliases=['sn'])
async def songs(ctx, song : int=None):

    os.chdir(queue_location+f"\\{ctx.message.guild.id}")
    embed = discord.Embed(color=LIGHT_BLUE)
    song_list = []

    if len(os.listdir()) == 0:
        embed.set_author(name="No Songs")
        return await ctx.send(embed=embed)
    else:
        for x in range(len(os.listdir())):
            y = os.listdir()[x].split('.wav')
            song_list.append(y)

        text = ""
        if song is not None:
            try:
                text = f"Queued song in position {song} Ø {filt_str(str(song_list[song+1]))}"
            except IndexError:
                text = f"There is no song in position {song}."
        else:
            resault = filt_str_mod(string=str(song_list))
            text = f"Songs Left in Queue Ø {resault}"

        await ctx.send(text)



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
async def playlist(ctx):

    id_letters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', '_', '-', '!']
    song_list = []
    song_len = []
    embed = discord.Embed(color=LIGHT_BLUE)
    final_len = 0

    playlist_name = None
    mode = None
    url = []

    try:
        args = str(ctx.message.content).split("/playlist ")[1]
        arguments = args.split(", ")

        playlist_name = arguments[0]
        mode = arguments[1]
        url = []

        print(len(arguments))
        if len(arguments) > 2:
            pass
        else:
            embed.color = RED
            embed.set_author(name='Missing Playlist Arguments (Help > "/playlist <playlist name>, <public | private>, <song1, song2, song3 ect...>")')

            return await ctx.send(embed=embed)

        for z in range(2, len(arguments)):
            url.append(arguments[z])

    except (AttributeError, IndexError):

        done = False
        done1 = False
        done2 = False

        await ctx.send("What do you want your playlist name to be?")

        while done is False:


            args = await client.wait_for('message')

            if args.channel.id == ctx.channel.id and args.guild.id == ctx.guild.id and args.author.id == ctx.author.id:
                playlist_name = args.content

                await ctx.send("What do you want your playlist privacy setting to be? (public or private)")
                while done1 is False:

                    args1 = await client.wait_for('message')

                    if args1.channel.id == ctx.channel.id and args1.guild.id == ctx.guild.id and args1.author.id == ctx.author.id:
                        if args1.content == "private" or args1.content == "public" or args1.content == "server":
                            mode = args1.content

                            await ctx.send("What songs do you want in your playlist? (Please seperate song names with a comma)")

                            while done2 is False:

                                url_args = await client.wait_for('message')

                                if url_args.channel.id == ctx.channel.id and url_args.guild.id == ctx.guild.id and url_args.author.id == ctx.author.id:

                                    url_args_ = url_args.content.split(", ")

                                    for z in range(0, len(url_args_)):
                                        url.append(url_args_[z])

                                        done2 = True
                                        done1 = True
                                        done = True

                                else:
                                    pass
                        else:
                            return await ctx.send("Incorrect privacy setting (public or private)")
                    else:
                        pass


            else:
                pass
    os.chdir(playlist_location)

    playlist_id = random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)


    url = filt_str_mod(str(url))

    mod_url = url.split(", ")

    linkLists = return_data(file_path+"\\tags-link.json")

    if playlist_id in linkLists["list"]["tags"]:
        playlist_id = random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)


    linkLists["list"]["tags"].append(playlist_id)
    make_asset(file_path+"\\tags-link.json", "w", linkLists, 4)


    for x in range(len(mod_url)):
        convt_url = youtubesearchpython.SearchVideos(keyword=mod_url[x], offset=1, mode="dict", max_results=1)

        thumbnail = convt_url.thumbnails[0]
        title = convt_url.titles[0]
        length = int(convt_url.durations[0].split(':')[0])

        song_len.append(length)
        song_list.append(title)

        final_len = final_len+song_len[x]

    final_songs = filt_str_mod(str(song_list))

    conv_url_ = youtubesearchpython.SearchVideos(keyword=random.choice(mod_url), offset=1, mode="dict", max_results=1)

    thumbnail = conv_url_.thumbnails[0]

    print(thumbnail)

    playlist_ = playlist_location+f"\\{playlist_name}"
    full_author = ctx.author.name+"#"+ctx.author.discriminator

    if mode == "public" or mode == "private" or mode == "server":

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
                "playlist-author": [ctx.author.id],
                "playlist-cover": thumbnail[1],
                "playlist-length": final_len,
                "playlist-id": playlist_id,
                "playlist-author-name": full_author,
                "queue-count": 0,
                "server-playlist": [int(ctx.guild.id)],
                "tags": [],
                "playlist-creation": str(datetime.datetime.now())

            })

            json.dump(playlist_info, new_playlist, indent=4)

            embed.set_author(name=f'Made new Playlist Ø "{playlist_name}"')
            embed.add_field(name="Author ● ", value=full_author, inline=False)
            embed.add_field(name="Songs ● ", value=final_songs, inline=False)
            embed.add_field(name="Privacy Setting ● ", value=mode)

            embed.set_image(url=thumbnail[1])
            embed.set_thumbnail(url=vorbis_img)

            await ctx.send(embed=embed)


@client.command()
async def playlists(ctx, *, playlist=None):

    embed = discord.Embed(color=LIGHT_BLUE)
    playlistOld = None
    playlistID = None
    name = None
    if playlist is None:
        playlistData = return_data(f"{file_path}\\recommendedPlaylist.json", "src")

        playlist = playlistData["playlist-name"]
        playlistID = playlistData["playlist-id"]

    else:
        playlistOld = False

    playlist_ = playlist_location+f"\\{playlist}\\"

    print(playlist_+f"{playlist}.json")
    if os.path.isfile(playlist_+f"{playlist}.json"):

        with open(playlist_+f"{playlist}.json") as read_playlist:

            text = read_playlist.read()
            json_data = json.loads(text)
            playlist_json = json_data['info']
            playlist_metadata = json_data['metadata']

            if playlist_json["privicy"] == "public" or ctx.author.id in playlist_metadata["playlist-author"]:

                if playlistOld is None:
                    print(playlistID)
                    if str(playlistID) != str(playlist_metadata["playlist-id"]):

                        embed.set_author(name="Most popular playlist has been deleted.")

                        return await ctx.send(embed=embed)
                    else:
                        embed.set_author(name=f'Most popular playlist')

                        embed.add_field(name=f"Playlist Name Ø", value=playlist, inline=False)
                        embed.set_footer(text="Note: Most popular playlist changes once an hour, if it's still the same after 1 hour, it's just because it's still the most popular lol")

                        embed.color = GOLD

                else:
                    embed.set_author(name=f'Here is the playlist "{playlist}"')

                try:
                    embed.add_field(name="Playlist Description > ", value=playlist_metadata["playlist-description"], inline=False)
                except KeyError:
                    pass
                embed.set_image(url=playlist_metadata['playlist-cover'])

                embed.add_field(name=f"Author of Playlist > ", value=playlist_metadata['playlist-author-name'], inline=False)
                embed.add_field(name="Songs > ", value=playlist_json['playlist'], inline=False)
                embed.add_field(name="Length of Playlist (Minutes) > ", value=playlist_metadata['playlist-length'], inline=False)
                embed.add_field(name="Date of playlist creation > ", value=playlist_metadata['playlist-creation'], inline=False)
                embed.add_field(name="Privacy Setting > ", value=playlist_json["privicy"], inline=False)

            elif playlist_json["privicy"] == "server":

                if int(ctx.guild.id) in playlist_metadata['server-playlist']['playlist-guild']:

                    embed.set_author(name=f'Here is the playlist "{playlist}"')
                    embed.set_image(url=playlist_metadata['playlist-cover'])

                    embed.add_field(name=f"Author of Playlist > ", value=playlist_metadata['playlist-author-name'])
                    embed.add_field(name="Songs > ", value=playlist_json['playlist'], inline=False)
                    embed.add_field(name="Length of Playlist (Minutes) > ", value=playlist_metadata['playlist-length'], inline=False)
                    embed.add_field(name="Date of playlist creation > ", value=playlist_metadata['playlist-creation'], inline=False)
                    embed.add_field(name="Privacy Setting > ", value=playlist_json["privicy"], inline=False)



                else:
                    embed.color = RED
                    embed.set_author(name="This Playlist is server only (meaning, the playlist is whitelisted, and only selected servers can use this playlist)")

            else:
                embed.color = RED
                embed.set_author(name="This Playlist is Private.")

            try:
                embed.color = discord.Color.from_rgb(int(playlist_metadata["playlist-color"][0]), int(playlist_metadata["playlist-color"][1]), int(playlist_metadata["playlist-color"][2]))
                await ctx.send(embed=embed)
            except KeyError:
                await ctx.send(embed=embed)

    else:
        if playlistOld is None:
            name = "Most popular playlist has been deleted."
        else:
            embed.color = RED
            name = "The playlist you're looking for does not exist!"

        await sendEmbed(embed, ctx, name)

@client.command()
async def deleteplaylist(ctx, *, playlist=None):

    embed = discord.Embed(color=LIGHT_BLUE)

    tagsList = file_path+"\\tags-link.json"
    playlistPath = playlist_location+f"\\{playlist}\\{playlist}.json"

    tagsListData = return_data(tagsList)

    if playlist is None:

        embed.set_author(name="You need to chose a playlist to delete.")

        return await ctx.send(embed=embed)
    async def delete():

        playlist_data = return_data(playlistPath)
        os.remove(playlist_location+f"\\{playlist}\\{playlist}.json")
        os.rmdir(playlist_location+f"\\{playlist}")

        tagsListData["list"]["tags"].remove(playlist_data["metadata"]["playlist-id"])

        embed.set_author(name=f'Deleted Playlist: "{playlist}"')

        make_asset(file_path+"\\tags-link.json", "w", tagsListData, 4)
        return await ctx.send(embed=embed)


    p_author = return_data(playlistPath, tabel="metadata", sub_tabel="playlist-author")

    if p_author is not None:
        if ctx.author.id in p_author:

            await delete()

        else:
            embed.color = RED
            embed.set_author(name="You're not the owner of this playlist!")

            return await ctx.send(embed=embed)

    else:
        await sendEmbed(embed, ctx, f"No playlist with the name {playlist}")

@client.command()
async def usage(ctx):

    embed = discord.Embed(color=TERQ)
    args = parseArgs(ctx)

    try:
        command = args[0]

        if command == "2":

            embed.add_field(name=":eject:  More Playlist Commands' Usage  :eject:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}asong > ", value=f"{CLIENT_PREFIX}pprivacy")
            embed.add_field(name=f"{CLIENT_PREFIX}paserver > ", value=f"{CLIENT_PREFIX}paserver <Server ID> <Playlist>")
            embed.add_field(name=f"{CLIENT_PREFIX}eplaylist > ", value=f"{CLIENT_PREFIX}eplaylist <picture>, <profile>, <URL of picture>")
            embed.add_field(name=f"{CLIENT_PREFIX}playliststag > ", value=f"{CLIENT_PREFIX}playliststag <tag>")
            embed.add_field(name=f"{CLIENT_PREFIX}atag > ", value=f"{CLIENT_PREFIX}atag <playlist Name>, <tag> Note: You can only add one tag at a time, but you can add as many as you like")
            embed.add_field(name=f"{CLIENT_PREFIX}pdescription > ", value=f"{CLIENT_PREFIX}pdescription <playlist Name>, <description>")
            embed.add_field(name=f"{CLIENT_PREFIX}lyrics > ", value=f"{CLIENT_PREFIX}lyrics <Artist Name>, <Song Name> remember to seperate Artist Name and Song Name with a comma")

        else:
            raise IndexError("No Error")
    except IndexError:
        embed.set_author(name="Command Usage")

        embed.add_field(name=":soccer:  General Commands  :soccer:", value="\u200b", inline=False)
        embed.add_field(name=f"{CLIENT_PREFIX}help > ", value=f"{CLIENT_PREFIX}help")
        embed.add_field(name=f"{CLIENT_PREFIX}join > ", value=f"{CLIENT_PREFIX}join")
        embed.add_field(name=f"{CLIENT_PREFIX}disconnect", value=f"{CLIENT_PREFIX}disconnect")
        embed.add_field(name=f"{CLIENT_PREFIX}usage > ", value=f"{CLIENT_PREFIX}usage")
        embed.add_field(name=f"{CLIENT_PREFIX}this > ", value=f"{CLIENT_PREFIX}this")
        embed.add_field(name=f"{CLIENT_PREFIX}profile > ", value=f"{CLIENT_PREFIX}profile <@user>")
        embed.add_field(name=":musical_note:  Music Commands  :musical_note:", value="\u200b", inline=False)
        embed.add_field(name=f"{CLIENT_PREFIX}queue > ", value=f"{CLIENT_PREFIX}queue <YouTube Video URLs or Name>")
        embed.add_field(name=f"{CLIENT_PREFIX}play > ", value=f"{CLIENT_PREFIX}play <YouTube Video URL or Name>")
        embed.add_field(name=f"{CLIENT_PREFIX}clear > ", value=f"{CLIENT_PREFIX}clear")
        embed.add_field(name=f"{CLIENT_PREFIX}songs > ", value=f"{CLIENT_PREFIX}songs")
        embed.add_field(name=f"{CLIENT_PREFIX}resume > ", value=f"{CLIENT_PREFIX}resume")
        embed.add_field(name=f"{CLIENT_PREFIX}pause > ", value=f"{CLIENT_PREFIX}pause")
        embed.add_field(name=f"{CLIENT_PREFIX}volume > ", value=f"{CLIENT_PREFIX}volume <1-10>")
        embed.add_field(name=f"{CLIENT_PREFIX}song > ", value=f"{CLIENT_PREFIX}song")
        embed.add_field(name=f"{CLIENT_PREFIX}spotify > ", value=f"{CLIENT_PREFIX}spotify <@user>")
        embed.add_field(name=":eject:  Playlist Commands' Usage  :eject:", value="\u200b", inline=False)
        embed.add_field(name=f"{CLIENT_PREFIX}playlist > ", value=f"{CLIENT_PREFIX}playlist <Playlist Name>, <Privacy Mode (public/private)>, <YouTube Video URLs or Name, Seperate with comma>")
        embed.add_field(name=f"{CLIENT_PREFIX}playlists > ", value=f"{CLIENT_PREFIX}playlists <Playlist Name>")
        embed.add_field(name=f"{CLIENT_PREFIX}deleteplaylist > ", value=f"{CLIENT_PREFIX}deleteplaylist <Playlist Name>")
        embed.add_field(name=f"{CLIENT_PREFIX}queueplaylist > ", value=f"{CLIENT_PREFIX}queueplaylist <Playlist Name>")
        embed.add_field(name=f"{CLIENT_PREFIX}ptrust > ", value=f"{CLIENT_PREFIX}ptrust <@user> <Playlist name>")
        embed.add_field(name=f"{CLIENT_PREFIX}prtrust > ", value=f"{CLIENT_PREFIX}prtrust <@user> <Playlist name>")
        embed.add_field(name=f"{CLIENT_PREFIX}pprivacy > ", value=f"{CLIENT_PREFIX}pprivacy public or private <Playlist name>")

    finally:
        await ctx.send(embed=embed)

@client.command()
async def song(ctx):

    try:
        voice = get(client.voice_clients, guild=ctx.guild)
        embed = discord.Embed(color=MEDIUM_PURPLE)
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
async def profile(ctx, member : discord.User=None):

    """Profile Command"""

    if member is None:
        member=ctx.author
    try:

        embed = discord.Embed(color=member.color)
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

            globalData = return_data(global_profile+f"\\{ctx.author.id}\\{ctx.author.id}.json")

            def calculatePopularPlaylist():
                lengthOfPlaylists = len(globalData["global"]["playlist-list"])
                playlistList = []
                mostPopularPlaylist = [0, None]

                for x in range(0, lengthOfPlaylists):
                    playlist = globalData["global"]["listened-playlist-list"][x]
                    dictPath = globalData["global"]["playlist-list"][playlist]

                    if checkPlaylistExistance(dictPath["playlist"]):

                        if int(dictPath["play-count"]) > mostPopularPlaylist[0]:
                            mostPopularPlaylist.clear()
                            mostPopularPlaylist.append(int(dictPath["play-count"]))
                            mostPopularPlaylist.append(dictPath["playlist"])

                    else:
                        del globalData["global"]["playlist-list"][playlist]
                        globalData["global"]["listened-playlist-list"].remove(playlist)

                        make_asset(global_profile+f"\\{ctx.author.id}\\{ctx.author.id}.json", "w", globalData, 4)
                        continue

                return mostPopularPlaylist




            text = read_user.read()
            json_formatted = json.loads(text)

            user_info = json_formatted[str(user_id)]
            mostPopularPlaylist = calculatePopularPlaylist()

            if mostPopularPlaylist[1] is None:
                mostPopularPlaylist[1] = "Does not have one"

            embed.set_author(name=f'Here is "{user_info["member-name"]}" Profile', icon_url=vorbis_img)
            embed.add_field(name=f"User Name  Ø   {user_info['member-name']}", value="\u200b", inline=False)
            embed.add_field(name=f"User ID   Ø   {user_info['member-id']}", value="\u200b", inline=False)
            embed.add_field(name=f"User Join Date   Ø   {user_info['member-joindate'].split('.')[0]}", value="\u200b", inline=False)
            embed.add_field(name=f"Current User Level   Ø   {current_level}", value="\u200b", inline=False)
            embed.add_field(name=f"Current User Experience   Ø   {current_exp+1}", value="\u200b", inline=False)
            embed.add_field(name=f"Until Next Level Up   Ø   {int(until_next_levelup-current_exp-1)}", value="\u200b", inline=False)
            embed.add_field(name=f"Playlist Listened to the Most   Ø   {mostPopularPlaylist[1]}", value="\u200b", inline=False)
            embed.set_image(url=user_info['member-avatar'])

            await ctx.send(embed=embed)

    except (FileNotFoundError, commands.UserNotFound):
        embed.color = RED
        embed.set_author(name=f"No Member the name {member}")

        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member=None , *, reason=None):


    embed = discord.Embed(color=MEDIUM_PURPLE)

    if member is None:
        embed.set_author(name="You need to chose a member.")
    else:
        await member.ban(reason=reason)

        embed.set_author(name=f"Banned {member}")
        embed.add_field(name="Reason: ", value=reason)
        embed.set_thumbnail(url=vorbis_img)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member=None, *, reason=""):



    embed = discord.Embed(color=MEDIUM_PURPLE)

    if member is None:

        embed.set_author(name=f"You need to chose a member.")

    else:
        await member.send(f"You've been kicked from {ctx.guild} Reason: {reason}")
        await member.kick(reason=reason)

        embed.set_author(name=f"Kicked {member}")
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
async def server(ctx, command=None, *, args=None):

    embed = discord.Embed(color=MEDIUM_PURPLE)
    commands = ["help", "join_role", "max_warnings", "blacklist", "log_channel", "join_channel", "leave_channel", "join_message", "join_image", "leave_message", "leave_image", "whitelist"]

    if command is None:
        command = "help"

    text = f"There is no server command with the name {command}"

    data = return_data(f"{config_location}\\{ctx.guild.id}\\config.json")




    if command == commands[0]:
        text = "Server Command Help"

        embed.add_field(name="Note > ", value="This may seem complicated, but don't worry! just look at the help command")
        embed.add_field(name="join_role", value=f"{CLIENT_PREFIX}server join_role, <The role to give when a player joins>")
        embed.add_field(name="max_warnings", value=f'{CLIENT_PREFIX}server max_warnings, <1 / 10> or put it to "None" for unlimited warnings')
        embed.add_field(name="blacklist", value=f"{CLIENT_PREFIX}server blacklist, <player-ids>")
        embed.add_field(name="Example for blacklist command", value=f"Example > {CLIENT_PREFIX}server blacklist, 400089431933059072, <other player IDs>")
        embed.add_field(name="log_channel", value=f"{CLIENT_PREFIX}server log_channel, <channel_id> Sets default log channel, (IE: Blacklist notifications and level up messages)")
        embed.add_field(name="join_channel", value=f"{CLIENT_PREFIX}server join_channel, <channel_id> Sets join log messages (IE: When a player joins, the message of the joining player will be sent to that channel)")
        embed.add_field(name="leave_channel", value=f"{CLIENT_PREFIX}server leave_channel, <channel_id> Sets leave log messages (IE: When a player leaves, the message of the leaving player will be sent to the specified channel)")
        embed.add_field(name="join_message", value=f"{CLIENT_PREFIX}server join_message, <message> The message that will be sent to the specifed join channel")
        embed.add_field(name="join_image", value=f"{CLIENT_PREFIX}server join_image, <url> The image that will be sent to the specified join channel upon a members joining to the server")
        embed.add_field(name="leave_image", value=f"{CLIENT_PREFIX}server leave_image, <url> The image that will be sent to the specified leave channel upon a members departure from the server")
        embed.add_field(name="whitelist", value=f"{CLIENT_PREFIX}server whitelist, on | off Will turn on | off whitelist ")

    elif command == commands[1]:
        text = f"I have set the join role to {args}"
        data["config"][f"{command}"] = args

    elif command == commands[2]:
        text = f"I have set the Max Warnings to {args}"
        data["config"][f"{command}"] = args

    elif command == commands[3]:
        text = f"Blacklisted player IDs > {args}"
        data["config"][f"{command}"] = args.split(", ")

    elif command == commands[4]:
        channel = client.get_guild(ctx.guild.id).get_channel(int(args))
        text = f"I've set the log channel to {channel}"

        data["config"][f"{command}"] = int(args)

    elif command == commands[5]:
        channel = client.get_guild(ctx.guild.id).get_channel(int(args))
        text = "I've set the Join channel to {channel}"

        data["config"][f"{command}"] = int(args)

    elif command == commands[6]:
        channel = client.get_guild(ctx.guild.id).get_channel(int(args))
        text = "I've set the Leave channel to {channel}"

        data["config"][f"{command}"] = int(args)

    elif command == commands[7]:
        text = f"New join message > {args}"
        data["config"][f"{command}"] = args

    elif command == commands[8]:

        if image(args):
            text = "I've set the new join image"
            embed.set_image(url=args)

            data["config"][f"{command}"] = args
        else:
            text = "This is not a valid URL"

    elif command == commands[9]:

        text = f"New leave message > {args}"
        data["config"][f"{command}"] = args

    elif command == commands[10]:

        if image(args):
            text = "I've set the new leave image"
            embed.set_image(url=args)

            data["config"][f"{command}"] = args
        else:
            text = "This is not a valid URL"

    elif command == commands[11]:
        text = f"Whitelisted player IDs > {args}"
        data["config"][f"{command}"] = args.split(", ")

    make_asset(f"{config_location}\\{ctx.guild.id}\\config.json", "w", data, 4)



    embed.set_author(name=text)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def warn(ctx, player : discord.Member, *, reason : str=None):
    try:
        path = f"{user_location}\\{ctx.guild.id}\\{player.id}\\{player.id}-warnings.json"
        config_path = f"{config_location}\\{ctx.guild.id}\\config.json"

        data = {}
        embed = discord.Embed(color=RED)

        warnings = 0
        max_warnings = 0
        splited_reason = reason.split(" ")

        mode = splited_reason[0]
        w_reason = []
        f_reason = None

        for x in range(1, len(splited_reason)):
            w_reason.append(splited_reason[x])
            f_reason = filt_str(str(w_reason))

        if mode == "remove":
            return await ctx.send(f_reason)

        try:
            warnings = int(return_data(file=path, tabel="setting1", sub_tabel="warnings"))
            max_warnings = return_data(file=config_path, tabel="main", sub_tabel="warnings")
            new_warning_count = warnings+1

        except FileNotFoundError:

            data["setting1"] = ({
                "warnings": 1
                })
            make_asset(file=path, mode="w+", data=data, indention=4)



        if max_warnings is type(int) and new_warning_count >= max_warnings:
            await player.send(f"You've been banned for reaching max warnings in the server")
            await player.ban(reason="Max Warnings Reached")
            embed.set_author(name=f"Banned {player.name} for reaching max warnings")
        else:
            data["setting1"] = ({
                "warning_entry": [{
                    "count": new_warning_count,
                    "reason": reason
                    }]
                })

            make_asset(file=path, mode="w+", data=data, indention=4)

            embed.set_author(name=f"Warned {player.name}, Warn Count: {new_warning_count}")


            await ctx.send(embed=embed)
    except AttributeError:
        await ctx.send

@client.command()
@commands.has_permissions(administrator=True)
async def leave(ctx):
    await ctx.send("Leaving Server...")
    guild = client.get_guild(ctx.guild.id)

    await guild.leave()

@client.command()
async def adminhelp(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)

    embed.set_author(name="Administrator Help")

    embed.add_field(name=f"{CLIENT_PREFIX}kick", value="Kicks Selected Player")
    embed.add_field(name=f"{CLIENT_PREFIX}ban", value="Bans Selected Player")
    embed.add_field(name=f"{CLIENT_PREFIX}leave", value="Bot will leave the server")
    embed.add_field(name=f"{CLIENT_PREFIX}warn", value="Warns selected Player")
    embed.add_field(name=f"{CLIENT_PREFIX}server", value="Server configurations")
    embed.add_field(name=f"{CLIENT_PREFIX}purge", value="Purges a channel by a selected amount of messages")
    embed.add_field(name=f"{CLIENT_PREFIX}unban", value="Unbans selected Player")

    await ctx.send(embed=embed)

@client.command()
async def this(ctx):


    embed = discord.Embed(color=MEDIUM_PURPLE)
    guild = ctx.guild

    embed.set_author(name=f"{guild}")
    embed.add_field(name="Server made at: ", value=str(guild.created_at).split(".")[0])
    embed.add_field(name="Level: ", value=guild.premium_tier, inline=False)
    embed.add_field(name="ID: ", value=guild.id, inline=False)
    embed.add_field(name="Member Count: ", value=guild.member_count, inline=False)
    embed.add_field(name="Region: ", value=guild.region, inline=False)
    embed.add_field(name="Bitrate Limit: ", value=guild.bitrate_limit, inline=False)
    embed.add_field(name="Owner: ", value=guild.owner, inline=False)
    embed.add_field(name="Latency: ", value=client.latency, inline=False)

    if guild.description is None:
        embed.set_footer(text="No guild Description Provided.")
    else:
        embed.set_footer(text=guild.description)

    embed.set_image(url=guild.icon_url)

    await ctx.send(embed=embed)

@client.command()
async def spotify(ctx, member : discord.Member=None):

    member_id = None


    if member is None:
        member_id = ctx.author.id
    else:
        member_id = member.id

    guild = client.get_guild(ctx.guild.id)
    user = guild.get_member(member_id)
    embed = discord.Embed(color=user.color)

    title = None
    artist = None
    album_url = None
    duration = None

    for activity in user.activities:
        if isinstance(activity, Spotify):
            title = str(activity.title)
            artist = str(activity.artist)
            album_url = str(activity.album_cover_url)
            duration = str(activity.duration).split(".")[0]
            track_id = str(activity.track_id).split(".")

    if title is None:
        if member is None:
            embed.set_author(name=f"You're not playing any song")
        else:
            embed.set_author(name=f"{user} is not playing any song")

        return await ctx.send(embed=embed)



    embed.set_author(name=f"{user} Spotify", icon_url=user.avatar_url)

    embed.add_field(name=f"{user} is playing   Ø   {title}", value="\u200b")
    embed.add_field(name=f"By   Ø   {artist}", value="\u200b", inline=False)
    embed.add_field(name=f"Song Duration   Ø   {duration}", value="\u200b", inline=False)
    embed.set_footer(text=f"Track ID   Ø   {track_id[0]}")

    embed.set_image(url=album_url)


    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def broadcast(ctx, g_id, *, message):

    guild = client.get_guild(int(g_id))
    channel = guild.get_channel(guild.system_channel.id)

    await channel.send(f"{message}")

@client.command()
async def ptrust(ctx, user : discord.Member=None, *, playlist_name=None):

    embed = discord.Embed(color=LIGHT_BLUE)

    if user is None and playlist_name is None:
        embed.set_author(name="Both Values are empty.")

        return await ctx.send(embed=embed)
    elif user is None:
        embed.set_author(name="No user was selected.")

        return await ctx.send(embed=embed)
    elif playlist_name is None:

        embed.set_author(name="No playlist selected.")

        return await ctx.send(embed=embed)
    else:

        full_path = f"{playlist_location}\\{playlist_name}\\{playlist_name}.json"
        playlist_data = return_data(full_path)
        owner_id = playlist_data["metadata"]["playlist-author"]

        if owner_id[0] == int(ctx.author.id):
            owner_id.append(int(user.id))

            make_asset(file=full_path, mode="w", data=playlist_data, indention=4)
            embed.set_author(name=f"{user} is now trusted")
        else:
            embed.set_author(name=f"You're not allowed to trust other people (Even if you're trusted, only owner of the playlist can do this)")
        await ctx.send(embed=embed)

@client.command()
async def prtrust(ctx, user : discord.Member=None, *, playlist_name=None):

    embed = discord.Embed(color=LIGHT_BLUE)

    if user is None and playlist_name is None:
        embed.set_author(name="Both Values are empty.")

        return await ctx.send(embed=embed)
    elif user is None:
        embed.set_author(name="No user was selected.")

        return await ctx.send(embed=embed)
    elif playlist_name is None:

        embed.set_author(name="No playlist selected.")

        return await ctx.send(embed=embed)
    else:

        full_path = f"{playlist_location}\\{playlist_name}\\{playlist_name}.json"

        playlist_data = return_data(full_path)
        owner_id = playlist_data["metadata"]["playlist-author"]

        if owner_id[0] != int(ctx.author.id):
            embed.set_author(name="You're not the owner of this playlist.")

            return await ctx.send(embed=embed)
        else:
            if os.path.isdir(f"{playlist_location}\\{playlist_name}") != True:
                embed.set_author(name=f'No playlist with the name "{playlist_name}"')
                await ctx.send(embed=embed)
            else:
                try:
                    if owner_id[0] == int(ctx.author.id) and owner_id[0] == int(user.id):
                        embed.color = RED
                        embed.set_author(name="You cannot remove yourself from your own playlist.")

                    elif owner_id[0] == int(user.id):
                        embed.color = RED
                        embed.set_author(name="You cannot remove owners' trust permissions.")

                    else:
                        owner_id.remove(int(user.id))
                        make_asset(file=full_path, mode="w", data=playlist_data, indention=4)

                        embed.set_author(name=f"{user} is no longer trusted.")

                    await ctx.send(embed=embed)

                except ValueError:
                    embed.set_author(name=f"{user} is already not trusted.")

                    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def owner_leave(ctx, server_id : int):

    guild = client.get_guild(server_id)

    print(f"Leaving {guild}")

    try:
        await guild.get_channel(guild.system_channel.id).send(f"I am leaving this server, upon owners asking. Do not try to invite me to this server again.\n\nDEBUG>>{guild.id}")
        await guild.leave()
    except AttributeError:

        await ctx.send("The guild you tried to make the bot leave is no longer existing.")

@client.command()
async def pprivacy(ctx, setting=None, *, playlist_name=None):

    done = False
    done1 = False

    embed = discord.Embed(color=LIGHT_BLUE)

    if setting is None or playlist_name is None:

        await ctx.send("What privacy setting do you want? (public or private)")
        while done is False:

            setting = await client.wait_for('message')

            print(setting)

            if setting.guild.id == ctx.guild.id and setting.channel.id == ctx.channel.id and setting.author.id == ctx.author.id:
                if setting.content == "private" or setting.content == "public":

                    setting = setting.content

                    await ctx.send("What playlist do you want to change the privacy setting?")

                    while done1 is False:

                        playlist_name = await client.wait_for('message')

                        if playlist_name.guild.id == ctx.guild.id and playlist_name.channel.id == ctx.channel.id and playlist_name.author.id == ctx.author.id:

                            playlist_name = playlist_name.content

                            done1 = True
                            done = True

                        else:
                            pass
                else:
                    return await ctx.send(f'"{setting.content}" is not a privacy setting.')
            else:
                pass

    full_path = f"{playlist_location}\\{playlist_name}\\{playlist_name}.json"

    try:
        playlist_data = return_data(f"{full_path}")

        playlist_data["info"]["privicy"] = setting

        if playlist_data["metadata"]["playlist-author"][0] != int(ctx.author.id):

            embed.set_author(name="You're not the owner of this playlist")

        else:
            make_asset(file=full_path, mode="w", data=playlist_data, indention=4)
            embed.set_author(name=f"Changed privacy setting to {setting}")

        await ctx.send(embed=embed)

    except TypeError:

        await ctx.send(f'Playlist: "{playlist_name}" not found.')

@client.command()
async def asong(ctx, songs=None, playlist_name=None):

    done = False
    done1 = False

    embed = discord.Embed(color=LIGHT_BLUE)
    song_list = []

    if songs is None or playlist_name is None:
        await ctx.send("What songs do you want to add? (Please seperate songs with a comma)")
        while done is False:

            new_songs = await client.wait_for('message')

            if check_channel(new_songs.guild.id, ctx.guild.id, new_songs.channel.id, ctx.channel.id, new_songs.author.id, ctx.author.id):

                songs = new_songs.content

                await ctx.send("What playlist are you chosing?")
                while done1 is False:

                    playlist_name = await client.wait_for('message')

                    if check_channel(playlist_name.guild.id, ctx.guild.id, playlist_name.channel.id, ctx.channel.id, playlist_name.author.id, ctx.author.id):
                        playlist_name = playlist_name.content

                        done1 = True
                        done = True
                    else:
                        pass
            else:
                pass

    song_data_old = return_data(file=f"{playlist_location}\\{playlist_name}\\{playlist_name}.json", tabel="info", sub_tabel="playlist")
    song_data_full = return_data(file=f"{playlist_location}\\{playlist_name}\\{playlist_name}.json")

    if song_data_old is None:
        embed.set_author(name=f'No playlist with the name "{playlist_name}"')
    else:
        if check_owner(playlist=playlist_name, owner_id=ctx.author.id):

            song_list.append(song_data_old)
            song_list.append(songs)

            full_songs = ", ".join(song_list)

            song_data_full["info"]["playlist"] = full_songs
            make_asset(file=f"{playlist_location}\\{playlist_name}\\{playlist_name}.json", mode="w", data=song_data_full, indention=4)

            embed.set_author(name=f'I have Added Ø "{songs}" to {playlist_name}')
        else:
            embed.set_author(name=f"You're not the owner of this playlist.")

    await ctx.send(embed=embed)

@client.command()
async def paserver(ctx, guild_id=None, playlist_name=None):

    embed = discord.Embed(color=LIGHT_BLUE)

    done = False
    done1 = False

    if guild_id is None or playlist_name is None:
        try:
            await ctx.send("What server do you want to the whitelist? (NOTE: Please use Guild IDs, NOT names, This can cause fatal errors in the system.)")

            while done is False:

                message = await client.wait_for('message')

                if check_channel(message.guild.id, ctx.guild.id, message.channel.id, ctx.channel.id, message.author.id, ctx.author.id):

                    guild_id = int(message.content)

                    if client.get_guild(guild_id) is not None:

                        await ctx.send("What playlist do you want to whitelist?")

                        while done1 is False:

                            message = await client.wait_for('message')

                            if check_channel(message.guild.id, ctx.guild.id, message.channel.id, ctx.channel.id, message.author.id, ctx.author.id):

                                playlist_name = message.content

                                done1 = True
                                done = True

                            else:
                                pass
                    else:
                        embed.set_author(name="Server not Found.")

                        return await ctx.send(embed=embed)
                else:
                    pass
        except ValueError:
            embed.set_author(name="Invalid Guild ID (ValueError)")

            return await ctx.send(embed=embed)
    guild = client.get_guild(int(guild_id))
    full_path = f"{playlist_location}\\{playlist_name}\\{playlist_name}.json"

    if check_owner(playlist_name, ctx.author.id):
        try:

            embed.set_author(name=f"Added {guild} to the playlist whitelist")
            playlist_data = return_data(file=full_path)
            print(playlist_data['metadata']['server-playlist']['playlist-guild'])
            playlist_data['metadata']['server-playlist']['playlist-guild'].append(int(guild_id))

            make_asset(full_path, "w", playlist_data, 4)
        except KeyError:
            embed.set_author(name=f"This playlist is not server-selected.")
    else:
        embed.set_author(name="You're not the owner of this playlist.")

    await ctx.send(embed=embed)

@client.command()
async def prname(ctx):
    embed = discord.Embed(color=LIGHT_BLUE)

    try:

        args = str(ctx.message.content).split("/prname ")
        args = args[1].split(", ")


        try:

            new_name = args[0]
            playlist = args[1]

            playlist_path = f"{playlist_location}\\{playlist}\\{playlist}.json"
            new_path = f"{playlist_location}\\{new_name}\\{new_name}.json"

            try:

                if os.path.isfile(new_path):
                    raise FileExistsError(".")
                else:
                    os.rename(playlist_path, f"{playlist_location}\\{playlist}\\{new_name}.json")
                    os.rename(f"{playlist_location}\\{playlist}", f"{playlist_location}\\{new_name}")

                    embed.set_author(name=f"Changed {playlist} to {new_name}")

            except FileExistsError:
                embed.set_author(name=f'There is already a playlist with the name "{new_name}"')

        except FileNotFoundError:
            embed.set_author(name=f'No playlist with the name "{playlist}"')

    except IndexError:
        embed.set_author(name="Missing Parameters (/prname <New Playlist name>, <Playlist Name>) Remember to add comma between Arguments")

    await ctx.send(embed=embed)

@client.command()
async def rsong(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)
    playlist_name = None

    try:
        content = parseArgs(ctx)
        try:
            playlist_name = content[0]

            songs = content[1]
            location = f"{playlist_location}\\{playlist_name}\\{playlist_name}.json"
            song = None

            data = return_data(file=location)
            song_list = data["info"]["playlist"]

            songListSplited = song_list.split(", ")
            data["info"]["playlist"] = songListSplited

            try:

                if check_owner(playlist_name, ctx.author.id):
                    try:
                        if type(songs) == str:
                            song = songs
                            songListSplited.remove(songs)

                    except ValueError:
                        song = songListSplited.pop(int(songs))
                        songListSplited.pop(int(songs))
                    finally:
                        data["info"]["playlist"] = filt_str_mod(str(data["info"]["playlist"]))
                        make_asset(location, "w", data, 4)

                        embed.set_author(name=f"Removed {song}")
                else:
                    raise commands.errors.NotOwner("User is not the owner of this playlist.")

            except commands.errors.NotOwner:
                await sendEmbed(embed, ctx, f"You're not the owner of this playlist.")
        except IndexError:
            await sendEmbed(embed, ctx, "Missing Arguments (/rsong <Playlist Name>, <Song> Remember to add a comma between the Playlist Name and The song)")
    except FileNotFoundError:
        await sendEmbed(embed, ctx, f"No playlist with the name {playlist_name}")

@client.command(aliases=["at"])
async def atag(ctx):

    args = parseArgs(ctx)
    embed = discord.Embed(color=LIGHT_BLUE)
    text = None

    playlistName = args[0]
    playlistTags = args[1]

    if checkPlaylistExistance(playlistName):
        path = f"{playlist_location}\\{playlistName}\\{playlistName}.json"
        if checkPlaylistPrivacy(playlistName) or check_owner(playlistName, ctx.author.id):
            playlistData = return_data(path)

            playlistData["metadata"]["tags"].append(playlistTags)
            make_asset(path, "w", playlistData, 4)

            text = f'Appened "{playlistTags}" onto "{playlistName}"'
        else:
            text = "You're not the owner of this playlist."
    else:
        text = "The playlist you're looking for does not exist."

    await sendEmbed(embed, ctx, text)

@client.command(aliases=["pt"])
async def playliststag(ctx, *, tag):

    tegsReturn = findPlaylistTags(tag)
    embed = discord.Embed(color=LIGHT_BLUE)

    if len(tegsReturn) <= 0:
        embed.set_author(name="Ø No playlists matching that tag.")
    else:
        embed.set_author(name="Ø Here are some playlists matching that tag")

        for x in range(5):
            try:
                playlistName = tegsReturn[x]
                embed.add_field(name=f"{x+1}   Ø   {getPlaylistInfo(playlistName).playlistname()}", value=f"Songs   Ø   {getPlaylistInfo(playlistName).playlistsongcontents()}", inline=False)
            except IndexError:
                break

    await ctx.send(embed=embed)

@client.command()
async def eplaylist(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)
    args = parseArgs(ctx, "url")
    commandList = ["picture", "color", "description", "help"]

    try:
        command, playlistName = args[0], args[1]
        path = f"{playlist_location}\\{playlistName}\\{playlistName}.json"

        if command in commandList:
            if checkPlaylistExistance(playlistName):
                if check_owner(playlistName, ctx.author.id):

                    if command == commandList[0]:
                        newPicture = args[2]
                        playlistData = getPlaylistInfo(playlistName).rawplaylist()

                        if image(newPicture):
                            playlistData["metadata"]["playlist-cover"] = newPicture
                            make_asset(path, "w", playlistData, 4)
                            embed.set_author(name=f"New Playlist image set")

                        else:
                            embed.set_author(name="This is not an image URL.")

                    elif command == commandList[1]:
                        playlistData = return_data(path)
                        if len(args) >= 4:

                            playlistData["metadata"]["playlist-color"] = []
                            playlistData["metadata"]["playlist-color"].append(args[2])
                            playlistData["metadata"]["playlist-color"].append(args[3])
                            playlistData["metadata"]["playlist-color"].append(args[4])

                            embed.color = discord.Color.from_rgb(int(args[2]), int(args[3]), int(args[4]))
                            embed.set_author(name="Example of your new colour (Note: I have set this as your playlist colour)")

                            make_asset(path, "w", playlistData, 4)
                        elif len(args) == 3:

                            if args[2] in colour_opts:
                                playlistData["metadata"]["playlist-color"] = colour_opts[args[2]]

                                make_asset(path, "w", playlistData, 4)

                                embed.set_author(name=f"I've changed your playlist colour to {args[2]}")
                            else:
                                embed.set_author(name="Colour not Found")



                    elif command == commandList[2]:

                        playlistData = return_data(path)
                        description = args[2]

                        playlistData["metadata"]["playlist-description"] = description
                        embed.set_author(name="I have set the playlist description (I am not going to preview it incase the description is too big, that can cause some programming issues.)")
                        make_asset(path, "w", playlistData, 4)

                    elif command == commandList[3]:

                        embed.set_author(name="Editing Playlist Help")
                        embed.add_field(name="To edit your playlist description, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist description, <Your playlist name>, <Your description>", inline=False)
                        embed.add_field(name="To edit your playlist Image, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist picture, <Your playlist name>, <Image URL>", inline=False)
                        embed.add_field(name="To edit your playlist colour, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist color, <Your playlist name>, <Color>", inline=False)
                        embed.set_footer(text="Note Ø Here is a list of colours, > blue, red, yellow, green, white, light blue, I will add more as time goes on, and you can can add your own colours by using RGB Values, like 0, 128, 255 for a light blue.")


                    else:
                        pass
                else:
                    embed.set_author(name="You're not the author of this playlist")
            else:
                embed.set_author(name="That playlist does not exist")
        else:
            embed.set_author(name=f'"{command}" is not an editable attribute')

    except IndexError:
        embed.set_author(name="Editing Playlist Help")
        embed.add_field(name="To edit your playlist description, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist description, <Your playlist name>, <Your description>", inline=False)
        embed.add_field(name="To edit your playlist Image, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist picture, <Your playlist name>, <Image URL>", inline=False)
        embed.add_field(name="To edit your playlist colour, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist color, <Your playlist name>, <Color>", inline=False)
        embed.set_footer(text="Note Ø Here is a list of colours, > blue, red, yellow, green, I will add more as time goes on, and you can can add your own colours by using RGB Values, like 0, 128, 255 for a light blue.")

    finally:
        await ctx.send(embed=embed)

@client.command()
async def link(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)
    args = parseArgs(ctx)

    try:
        if len(args) >= 1:

            command = args[0]
            authorID = ctx.author.id
            linkLocation = f"{user_location}\\{ctx.guild.id}\\{authorID}\\{authorID}-links.json"

            if command == "make":
                try:
                    linkedServers = args[1]
                    guildPath = f"{guild_location}\\{linkedServers}\\{linkedServers}-LINKS.json"

                    userGlobalPath = f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json"
                    globalData = return_data(userGlobalPath)

                    guildLinkData = return_data(guildPath)
                    memberData = return_data(linkLocation)

                    if memberData["member-link"]["link-enabled"] != True:
                        embed.set_author(name=f'Link is not enabled. To enable it, do this command "{CLIENT_PREFIX}link link, True"')
                    else:

                        if globalData["global"]["has-link"] is True:
                            embed.set_author(name="You already have a link.")
                        else:
                            memberData["member-link"]["links"].append(linkedServers)
                            memberData["member-link"]["links"].append(f"{ctx.guild.id}")
                            globalData["global"]["has-link"] = True
                            globalData["global"]["link-id"] = str(linkedServers)


                            guildLinkData["guild-links"][f"{ctx.author.id}"] = []
                            guildLinkData["guild-links"][f"{ctx.author.id}"].append(f"{ctx.author.id}")
                            guildLinkData["guild-links"][f"{ctx.author.id}"].append(f"{ctx.guild.id}")


                            make_asset(linkLocation, "w", memberData, 4)
                            make_asset(guildPath, "w", guildLinkData, 4)
                            make_asset(userGlobalPath, "w", globalData, 4)

                            print(return_data(guildPath))

                            embed.set_author(name=f"Added '{linkedServers}' to your link")
                except Exception as e:
                    embed.set_author(name=f"Foreign Error Ø {e}")
            elif command == "link":

                value = args[1]

                actualValue = (value == "True")
                memberData = return_data(linkLocation)

                memberData["member-link"]["link-enabled"] = actualValue
                embed.set_author(name=f"Link is now {actualValue} (Note: if you put anything other than True or False, it will default to False.)")

                make_asset(linkLocation, "w", memberData, 4)

            elif command == "remove":
                try:

                    globalUserData = return_data(global_profile+f"\\{ctx.author.id}\\{ctx.author.id}.json")

                    if globalUserData["global"]["has-link"] is True:
                        guildID = globalUserData["global"]["link-id"]
                        globalUserData["global"]["has-link"] = False

                        guildPath = f"{guild_location}\\{guildID}\\{guildID}-LINKS.json"
                        guild = client.get_guild(int(guildID))
                        linkLocation = f"{user_location}\\{guildID}\\{ctx.author.id}\\{ctx.author.id}-links.json"

                        userData = return_data(linkLocation)
                        serverData = return_data(guildPath)

                        userData["member-link"]["links"].clear()
                        del serverData["guild-links"][str(ctx.author.id)]

                        make_asset(linkLocation, "w", userData, 4)
                        make_asset(guildPath, "w", serverData, 4)
                        make_asset(global_profile+f"\\{ctx.author.id}\\{ctx.author.id}.json", "w", globalUserData, 4)

                        embed.set_author(name=f"I have severed your link from {guild}, You will now start levelling up independently on both servers")
                    else:
                        raise IndexError(".")
                except IndexError:
                    embed.set_author(name=f"You have no links")



            else:
                embed.set_author(name=f"{command} is not a link attribute")
        else:
            raise IndexError
    except AttributeError as e:
        embed.set_author(name=f"Missing Arguments, Actual Console Error>{e}")

    finally:
        await ctx.send(embed=embed)

@client.command()
async def lyrics(ctx):
    try:
        try:
            args = parseArgs(ctx)
            await ctx.send(f"Searching for: {args[1]}\n\nBy: {args[0]}")
            artist = genius.search_song(args[1], args[0])

            await ctx.send(artist.lyrics)
        except IndexError:
            await ctx.send("Missing Arguments")
    except discord.errors.HTTPException:
        try:
            lyrics = str(artist.lyrics)
            half1, half2 = lyrics[:len(lyrics)//2],lyrics[len(lyrics)//2:]

            await ctx.send(half1)
            await ctx.send(half2)
            await ctx.send("\n\nNOTE: I had to split the song lyrics in half, due to discords 2000 character limit, so the lyrics have been sent in two messages.")

        except Exception as e:
            await ctx.send(f"EXCEPTION >>> {e}\n\nThis error is a un-caught Error, this probably a song that is too big to split in\ntwo messages, so discord threw this error, I didn't know a song that was over\n4000 Characters so I could not test the code properly lmao ")
for filename in os.listdir(cog_location):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')

client.run(TOKEN)
