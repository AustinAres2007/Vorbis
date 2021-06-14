"""Made by: Austin Ares, Fabian Kuzbiel, Elina"""


import discord, time, os, shutil, youtube_dl, youtubesearchpython, json, datetime, random, logging, asyncio, lyricsgenius, threading, pyautogui, mouse, urllib, requests

from discord.ext import commands, tasks
from discord.utils import get
from discord import Spotify
from PIL import Image, ImageFont, ImageDraw

TOKEN = None
CLIENT_ID = None
CLIENT_SECRET = None
GENIUS_ID = None
GENIUS_SECRET = None
GENIUS_ACCESS_TOKEN = None
MAIN_GUILD = None
RST_CNT = 0

"""Location Variables"""

global file_path, music_location, ydl_opts, res_location, config_location, playlist_location, metadata_location

file_path = os.path.dirname(os.path.realpath(__file__))
vorbis_img = "https://cdn.discordapp.com/attachments/800136030228316170/802961405296902154/icon2.jpg"
vorbis_img2 = "https://cdn.discordapp.com/attachments/800136030228316170/833278727327842314/image0.jpg"

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.reactions = True
intents.messages = True

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
chatroom_location = file_path+"\\Chatrooms"
system_location = file_path+"\\System"
asset_location = file_path+"\\Assets"
gotham_font_location = "C:\\Users\\Default\\Documents\\Fonts\\Gotham-Font\\"

"""Logger parameters"""

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="System\\vorbis_info.log", encoding='utf-8', mode="w")
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

def return_data(file : str, tabel : str=None, sub_tabel : str=None, ty : str=None):
    try:
        if tabel is None:
            with open(file) as data:

                RwText_Data = data.read()


                if ty == "text":
                    return RwText_Data
                else:
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

def getUserArgs(ctx, args):


    if args.channel.id == ctx.channel.id and args.guild.id == ctx.guild.id and args.author.id == ctx.author.id:
        return args.content
    else:
        return None


def recomendPlaylistTimer():


    RST_CNT = 0
    highestValue = 0
    listOfPlaylists = {}
    nameList = []
    recommendedPlaylist = {}
    recommendedPlaylist['src'] = {}

    clock = return_data(f"{system_location}\\playlist-clock.json")

    while True:

        if RST_CNT <= clock["setting"]["last-update"] and RST_CNT >= clock["setting"]["last-update"]-1:
            RST_CNT = RST_CNT+1

            data = {}
            data["setting"] = {
                "last-update": RST_CNT,
                "time": str(datetime.datetime.now())
            }

            make_asset(f"{system_location}\\playlist-clock.json", "w", data, 4)
        else:
            print("TimerError")
            break

        curnt_time = str(datetime.datetime.now())


        print(f"Count: {RST_CNT} Playlist timer update at: {curnt_time.split('.')[0]}")

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
                recommendedPlaylist["src"]["time"] = curnt_time.split('.')[0]

                make_asset(f"{system_location}\\recommendedPlaylist.json", "w", recommendedPlaylist, 4)


            else:
                pass

        time.sleep(3600)

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
                    if int(playlistData["metadata"]["queue-count"]) > int(maxInt[0]) and int(playlistData["metadata"]["queue-count"]) > int(maxInt[1]):
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

def getSongMetaData(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice is not None and voice.is_connected() and voice.is_playing():
        metadata = return_data(metadata_location+f"\\{ctx.guild.id}\\metadata.json")
        return metadata
    else:
        return "None"

def replaceSpaces(string : str=None):

    if string is not None:
        stringSplit = string.split(" ")
        e = []

        for x in range(len(stringSplit)):
            e.append(stringSplit[x])

            string = "-".join(e)

        return string
    else:
        return None

def get_user_asset(ctx : discord.Message, type : str):

    user_types = ["GlobalProfiles", "Members"]

    if type in user_types:
        if type == "GlobalProfiles":
            path = f"{user_types[0]}\\{ctx.author.id}\\{ctx.author.id}.json"
        elif type == "Members":
            path = f"{user_types[1]}\\{ctx.guild.id}\\{ctx.author.id}\\{ctx.author.id}.json"

        data = return_data(path)

        return data

    else:
        raise AttributeError(f"No user_type: {type}")

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
client = commands.AutoShardedBot(shard_count=2, command_prefix=CLIENT_PREFIX, case_insenstive=True, guild_subscriptions=True, intents=intents)

"""Embed Colours"""

WHITE = discord.Color.from_rgb(255, 255, 255)
TERQ = discord.Color.from_rgb(49,171,159)
RED = discord.Color.from_rgb(255, 0, 0)
YELLOW = discord.Color.from_rgb(255, 255, 0)
LIGHT_BLUE = discord.Color.from_rgb(0,128,255)
MEDIUM_PURPLE = discord.Color.from_rgb(147, 112, 219)
GOLD = discord.Color.from_rgb(207,181,59)
AZURE = discord.Color.from_rgb(155, 155, 255)

AZURE_T = (155, 155, 255)
WHITE_T = (255, 255, 255)
MED_PURPLE_T = (147, 112, 219)
LIGHT_BLUE_T = (0,128,255)
RED_T = (255, 0, 0)
"""Bot Code"""

@client.remove_command("help")
@client.event
async def on_ready():


    curnt_time = str(datetime.datetime.now())
    print(f"Version 1.2\nVorbis is Online\n\nStartup/Refresh at: {curnt_time.split('.')[0]}")

    await client.change_presence(status=discord.Status.online, activity=discord.Game(f'{CLIENT_PREFIX}help'))

    data = {}

    data["setting"] = {
        "last-update": 0,
        "time": None
    }

    make_asset(f"{system_location}\\playlist-clock.json", "w", data, 4)
    threading.Thread(target=recomendPlaylistTimer).start()

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
            embed.add_field(name=f"{CLIENT_PREFIX}loop", value=f"Will turn on / off song looping depending on what it's currently on.")
            embed.add_field(name=f":moneybag: Economy Commands :moneybag:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}buy", value=f"Will buy an item, as of now, you can only buy rolls, but I plan to expand this. The item has to be in the shop, and you have to be able to afford it, (Note: To look at your own balance, do {CLIENT_PREFIX}profile")
            embed.add_field(name=f"{CLIENT_PREFIX}shop", value=f"Will show what items are available in the shop, items in the shops are added by administrators, to buy something, you need money, you can earn money by talking in chat. (Note: This economy system is not accurate to in-real-life scenarios, and is in dollars)")
            embed.add_field(name=f":pick: More General Commands :pick:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}ah", value=f"Administration Commands, if you are a normal player, do not do this command (Note: Nothing will happen)")
            embed.add_field(name=f"{CLIENT_PREFIX}credit", value=f"Credits, Shows updated credits of who made Vorbis (Note: 3 People, Austin, Fabian, Elina)")
            embed.add_field(name=f"{CLIENT_PREFIX}sendfeedback", value=f"Sends feedback to the Vorbis testing server, any feedback is highly valued. (Note: Please include problems with the bot, not just random stuff)")
            embed.add_field(name=f"{CLIENT_PREFIX}comment", value=f"Comments on a playlist (Note: to comment on a playlist, you must have queued that playlist first, with {CLIENT_PREFIX}queueplaylist)")
            embed.add_field(name=f"{CLIENT_PREFIX}read", value=f"Will read comments from a selected playlist. (Note: It will pick random messages, but you can read a certain message if you know the ID)")
            embed.add_field(name=f"{CLIENT_PREFIX}delete", value=f"Will delete a selected comment from a selected playlist. (Note: you cannot delete other peoples comments, and you cannot reverse the deletion of a comment)")
            embed.add_field(name=f"{CLIENT_PREFIX}image", value=f"WIll send an image of your User Profile.")

            embed.set_footer(text=f"Do {CLIENT_PREFIX}help or {CLIENT_PREFIX}help 3 for more commands")
            return await ctx.send(embed=embed)

        elif int(arg) == 3:
            embed.set_author(name="≥ Commands 3")
            embed.add_field(name=f":speech_left: Communication Commands :speech_left:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}chatroom", value=f"Will make a chatroom (You can edit aspects of the chatroom afterwards with {CLIENT_PREFIX}edit)")
            embed.add_field(name=f"{CLIENT_PREFIX}connect", value=f"Will connect to a chatroom (You'll need the chatroom ID and password to do this)")
            embed.add_field(name=f"{CLIENT_PREFIX}chat", value=f"Will send a message to the chatroom you're currently in (Note: Do {CLIENT_PREFIX}connect to connect to one)")
            embed.add_field(name=f"{CLIENT_PREFIX}leave", value=f"Will leave the chatroom you're currently in (Note: If the chatroom is private, but you're whitelisted, you'll be able to join back)")
            embed.add_field(name=f"{CLIENT_PREFIX}pull", value=f"Pulls a chatroom from the server (Note: You have to be the owner of the chatroom, and you need to be connected to it, you need the chatroom password, and you cannot undo this command)")
            embed.add_field(name=f"{CLIENT_PREFIX}edit", value=f"Edits Aspects of your chatroom (Note: You have to be connected to it, and you need to be the owner)")
            embed.add_field(name=f"{CLIENT_PREFIX}room", value=f"Shows infomation about the chatroom you're currently in (Note: You need to be connected, if you leave, you will not be able to access this infomation)")
            embed.add_field(name=f"{CLIENT_PREFIX}boot", value=f"Will kick a player from the chatroom you're in (You have to be the owner of the chatroom to do this command)")
            embed.add_field(name=f"{CLIENT_PREFIX}exile", value=f"Will ban a player from the chatroom you're in (You have to be the owner of the chatroom to do this command)")
            embed.add_field(name=f"{CLIENT_PREFIX}excuse", value=f"Will unban a player from the chatroom you're in (You have to be the owner of the chatroom to do this command)")

            embed.set_footer(text=f"Do {CLIENT_PREFIX}help or {CLIENT_PREFIX}help 2 for more commands")

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
    embed.add_field(name=f"Do {CLIENT_PREFIX}help 2 or 3 for more commands", value="\u200b", inline=False)

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
        await ctx.send(f"Purged {ctx.channel} by {amt} messages", delete_after=3)

@client.command(aliases=['pl'])
async def play(ctx):
    args = parseArgs(ctx)
    url = None
    url_old = None

    try:
        url = args[0]
        url_old = url
    except IndexError:
        pass



    """Variables Needed for the play Command"""
    guild_id = ctx.guild.id
    guild = f"\\{ctx.message.guild.id}"
    guild_ = client.get_guild(guild_id)
    embed = discord.Embed(colour=LIGHT_BLUE)

    if url == "":

        url_old = "2 second video"

    multiple_songs = url.split(',')
    full_path = music_location+guild
    queue_full_path = queue_location+guild
    meta_full_path = metadata_location+guild
    config_full_path = config_location+guild
    server = client.get_guild(ctx.message.guild.id)
    embed = discord.Embed(colour=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)
    client_volume = return_data(config_location+f"\\{ctx.guild.id}\\config.json", "config", "vol")
    config = return_data(f"{config_location}\\{ctx.guild.id}\\config.json")
    message = ctx.message


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
            try:
                return await channel.connect()
            except discord.errors.ClientException:
                pass

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
        payload = return_data(metadata_location+f"\\{ctx.guild.id}\\payload-data.json")

        metadata['metadata'] = ({
            "name": title,
            "views": views,
            "author": ctx.author.name
        })

        payload["data"]["author-id"] = ctx.author.id
        payload["data"]["message-id"] = ctx.message.id
        payload["data"]["og-message-id"] = ctx.message.id

        json.dump(metadata, write_data, indent=4)
        make_asset(metadata_location+f"\\{ctx.guild.id}\\payload-data.json", "w", payload, 4)

    if int(len(length.split(':'))) >= 2 and int(len(length.split(':'))) >= 3:


        embed.color = RED
        embed.set_author(name=f"Cannot Download Song, Song is {length.split(':')[0]} hours! Limit is 2 hours!")

        return await ctx.send(embed=embed)

    if url_old == "2 second video":
        if len(os.listdir(queue_full_path)) > 0:

            embed.set_author(name=f'I will now start playing your queued songs, one moment please..')
            video = "https://www.youtube.com/watch?v=Wch3gJG2GJ4"
        else:
            embed.set_author(name="You don't have any songs in your queue")
            return
    else:
        embed.set_author(name=f'Playing "{title}"')
        embed.add_field(name=f"Views Ø ",value=views)
        embed.add_field(name=f"Link Ø ",value=video, inline=False)
        embed.add_field(name=f"Length Ø ",value=length, inline=False)
        embed.add_field(name=f"Channel Ø ",value=channel, inline=False)
        embed.add_field(name=f"Client Volume Ø ", value=client_volume, inline=False)
        embed.add_field(name=f"Looping Ø ", value=config["config"]["loop"], inline=False)
        embed.set_footer(text=f"You can click the 🎵 button to pause, Click 🎵 again to resume, Click the 🎶 button to skip the track, Click 📼 button to check how many songs are in the queue, Click 🔂 to turn on looping, and click 🔂 again to turn off looping")

    await ctx.send(embed=embed)

    def check_queue():
        config_data = return_data(f"{config_location}\\{ctx.guild.id}\\config.json")
        music_file = full_path+"\\music.wav"

        if config_data["config"]["loop"] == False:
            file_to_move = queue_full_path+f"\\music.wav"


            os.chdir(queue_full_path)

            if len(os.listdir()) <= 0:

                if os.path.isfile(music_file):
                    os.remove(music_file)
            else:
                next_song = queue_full_path+f"\\{os.listdir(queue_full_path)[0]}"
                if os.path.isfile(music_file):
                    os.remove(music_file)

                next_song_nfext = os.listdir(queue_full_path)[0].split(".wav")
                default_filename = youtubesearchpython.SearchVideos(keyword=next_song_nfext, offset=1, mode="dict", max_results=1)

                name = str(default_filename.titles[0])
                view = str(default_filename.views[0])
                channels = str(default_filename.channels[0])

                with open(meta_full_path+"\\metadata.json", 'w+') as write_metadata:

                    video_metadata = {}

                    video_metadata['metadata'] = ({
                        "name": name,
                        "views": view,
                        "author": ctx.author.name,
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
        else:
            if voice and voice.is_playing() and voice.is_paused():
                voice.stop()

            try:
                client_volume = return_data(config_location+f"\\{ctx.guild.id}\\config.json", "config", "vol")

                voice.play(discord.FFmpegPCMAudio(music_file), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = client_volume

            except discord.errors.ClientException:
                pass

    """Actual Play Command Code"""

    if os.path.isfile(full_path+f"\\music.wav"):

        voice = get(client.voice_clients, guild=ctx.guild)
        voice.stop()

        os.remove("music.wav")
    else:
        pass

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            def downloadContent():
                ydl.download([video])

            threading.Thread(target=downloadContent).start()

            try:
                raise IndexError
            except IndexError:
                loop = True

                while loop is True:

                    await asyncio.sleep(1)
                    if len(os.listdir()) == 1 and os.listdir()[0].endswith(".wav"):

                        os.rename(os.listdir()[0], "music.wav")
                        voice.stop()

                        try:
                            voice.play(discord.FFmpegPCMAudio(full_path+"\\music.wav"), after=lambda e: check_queue())
                            voice.source = discord.PCMVolumeTransformer(voice.source)
                            voice.source.volume = client_volume

                            await message.add_reaction("\U0001f3b6")
                            await message.add_reaction("\U0001f3b5")
                            await message.add_reaction("\U0001f4fc")
                            await message.add_reaction("\U0001f502")

                            loop = False

                        except discord.errors.ClientException as e:
                            await ctx.send(f"I am having some Network Issues, please try {CLIENT_PREFIX}join, and try again.\n\nError: {e}")
                    else:
                        continue

        except youtube_dl.utils.DownloadError:
            await ctx.send(f"I am having a song download error, please try {CLIENT_PREFIX}play again, if this problem persists, please file a bug report with {CLIENT_PREFIX}sendfeedback <The issue>")

@client.command(aliases=['qpl'])
async def queueplaylist(ctx, *, playlist=None):

    """queueplaylist command"""

    embed = discord.Embed(color=LIGHT_BLUE)
    ctx_author = ctx.author.name+"#"+ctx.author.discriminator
    url = None
    guild = f"\\{ctx.message.guild.id}"
    fail = False
    failure = True
    sendWrongfulEmbed = True

    globalPath = f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json"
    globalProfile = return_data(globalPath)

    if playlist is None:

        embed.set_author(name="You need to specify a playlist.")

        return await ctx.send(embed=embed)

    full_temp_path = temp_location+guild
    full_queue_path = queue_location+guild

    os.chdir(full_temp_path)

    for z in range(len(os.listdir())):
        os.remove(f"{temp_location}\\{ctx.guild.id}\\{os.listdir()[0]}")

    if os.path.isdir(playlist_location+f"\\{playlist}"):
        pass
    else:
        embed.color = RED
        embed.set_author(name=f'"{playlist}" is not a playlist!')


        if globalProfile["global"]["auto-correct"]["failure"]["failure-count"] >= 2 and globalProfile["global"]["auto-correct"]["failure"]["correct-playlist"] is not None:
            await ctx.send(f'That playlist does not exist, do you mean the playlist called "{globalProfile["global"]["auto-correct"]["failure"]["correct-playlist"]}"?\n*if so, please react to this message with the :white_check_mark: emoij\nor, if I was wrong, react with :no_entry: emoji. If you do not add a reaction within\n20 seconds, I will timeout.*')

            def checkEmj(reaction, member):
                return member == ctx.author and str(reaction.emoji) == "\u2705" or str(reaction.emoji) == "\u26D4"

            try:
                reaction, member = await client.wait_for('reaction_add', timeout=20.0, check=checkEmj)


            except asyncio.TimeoutError:
                await ctx.message.add_reaction(client.get_guild(MAIN_GUILD).emojis[14])
                sendWrongfulEmbed = False
            else:
                if reaction.emoji == "\u2705":
                    playlist = globalProfile["global"]["auto-correct"]["failure"]["correct-playlist"]
                    failure = False
                    globalProfile["global"]["auto-correct"]["failure"]["failure-count"] = 0

                elif reaction.emoji == "\u26D4":
                    await ctx.send("Okay, I got the playlist wrong, thank you for the feedback. :innocent:")
                    sendWrongfulEmbed = False
                else:
                    pass


        if failure is True:

            globalProfile["global"]["auto-correct"]["failure"] = {
                "failure-name": playlist,
                "command-completion": False,
                "failure-count": globalProfile["global"]["auto-correct"]["failure"]["failure-count"]+1,
                "correct-playlist": None
            }

            if sendWrongfulEmbed is True:
                await ctx.send(embed=embed)
            return make_asset(globalPath, "w", globalProfile, 4)
        else:
            embed.color = AZURE
            make_asset(globalPath, "w", globalProfile, 4)

    with open(playlist_location+f"\\{playlist}\\{playlist}.json") as queued_playlist:

        globalProfile["global"]["auto-correct"]["failure"]["command-completion"] = True
        globalProfile["global"]["auto-correct"]["failure"]["correct-playlist"] = playlist


        text = queued_playlist.read()
        json_text = json.loads(text)

        json_text_file = json_text['info']

        privacy_setting = json_text_file['privicy']
        author = json_text["metadata"]['playlist-author']
        playCount = int(json_text["metadata"]['queue-count'])+1

        songs = json_text_file['playlist'].split(',')

        make_asset(globalPath, "w", globalProfile, 4)

        async def queue_playlist():
            authors = []

            for q in range(len(author)):
                user = client.get_user(author[q])
                authors.append(f"{user}")

            playlist_path = f"{playlist_location}\\{playlist}\\{playlist}.json"
            playlist_data = return_data(playlist_path)

            embed.set_author(name=f'Queueing the Playlist Ø "{playlist}"')

            songListFull = ", ".join(songs)
            authors = ", ".join(authors)

            embed.add_field(name="Author of Playlist> ", value=authors, inline=False)
            embed.add_field(name="Songs > ", value=songListFull, inline=False)
            embed.add_field(name="Amout of Songs > ", value=len(songs), inline=False)
            embed.set_footer(text=f"Once a green tick reaction is shown on the command message, your playlist will have finished queueing,  if you see a red circle with a whiteline, the download failed.")
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
                loop = True

                if int(len(len_split)) >= 3 and int(len_split[0]) >= 1:


                    embed.color = RED
                    embed.set_author(name=f"Song / Video is too long! Limit is 1 hour! (Song is {int(len_split[0])})")

                    return await ctx.send(embed=embed)

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    try:
                        try:
                            filtered = filt_str(title)

                            def queueSongs():
                                if loop is True:
                                    ydl.download([link])
                            threading.Thread(target=queueSongs).start()

                        except (youtube_dl.utils.DownloadError, urllib.error.HTTPError):
                            fail = True
                            return await ctx.message.add_reaction("\u26D4")
                        try:
                            raise IndexError

                        except (IndexError, PermissionError):

                            while loop is True:

                                await asyncio.sleep(1)
                                if len(os.listdir()) == 1 and os.listdir()[0].endswith(".wav"):

                                    if "playscript" in playlist_data["metadata"].keys():

                                        os.rename(os.listdir()[0], f"{playlist_data['metadata']['playscript'][x]} - {filtered}.wav")
                                        shutil.move(os.listdir()[0], full_queue_path)
                                    else:

                                        os.rename(os.listdir()[0], filtered+".wav")
                                        shutil.move(os.listdir()[0], full_queue_path)

                                    await ctx.message.add_reaction(client.get_guild(MAIN_GUILD).emojis[x])
                                    loop = False

                                else:
                                    continue


                    except shutil.Error:
                        return await ctx.message.add_reaction("\u26D4")
                        fail = True

        if privacy_setting == "public" or ctx.author.id in author:
            await queue_playlist()

            if fail is True:
                return
            playlist_path = f"{playlist_location}\\{playlist}\\{playlist}.json"
            playlist_data = return_data(playlist_path)
            playlist_data["metadata"]["queue-count"] = playCount
            globalData = return_data(global_profile+f"\\{ctx.author.id}\\{ctx.author.id}.json")
            metadata = return_data(metadata_location+f"\\{ctx.guild.id}\\payload-data.json")


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

                metadata["data"]["queued-playlist"] = playlist

                make_asset(playlist_path, "w", playlist_data, 4)
                make_asset(metadata_location+f"\\{ctx.guild.id}\\payload-data.json", "w", metadata, 4)
                make_asset(global_profile+f"\\{ctx.author.id}\\{ctx.author.id}.json", "w", globalData, 4)

        elif privacy_setting == "server":
            if int(ctx.guild.id) in json_text["metadata"]['server-playlist']:
                await queue_playlist()
                if fail is True:
                    return
            else:
                embed.color = RED
                embed.set_author(name="This Playlist is server only (meaning, the playlist is whitelisted, and only selected servers can use this playlist)")

                return await ctx.send(embed=embed)
        else:
            embed.color = RED
            embed.set_author(name="This playlist is private!")

            return await ctx.send(embed=embed)
        embed.set_author(name=f'Queued the playlist Ø "{playlist}"')

        for x in range(len(os.listdir(temp_location+f"\\{ctx.guild.id}\\"))):
            os.remove(os.listdir()[x])

        for y in range(len(songs)):
            await ctx.message.remove_reaction(client.get_guild(MAIN_GUILD).emojis[y], client.get_user(798867893910765579))

        await ctx.message.add_reaction("\u2705")



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
        try:
            embed.set_author(name=f"Connected to {channel}")
            await ctx.send(embed=embed)
            voice = await channel.connect()

        except discord.errors.ClientException:
            await ctx.send("Already connected to a voice channel")
@client.command(aliases=['p'])
async def pause(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice != None:
        if voice.is_playing() and voice.is_connected():
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
            loop = True

        except IndexError:
            return await sendEmbed(embed, ctx, f'No song / video with the name "{url}" (I have stopped queueing songs)')

        if os.path.isfile(f"{queue_location}\\{ctx.message.guild.id}\\{title}.wav"):

            embed.color = RED
            embed.set_author(name=f"The song: ''{title}'' is already queued!")

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

                def queueSongs():
                    if loop is True:
                        ydl.download([video])

                threading.Thread(target=queueSongs).start()

                filtered = filt_str(title)

                """Moves and renames downloaded file to the queue"""

                while loop is True:

                    await asyncio.sleep(1)

                    if len(os.listdir()) == 1 and os.listdir()[0].endswith(".wav"):

                        temp_song_location = full_temp_path+f"\\temp.wav"
                        queued_name = filtered+".wav"
                        temp_song = os.listdir()[0]

                        os.rename(temp_song, queued_name)
                        shutil.move(temp_song_location, full_queue_path)

                        await ctx.send(embed=embed)

                        loop = False
                    else:
                        continue
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
    config_queue = f"{config_location}\\{ctx.guild.id}\\config.json"
    first_song = None

    if len(os.listdir(guild_queue)) > 0:
        first_song = os.listdir(guild_queue)[0].split(".wav")[0]

    embed = discord.Embed(color=LIGHT_BLUE)
    voice = get(client.voice_clients, guild=ctx.guild)
    config_data = return_data(config_queue)

    embed.set_author(name="Skipping Current Song")



    if voice and voice.is_playing() or voice.is_paused():

        if first_song is None:
            embed.set_author(name="No more songs")

        else:
            embed.set_author(name=f"Now Playing: {first_song}")

            voice.pause()
            voice.stop()

            config_data["config"]["loop"] = False

            make_asset(config_queue, "w", config_data, 4)
    else:
        embed.set_author(name="No song to be skipped")

    await ctx.send(embed=embed)

@client.command(aliases=['v'])
async def volume(ctx, volume_float):

    guild = f"\\{ctx.message.guild.id}"
    full_config_path = config_location+guild
    embed = discord.Embed(colour=LIGHT_BLUE)
    try:
        if volume_float is None:
            embed.set_author(name="You need to set a volume. (In a float value, like: 0.1, 0.6, 1.7)")
        elif volume_float > 10:
            embed.set_author(name="You cannot go any higher than 10, you would get hearing damage.")
        else:

            config_data = return_data(f"{config_location}\\{ctx.guild.id}\\config.json")
            config_data["config"]["vol"] = float(volume_float)

            make_asset(file=full_config_path+"\\config.json", mode="w", data=config_data, indention=4)

            embed.set_author(name=f"Changed volume to > {volume_float}")


    except TypeError:
        embed.set_author(name="The volume has to be A Floating Point Value, or an integer value.")

    finally:
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

    embed = discord.Embed(color=LIGHT_BLUE)
    song_list = []
    songsList = os.listdir(queue_location+f"\\{ctx.guild.id}")

    embed.set_author(name="Queued Songs")

    for x in range(len(songsList)):
        song = songsList[x].split(".wav")[0]

        embed.add_field(name=f"Song {x+1}  Ø ", value=song, inline=False)

    embed.set_footer(text=f"Amount of songs left: {len(songsList)}")
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
                            return await ctx.send("Incorrect privacy setting (public, private or server)")
                    else:
                        pass


            else:
                pass

    os.chdir(playlist_location)

    playlist_id = random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)


    url = filt_str_mod(str(url))

    mod_url = url.split(", ")

    linkLists = return_data(f"{system_location}\\tags-link.json")

    if playlist_id in linkLists["list"]["tags"]:
        playlist_id = random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)


    linkLists["list"]["tags"].append(playlist_id)



    for x in range(len(mod_url)):
        convt_url = youtubesearchpython.SearchVideos(keyword=mod_url[x], offset=1, mode="dict", max_results=1)

        thumbnail = convt_url.thumbnails[0]
        title = convt_url.titles[0]
        length = 0

        song_len.append(length)
        song_list.append(title)

        final_len = final_len+song_len[x]

    final_songs = filt_str_mod(str(song_list))

    if len(final_songs.split(", ")) > 14:
        return await ctx.send("You cannot add more than 14 songs. Please try again with fewer songs.")

    conv_url_ = youtubesearchpython.SearchVideos(keyword=random.choice(mod_url), offset=1, mode="dict", max_results=1)
    thumbnail = conv_url_.thumbnails[0]

    playlist_ = playlist_location+f"\\{playlist_name}"
    full_author = ctx.author.name+"#"+ctx.author.discriminator

    if mode == "public" or mode == "private" or mode == "server":
        pass
    else:
        embed.color = RED
        embed.set_author(name=f"Incorrect privacy setting (public, private or server)")
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
                "playlist-creation": str(datetime.datetime.now()),
                "playlist-comments": {},
                "playlist-comment-count": 0

            })

            json.dump(playlist_info, new_playlist, indent=4)
            make_asset(f"{system_location}\\tags-link.json", "w", linkLists, 4)

            embed.set_author(name=f'Made new Playlist Ø "{playlist_name}"')
            embed.add_field(name="Author ● ", value=full_author, inline=False)
            embed.add_field(name="Songs ● ", value=final_songs, inline=False)
            embed.add_field(name="Privacy Setting ● ", value=mode)

            embed.set_image(url=thumbnail[1])
            embed.set_thumbnail(url=vorbis_img)

            await ctx.send(embed=embed)


@client.command()
async def playlists(ctx, *, playlist=None):

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    embed = discord.Embed(color=LIGHT_BLUE)

    playlistOld = None
    playlistID = None
    name = None
    sendEmbed = None

    if playlist is None:
        playlistData = return_data(f"{system_location}\\recommendedPlaylist.json", "src")

        playlist = playlistData["playlist-name"]
        playlistID = playlistData["playlist-id"]

    else:
        playlistOld = False

    playlist_ = playlist_location+f"\\{playlist}\\"

    if os.path.isfile(playlist_+f"{playlist}.json"):

        with open(playlist_+f"{playlist}.json") as read_playlist:

            text = read_playlist.read()
            json_data = json.loads(text)
            playlist_json = json_data['info']
            playlist_metadata = json_data['metadata']

            if playlist_json["privicy"] == "public" or ctx.author.id in playlist_metadata["playlist-author"]:
                print("CHECK 2")
                if playlistOld is None:

                    if str(playlistID) != str(playlist_metadata["playlist-id"]):

                        embed.set_author(name="Most popular playlist has been deleted.")

                        return await ctx.send(embed=embed)
                    else:
                        embed.set_author(name=f'Most popular playlist')

                        embed.add_field(name=f"Playlist Name Ø", value=playlist, inline=False)
                        embed.add_field(name=f"Comment Count Ø", value=playlist_metadata["playlist-comment-count"], inline=False)
                        time = playlistData['time']

                        year = time.split("-")[0]
                        month = time.split("-")[1]
                        day = time.split("-")[2].split(" ")[0]
                        tod = time.split("-")[2].split(" ")[1]

                        embed.set_footer(text=f"Last Updated at {months[int(month)-1]} {day}, {year} at {tod}")

                        embed.color = GOLD

                else:
                    embed.set_author(name=f'Here is the playlist "{playlist}"')

                try:
                    embed.add_field(name="Playlist Description > ", value=playlist_metadata["playlist-description"], inline=False)
                except KeyError:
                    pass

                playlist_tags = filt_str_mod(str(playlist_metadata["tags"]))
                embed.set_image(url=playlist_metadata['playlist-cover'])

                if len(playlist_metadata["tags"]) == 0:
                    playlist_tags = "No tags"

                embed.add_field(name=f"Author of Playlist > ", value=playlist_metadata['playlist-author-name'], inline=False)
                for x in range(len(playlist_json["playlist"].split(", "))):
                    embed.add_field(name=f"Song {x+1} ", value=playlist_json["playlist"].split(", ")[x], inline=False)
                embed.add_field(name="Length of Playlist (Minutes) > ", value=playlist_metadata['playlist-length'], inline=False)
                embed.add_field(name="Date of playlist creation > ", value=playlist_metadata['playlist-creation'], inline=False)
                embed.add_field(name="Privacy Setting > ", value=playlist_json["privicy"], inline=False)
                embed.add_field(name="Tags > ", value=playlist_tags, inline=False)

                if "playscript" in playlist_metadata.keys():

                    finalScript = ", ".join(playlist_metadata["playscript"])

                    embed.add_field(name="PlayScript :tm: > ", value=finalScript, inline=False)
            elif playlist_json["privicy"] == "server":

                if int(ctx.guild.id) in playlist_metadata['server-playlist']:
                    playlist_tags = filt_str_mod(str(playlist_metadata["tags"]))

                    try:
                        embed.add_field(name="Playlist Description > ", value=playlist_metadata["playlist-description"], inline=False)
                    except KeyError:
                        pass

                    if len(playlist_metadata["tags"]) == 0:
                        playlist_tags = "No tags"

                    embed.set_author(name=f'Here is the playlist "{playlist}"')
                    embed.set_image(url=playlist_metadata['playlist-cover'])

                    embed.add_field(name=f"Author of Playlist > ", value=playlist_metadata['playlist-author-name'])
                    embed.add_field(name="Songs > ", value=playlist_json['playlist'], inline=False)
                    embed.add_field(name="Length of Playlist (Minutes) > ", value=playlist_metadata['playlist-length'], inline=False)
                    embed.add_field(name="Date of playlist creation > ", value=playlist_metadata['playlist-creation'], inline=False)
                    embed.add_field(name="Privacy Setting > ", value=playlist_json["privicy"], inline=False)
                    embed.add_field(name="Tags > ", value=playlist_tags, inline=False)



                else:
                    embed.color = RED
                    embed.set_author(name="This Playlist is server only (meaning, the playlist is whitelisted, and only selected servers can use this playlist)")

            else:
                embed.color = RED
                embed.set_author(name="This Playlist is Private.")

            try:
                if "playlist-color" in playlist_metadata.keys():
                    embed.color = discord.Color.from_rgb(int(playlist_metadata["playlist-color"][0]), int(playlist_metadata["playlist-color"][1]), int(playlist_metadata["playlist-color"][2]))
                else:
                    pass
            except KeyError:
                pass

    else:
        if playlistOld is None:
            name = "Most popular playlist has been deleted."
        else:
            embed.color = RED
            name = "The playlist you're looking for does not exist!"

    await ctx.send(embed=embed)

@client.command()
async def deleteplaylist(ctx, *, playlist=None):

    embed = discord.Embed(color=LIGHT_BLUE)

    tagsList = f"{system_location}\\tags-link.json"
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

        make_asset(f"{system_location}\\tags-link.json", "w", tagsListData, 4)
        return await ctx.send(embed=embed)


    p_author = return_data(playlistPath)

    if p_author is not None:
        if ctx.author.id == p_author["metadata"]["playlist-author"][0]:
            await delete()

        else:
            embed.color = RED
            embed.set_author(name="You're not the owner of this playlist!")

            return await ctx.send(embed=embed)

    else:
        await sendEmbed(embed, ctx, f"No playlist with the name ''{playlist}''")

@client.command()
async def usage(ctx):

    embed = discord.Embed(color=AZURE)
    args = parseArgs(ctx)

    try:
        command = args[0]

        if command == "2":

            embed.add_field(name=":eject:  More Playlist Commands' Usage  :eject:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}asong > ", value=f"{CLIENT_PREFIX}asong <Song>, <Playlist> (Note: you can only add one song at a time)")
            embed.add_field(name=f"{CLIENT_PREFIX}paserver > ", value=f"{CLIENT_PREFIX}paserver <Server ID>, <Playlist>")
            embed.add_field(name=f"{CLIENT_PREFIX}eplaylist > ", value=f"{CLIENT_PREFIX}eplaylist <picture>, <profile>, <URL of picture>")
            embed.add_field(name=f"{CLIENT_PREFIX}playliststag > ", value=f"{CLIENT_PREFIX}playliststag <tag>")
            embed.add_field(name=f"{CLIENT_PREFIX}atag > ", value=f"{CLIENT_PREFIX}atag <playlist Name>, <tag> Note: You can only add one tag at a time, but you can add as many as you like")
            embed.add_field(name=f"{CLIENT_PREFIX}pdescription > ", value=f"{CLIENT_PREFIX}pdescription <playlist Name>, <description> (remember to seperate Playlist Name and Description with a comma)")
            embed.add_field(name=":musical_note:  More Music Commands' Usage  :musical_note:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}lyrics > ", value=f"{CLIENT_PREFIX}lyrics <Artist Name>, <Song Name> remember to seperate Artist Name and Song Name with a comma")
            embed.add_field(name=f"{CLIENT_PREFIX}loop > ", value=f"{CLIENT_PREFIX}loop")
            embed.add_field(name=":soccer:  More General Commands' Usage  :soccer:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}credit > ", value=f"{CLIENT_PREFIX}credit")
            embed.add_field(name=f"{CLIENT_PREFIX}sendfeedback > ", value=f"{CLIENT_PREFIX}sendfeedback <feedback>")
            embed.add_field(name=f"{CLIENT_PREFIX}comment > ", value=f"{CLIENT_PREFIX}comment <comment text> (Note: To send a comment to a playlist, you have to have queued that playlist with {CLIENT_PREFIX}queueplaylist)")
            embed.add_field(name=f"{CLIENT_PREFIX}read > ", value=f"{CLIENT_PREFIX}read <playlist you want to read comments from>, <comment ID (Optional)>")
            embed.add_field(name=f"{CLIENT_PREFIX}delete > ", value=f"{CLIENT_PREFIX}delete <playlist of where the comment was posted>, <comment ID>")
            embed.add_field(name=f"{CLIENT_PREFIX}image > ", value=f"{CLIENT_PREFIX}image")
            embed.add_field(name=":moneybag:  Economy Commands' Usage  :moneybag:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}shop > ", value=f"{CLIENT_PREFIX}shop")
            embed.add_field(name=f"{CLIENT_PREFIX}buy > ", value=f"{CLIENT_PREFIX}buy <item name>")

        elif command == "3":

            embed.add_field(name=f":speech_left: Communication Commands :speech_left:", value="\u200b", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}chatroom > ", value=f"{CLIENT_PREFIX}chatroom <Chatroom Name>, <Password>")
            embed.add_field(name=f"{CLIENT_PREFIX}connect > ", value=f"{CLIENT_PREFIX}connect <Chatroom ID>, <Password>")
            embed.add_field(name=f"{CLIENT_PREFIX}chat > ", value=f"{CLIENT_PREFIX}chat <Message>")
            embed.add_field(name=f"{CLIENT_PREFIX}leave > ", value=f"{CLIENT_PREFIX}leave")
            embed.add_field(name=f"{CLIENT_PREFIX}pull > ", value=f"{CLIENT_PREFIX}pull <Chatroom Password>")
            embed.add_field(name=f"{CLIENT_PREFIX}edit > ", value=f"{CLIENT_PREFIX}edit <edit options will show up when you do this command>")
            embed.add_field(name=f"{CLIENT_PREFIX}room > ", value=f"{CLIENT_PREFIX}room")
            embed.add_field(name=f"{CLIENT_PREFIX}boot > ", value=f"{CLIENT_PREFIX}boot <Player Fullname including tag>")
            embed.add_field(name=f"{CLIENT_PREFIX}exile > ", value=f"{CLIENT_PREFIX}exile <Player Fullname including tag>")
            embed.add_field(name=f"{CLIENT_PREFIX}excuse > ", value=f"{CLIENT_PREFIX}excuse <Player Fullname including tag>")

        else:
            raise IndexError("No Error")
    except IndexError:
        embed.set_author(name="Command Usage")

        embed.add_field(name=":soccer:  General Commands  :soccer:", value="\u200b", inline=False)
        embed.add_field(name=f"{CLIENT_PREFIX}help > ", value=f"{CLIENT_PREFIX}help")
        embed.add_field(name=f"{CLIENT_PREFIX}join > ", value=f"{CLIENT_PREFIX}join")
        embed.add_field(name=f"{CLIENT_PREFIX}disconnect", value=f"{CLIENT_PREFIX}disconnect")
        embed.add_field(name=f"{CLIENT_PREFIX}usage > ", value=f"{CLIENT_PREFIX}usage <2-3>")
        embed.add_field(name=f"{CLIENT_PREFIX}this > ", value=f"{CLIENT_PREFIX}this")
        embed.add_field(name=f"{CLIENT_PREFIX}profile > ", value=f"{CLIENT_PREFIX}profile <@user>")
        embed.add_field(name=":musical_note:  Music Commands  :musical_note:", value="\u200b", inline=False)
        embed.add_field(name=f"{CLIENT_PREFIX}queue > ", value=f"{CLIENT_PREFIX}queue <YouTube Video URLs or Name, If playing multiple songs, separate with a comma>")
        embed.add_field(name=f"{CLIENT_PREFIX}play > ", value=f"{CLIENT_PREFIX}play <YouTube Video URL or Name>")
        embed.add_field(name=f"{CLIENT_PREFIX}clear > ", value=f"{CLIENT_PREFIX}clear")
        embed.add_field(name=f"{CLIENT_PREFIX}songs > ", value=f"{CLIENT_PREFIX}songs")
        embed.add_field(name=f"{CLIENT_PREFIX}resume > ", value=f"{CLIENT_PREFIX}resume")
        embed.add_field(name=f"{CLIENT_PREFIX}pause > ", value=f"{CLIENT_PREFIX}pause")
        embed.add_field(name=f"{CLIENT_PREFIX}volume > ", value=f"{CLIENT_PREFIX}volume <1-10>")
        embed.add_field(name=f"{CLIENT_PREFIX}song > ", value=f"{CLIENT_PREFIX}song")
        embed.add_field(name=f"{CLIENT_PREFIX}spotify > ", value=f"{CLIENT_PREFIX}spotify <@user>")
        embed.add_field(name=":eject:  Playlist Commands' Usage  :eject:", value="\u200b", inline=False)
        embed.add_field(name=f"{CLIENT_PREFIX}playlist > ", value=f"{CLIENT_PREFIX}playlist <Playlist Name>, <Privacy Mode (public/private)>, <YouTube Video URLs or Name, Seperate all parameters with commas, including songs>")
        embed.add_field(name=f"{CLIENT_PREFIX}playlists > ", value=f"{CLIENT_PREFIX}playlists <Playlist Name>")
        embed.add_field(name=f"{CLIENT_PREFIX}deleteplaylist > ", value=f"{CLIENT_PREFIX}deleteplaylist <Playlist Name>")
        embed.add_field(name=f"{CLIENT_PREFIX}queueplaylist > ", value=f"{CLIENT_PREFIX}queueplaylist <Playlist Name>")
        embed.add_field(name=f"{CLIENT_PREFIX}ptrust > ", value=f"{CLIENT_PREFIX}ptrust <@user> <Playlist name>")
        embed.add_field(name=f"{CLIENT_PREFIX}prtrust > ", value=f"{CLIENT_PREFIX}prtrust <@user> <Playlist name>")
        embed.add_field(name=f"{CLIENT_PREFIX}pprivacy > ", value=f'{CLIENT_PREFIX}pprivacy <public, private, or server>, <Playlist name>')

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
        _font_ = "GothamBook.ttf"

        full_usr_path = f"{user_location}\\{ctx.message.guild.id}"

        with open(f"{full_usr_path}\\{user_id}\\{user_id}-exp.json") as read_level_data:

            text = read_level_data.read()
            json_readable = json.loads(text)

            json_tabel = json_readable[str(user_id)]

            current_level = json_tabel['member-level']
            current_exp = json_tabel['member-exp']
            until_next_levelup = json_tabel['member-until-next-lvl']

        with open(f"{full_usr_path}\\{user_id}\\{user_id}.json") as read_user:

            globalData = return_data(global_profile+f"\\{member.id}\\{member.id}.json")

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

                        make_asset(global_profile+f"\\{member.id}\\{member.id}.json", "w", globalData, 4)
                        continue

                return mostPopularPlaylist

            text = read_user.read()
            json_formatted = json.loads(text)
            favoritePlaylist = None
            user_info = json_formatted[str(user_id)]
            userBalance = return_data(f"{user_location}\\{ctx.guild.id}\\{ctx.author.id}\\{ctx.author.id}-bank.json")
            levels = [50, 60, 70, 80, 90, 100]

            if calculatePopularPlaylist()[1] is None:
                favoritePlaylist = "Does not have one"
            else:
                favoritePlaylist = calculatePopularPlaylist()[1]

            with requests.get(str(member.avatar_url), stream=True) as dataStream:
                avatar_location = f"{user_location}\\{ctx.guild.id}\\{user_info['member-id']}\\avatar.png"

                if dataStream.status_code == 200:
                    dataStream.raw.decode_content = True

                    with open(avatar_location, 'wb') as avatar:
                        shutil.copyfileobj(dataStream.raw, avatar)

                else:
                    pass

                with Image.open(f"{asset_location}\\profile-template.png") as file:
                    size = (400, 400)

                    level_progress_bar_list = []
                    progress_bar = json_formatted["progress-bar"]["progress-bar-count"]

                    avatar_ = Image.open(avatar_location)
                    avatar_ = avatar_.convert("L")
                    avatar_ = avatar_.resize(size, Image.ANTIALIAS)

                    file.paste(avatar_, (580, 580))

                    font = ImageFont.truetype(f"{gotham_font_location}\\{_font_}", 31)
                    font_ = ImageFont.truetype(f"{gotham_font_location}\\{_font_}", 17)
                    image = ImageDraw.Draw(file)
                    COLOUR = None
                    rank = None

                    if current_level >= 100 and current_level < 200:
                        COLOUR = AZURE_T
                        rank = "Centennial"

                    elif current_level >= 200 and current_level < 300:
                        COLOUR = RED_T
                        rank = "Cardinal"
                    else:
                        COLOUR = WHITE_T
                        rank = "Citizen"

                    if "description" in list(globalData["global"].keys()):
                        image.text((25, 25), text=f"Username: {user_info['member-name']}\n\nUser ID: {user_info['member-id']}\n\nUser Join Date: {user_info['member-joindate'].split('.')[0]}\n\nUser Level: {current_level}\n\nUser Experience: {current_exp+1}\n\nUntil Next Level Up: {int(until_next_levelup-current_exp-1)}\n\nServer: {ctx.guild}\n\nUser Description: {globalData['global']['description']}\n\nRank: {rank}", fill=COLOUR, font=font)
                    else:
                        image.text((25, 25), text=f"Username: {user_info['member-name']}\n\nUser ID: {user_info['member-id']}\n\nUser Join Date: {user_info['member-joindate'].split('.')[0]}\n\nUser Level: {current_level}\n\nServer: {ctx.guild}\n\nRank: {rank}", fill=COLOUR, font=font)

                    image.rectangle([1020, 1022, 4, 0], fill=None, outline=COLOUR, width=6)
                    image.rectangle([580, 580, 980, 980], fill=None, outline=COLOUR, width=4)
                    image.rectangle([40, 880, 500, 940], fill=None, outline=COLOUR, width=4)

                    image.text((210, 835), text=f"Level {current_level}", fill=COLOUR, font=font)#

                    y = 0
                    z = 50

                    if until_next_levelup == 50:
                        y=18.8
                    elif until_next_levelup == 60:
                        y=15.6
                    elif until_next_levelup == 70:
                        y=13.3
                    elif until_next_levelup == 80:
                        y=11.3
                    elif until_next_levelup == 90:
                        y=10
                    elif until_next_levelup == 100:
                        y=9

                    image.rectangle([40, 880, z+y*progress_bar, 940], fill=COLOUR, width=4)

                    file.save(f"{user_location}\\{ctx.guild.id}\\{user_info['member-id']}\\profile.png")
                    os.remove(avatar_location)

            embed.set_author(name=f'Here is "{user_info["member-name"]}" Profile', icon_url=vorbis_img)
            embed.add_field(name=f"User Name  Ø   {user_info['member-name']}", value="\u200b", inline=False)
            embed.add_field(name=f"User ID   Ø   {user_info['member-id']}", value="\u200b", inline=False)
            embed.add_field(name=f"User Join Date   Ø   {user_info['member-joindate'].split('.')[0]}", value="\u200b", inline=False)
            embed.add_field(name=f"Current User Level   Ø   {current_level}", value="\u200b", inline=False)
            embed.add_field(name=f"Favorite Playlist   Ø   {favoritePlaylist}", value="\u200b", inline=False)

            if member.id == ctx.author.id:
                embed.add_field(name=f"User Balance   Ø   {userBalance[str(ctx.author.id)]['balance']}", value="\u200b", inline=False)

            embed.set_image(url=user_info['member-avatar'])

            if "description" in list(globalData["global"].keys()):
                embed.add_field(name=f'User Description   Ø   "{globalData["global"]["description"]}"', value="\u200b", inline=False)

            if globalData["global"]["has-link"] is True:
                if int(globalData["global"]["link-id"]) == ctx.guild.id:
                    guildID = int(globalData["global"]["link-made-id"])
                else:
                    guildID = int(globalData["global"]["link-id"])

                guild = client.get_guild(guildID)
                embed.add_field(name=f"Has a Link with   Ø   {guild} (guild ID: {guildID})", value="\u200b", inline=False)
            else:
                embed.add_field(name=f"Does not have a link", value="\u200b", inline=False)
            await ctx.send(embed=embed)

    except (commands.UserNotFound):

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
async def kick(ctx, member : discord.Member=None, *, reason : str="Unspecified"):

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
    commands = ["help", "join_role", "max_warnings", "blacklist", "log_channel", "join_channel", "leave_channel", "join_message", "join_image", "leave_message", "leave_image", "whitelist", "shop_image", "shop_name"]

    if command is None:
        command = "help"

    data = return_data(f"{config_location}\\{ctx.guild.id}\\config.json")




    if command == commands[0]:
        text = "Server Command Help"

        embed.add_field(name="Note > ", value="This may seem complicated, but don't worry! just look at the help command")
        embed.add_field(name="join_role", value=f"{CLIENT_PREFIX}server join_role <The role to give when a player joins>")
        embed.add_field(name="max_warnings", value=f'{CLIENT_PREFIX}server max_warnings <1 / 10> or put it to "None" for unlimited warnings')
        embed.add_field(name="log_channel", value=f"{CLIENT_PREFIX}server log_channel <channel_id> Sets default log channel, (IE: Blacklist notifications and level up messages)")
        embed.add_field(name="join_channel", value=f"{CLIENT_PREFIX}server join_channel <channel_id> Sets join log messages (IE: When a player joins, the message of the joining player will be sent to that channel)")
        embed.add_field(name="leave_channel", value=f"{CLIENT_PREFIX}server leave_channel <channel_id> Sets leave log messages (IE: When a player leaves, the message of the leaving player will be sent to the specified channel)")
        embed.add_field(name="join_message", value=f"{CLIENT_PREFIX}server join_message <message> The message that will be sent to the specifed join channel")
        embed.add_field(name="join_image", value=f"{CLIENT_PREFIX}server join_image <url> The image that will be sent to the specified join channel upon a members joining to the server")
        embed.add_field(name="leave_image", value=f"{CLIENT_PREFIX}server leave_image <url> The image that will be sent to the specified leave channel upon a members departure from the server")
        embed.add_field(name="whitelist", value=f"{CLIENT_PREFIX}server whitelist on | off Will turn on | off whitelist ")
        embed.add_field(name="shop_image", value=f"{CLIENT_PREFIX}server shop_image <URL> This will change the shop image from the default Vorbis one (Think of it as a shop sign :D)")
        embed.add_field(name="shop_name", value=f"{CLIENT_PREFIX}server shop_name <New Name> Will change the name of your shop")

    elif command == commands[1]:
        text = f"I have set the join role to {args}"
        data["config"][f"{command}"] = args

    elif command == commands[2]:
        text = f"I have set the Max Warnings to {args}"
        data["config"][f"{command}"] = args

    elif command == commands[3]:
        text = "The blacklist feature has been deprecated."

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

        if args == "on" or args == "off":
            text = f"Whitelisted player IDs > {args}"
            data["config"][f"{command}"] = args.split(", ")
        else:
            text = f"That is not an option, Please do {CLIENT_PREFIX}server whitelist on or off"

    elif command == commands[12]:


        if image(args):
            text = f'New shop image'
            data["config"][f"{command}"] = args

            embed.set_image(url=args)
        else:
            text = "This is not a valid URL"

    elif command == commands[13]:

        text = f'The shops name is now "{args}"'
        data["config"][command] = args
    else:
        text = f"There is no server command with the name {command}"
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
            max_warnings = return_data(file=config_path, tabel="config", sub_tabel="max_warnings")
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
        await ctx.send("Missing Arguments")

@client.command()
@commands.has_permissions(administrator=True)
async def leaveguild(ctx):
    await ctx.send("Leaving Server...")
    guild = client.get_guild(ctx.guild.id)

    await guild.leave()

@client.command(aliases=["ah"])
async def adminhelp(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)

    embed.set_author(name="Administrator Help")

    embed.add_field(name=":fist:  Punishment Command  :fist:", value="\u200b", inline=False)
    embed.add_field(name=f"{CLIENT_PREFIX}kick", value="Kicks Selected Player")
    embed.add_field(name=f"{CLIENT_PREFIX}ban", value="Bans Selected Player")
    embed.add_field(name=f"{CLIENT_PREFIX}warn", value="Warns selected Player")
    embed.add_field(name=":star:  General Administration Commands  :star:", value="\u200b", inline=False)
    embed.add_field(name=f"{CLIENT_PREFIX}leave", value="Bot will leave the server")
    embed.add_field(name=f"{CLIENT_PREFIX}server", value="Server configurations")
    embed.add_field(name=f"{CLIENT_PREFIX}purge", value="Purges a channel by a selected amount of messages")
    embed.add_field(name=f"{CLIENT_PREFIX}unban", value="Unbans selected Player")
    embed.add_field(name=":money_with_wings:  Administrator Economy Commands  :money_with_wings:", value="\u200b", inline=False)
    embed.add_field(name=f"{CLIENT_PREFIX}bank", value="Will show general infomation about the guilds account (Like: Giving or clearing the bank)")
    embed.add_field(name=f"{CLIENT_PREFIX}sell", value=f"Will put an item in the shop (I STRONGLY recommend looking at usage help for this command, by doing {CLIENT_PREFIX}ahu)")
    embed.add_field(name=f"{CLIENT_PREFIX}remove", value=f"Will remove an item from the shop.")

    await ctx.send(embed=embed)

@client.command()
async def this(ctx):


    embed = discord.Embed(color=MEDIUM_PURPLE)
    guild = ctx.guild
    config = return_data(f"{config_location}\\{ctx.guild.id}\\config.json")

    embed.set_author(name=f"{guild}")
    embed.add_field(name="Server made at: ", value=str(guild.created_at).split(".")[0])
    embed.add_field(name="Level: ", value=guild.premium_tier, inline=False)
    embed.add_field(name="ID: ", value=guild.id, inline=False)
    embed.add_field(name="Member Count: ", value=guild.member_count, inline=False)
    embed.add_field(name="Region: ", value=guild.region, inline=False)
    embed.add_field(name="Bitrate Limit: ", value=guild.bitrate_limit, inline=False)
    embed.add_field(name="Owner: ", value=guild.owner, inline=False)
    embed.add_field(name="Latency: ", value=client.latency, inline=False)
    embed.add_field(name="Song Looping: ", value=config["config"]["loop"], inline=False)

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
            embed.set_author(name=f"You're not playing any song on Spotify")
        else:
            embed.set_author(name=f"{user} is not playing any song on Spotify")

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
        try:
            full_path = f"{playlist_location}\\{playlist_name}\\{playlist_name}.json"
            playlist_data = return_data(full_path)

            if ctx.author.id == playlist_data["metadata"]["playlist-author"][0]:
                if user.id in playlist_data["metadata"]["playlist-author"]:
                    embed.set_author(name=f"''{user}'' is already trusted")
                else:
                    playlist_data["metadata"]["playlist-author"].append(int(user.id))

                    make_asset(full_path, "w", playlist_data, 4)
                    embed.set_author(name=f"{user} is now trusted")
            else:
                embed.set_author(name=f"You're not allowed to trust other people (Even if you're trusted, only owner of the playlist can do this)")
        except TypeError:
            embed.set_author(name=f'No playlist with the name "{playlist_name}"')

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
async def pprivacy(ctx):

    playlist_name = None
    setting = None
    done = False
    done1 = False
    args = parseArgs(ctx)

    try:
        setting = args[0]
        playlist_name = args[1]
    except IndexError:
        return await ctx.send("Missing Arguments")


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
async def asong(ctx):

    done = False
    done1 = False
    song_list = []
    args = parseArgs(ctx)

    voice = get(client.voice_clients, guild=ctx.guild)
    embed = discord.Embed(color=LIGHT_BLUE)

    try:
        songs = args[0]
        playlist_name = args[1]




    except IndexError:

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

    if songs == "current song":
        songData = getSongMetaData(ctx)
        songs = songData["metadata"]["name"]

    song_data_old = return_data(file=f"{playlist_location}\\{playlist_name}\\{playlist_name}.json", tabel="info", sub_tabel="playlist")
    song_data_full = return_data(file=f"{playlist_location}\\{playlist_name}\\{playlist_name}.json")

    if song_data_old is None:
        embed.set_author(name=f'No playlist with the name "{playlist_name}"')
    else:
        if check_owner(playlist=playlist_name, owner_id=ctx.author.id):

            song_list.append(song_data_old)
            song_list.append(songs)

            full_songs = ", ".join(song_list)

            if len(full_songs.split(", ")) > 14:
                await ctx.send("You cannot have more than 14 songs in a playlist")
            else:
                if "playscript" in song_data_full["metadata"].keys():
                    song_data_full["metadata"]["playscript"].append(str(len(full_songs.split(", "))))
                    song_data_full["metadata"]["og-playscript"].append(str(len(full_songs.split(", "))))

                song_data_full["info"]["playlist"] = full_songs
                make_asset(file=f"{playlist_location}\\{playlist_name}\\{playlist_name}.json", mode="w", data=song_data_full, indention=4)

                embed.set_author(name=f'I have Added Ø "{songs}" to {playlist_name}')
                await ctx.send(embed=embed)
        else:
            embed.set_author(name=f"You're not the owner of this playlist.")
            await ctx.send(embed=embed)


@client.command()
async def paserver(ctx):

    args = parseArgs(ctx)

    try:
        guild_id = args[0]

        if guild_id == "":
            raise IndexError

        playlist_name = args[1]

    except IndexError:
        return await ctx.send("Missing Arguments")

    embed = discord.Embed(color=LIGHT_BLUE)

    done = False
    done1 = False

    guild = client.get_guild(int(guild_id))
    full_path = f"{playlist_location}\\{playlist_name}\\{playlist_name}.json"
    playlist_data = return_data(file=full_path)

    if check_owner(playlist_name, ctx.author.id):
        try:
            if playlist_data["info"]["privicy"] == "server":
                embed.set_author(name=f"Added {guild} to the playlist whitelist")

                playlist_data['metadata']['server-playlist'].append(int(guild_id))

                make_asset(full_path, "w", playlist_data, 4)
            else:
                raise KeyError
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
        print(content)
        try:
            try:
                playlist_name = content[0]
                songs = content[1]
            except IndexError:
                return await ctx.send("Missing Arguments (/rsong <Playlist Name>, <Song> Remember to add a comma between the Playlist Name and The song)")

            location = f"{playlist_location}\\{playlist_name}\\{playlist_name}.json"
            song = None

            data = return_data(file=location)
            song_list = data["info"]["playlist"]

            songListSplited = song_list.split(", ")
            data["info"]["playlist"] = songListSplited

            try:

                if check_owner(playlist_name, ctx.author.id):
                    try:

                        song = songListSplited[int(songs)-1]
                        songListSplited.pop(int(songs)-1)


                        if "playscript" in data["metadata"].keys():
                            data["metadata"]["playscript"].remove(str(songs))
                            data["metadata"]["og-playscript"].remove(str(songs))

                    finally:
                        data["info"]["playlist"] = filt_str_mod(str(data["info"]["playlist"]))
                        make_asset(location, "w", data, 4)

                        embed.set_author(name=f'Removed the song "{song}"')

                        await ctx.send(embed=embed)
                else:
                    raise commands.errors.NotOwner("User is not the owner of this playlist.")

            except commands.errors.NotOwner:
                await sendEmbed(embed, ctx, f"You're not the owner of this playlist.")
        except AttributeError:
            await sendEmbed(embed, ctx, "Missing Arguments (/rsong <Playlist Name>, <Song> Remember to add a comma between the Playlist Name and The song)")
    except FileNotFoundError:
        await sendEmbed(embed, ctx, f"No playlist with the name {playlist_name}")

@client.command(aliases=["at"])
async def atag(ctx):

    args = parseArgs(ctx)
    embed = discord.Embed(color=LIGHT_BLUE)
    text = None

    try:
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


    except IndexError:
        text = f"Missing Arguments, please look at the usage for this command by doing {CLIENT_PREFIX}usage 2"

    finally:
        await sendEmbed(embed, ctx, text)

@client.command(aliases=["pt"])
async def playliststag(ctx, *, tag):

    tegsReturn = findPlaylistTags(tag)
    embed = discord.Embed(color=LIGHT_BLUE)

    if len(tegsReturn) <= 0:
        embed.set_author(name="Ø No playlists matching that tag.")
    else:
        embed.set_author(name="Ø Here are some popular playlists matching that tag")

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
    commandList = ["picture", "color", "description", "help", "playscript"]

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
                        sentence = []

                        for x in range(2, len(args)):
                            sentence.append(args[x])

                        description = ", ".join(sentence)

                        playlistData["metadata"]["playlist-description"] = description
                        embed.set_author(name="I have set the playlist description (I am not going to preview it incase the description is too big, that can cause some programming issues.)")
                        make_asset(path, "w", playlistData, 4)

                    elif command == commandList[3]:

                        embed.set_author(name="Editing Playlist Help")
                        embed.add_field(name="To edit your playlist description, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist description, <Your playlist name>, <Your description> (Will change you playlist description this is public, so be careful with what you chose, can be in any language, or just anything that is UNICODE)", inline=False)
                        embed.add_field(name="To edit your playlist Image, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist picture, <Your playlist name>, <Image URL> (Will change your playlist Thumbnail, this is public, so be careful with what you chose, and it has to be a valid image URL Any Image that gets uploaded to discord is a valid image that you can use)", inline=False)
                        embed.add_field(name="To edit your playlist colour, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist color, <Your playlist name>, <Color> (This will change your embed color, if you don't want to pick a pre-set color, you can use RGB Values, Example: /eplaylist color, <Your Playlist>, 155, 155, 255 For a light blue)", inline=False)
                        embed.add_field(name="To edit your PlayScript, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist playscript, <Your playlist name>, <Order> (PlayScript is a feature where: if you have a playlist, but the order of songs is not right for you, you can reorder them in the order you want. Example > https://www.youtube.com/watch?v=ylVPnQuVwoI)", inline=False)
                        embed.set_footer(text="Note Ø Here is a list of colours, > blue, red, yellow, green, white, light blue, I will add more as time goes on, and you can can add your own colours by using RGB Values, like 0, 128, 255 for a light blue.")

                    elif command == commandList[4]:

                        reA = []
                        playlistData = return_data(path)

                        for x in range(2, len(args)):
                            reA.append(args[x])

                        playlistData["metadata"]["playscript"] = reA
                        playlistData["metadata"]["og-playscript"] = reA

                        make_asset(path, "w", playlistData, 4)

                        embed.set_author(name=f"PlayScript Ø {reA}")

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
        embed.add_field(name="To edit your playlist description, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist description, <Your playlist name>, <Your description> (Will change your playlist description this is public, so be careful with what you chose, can be in any language, or just anything that is UNICODE)", inline=False)
        embed.add_field(name="To edit your playlist Image, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist picture, <Your playlist name>, <Image URL> (Will change your playlist Thumbnail, this is public, so be careful with what you chose, and it has to be a valid image URL Any Image that gets uploaded to discord is a valid image that you can use)", inline=False)
        embed.add_field(name="To edit your playlist colour, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist color, <Your playlist name>, <Color> (This will change your embed color, if you don't want to pick a pre-set color, you can use RGB Values, Example: /eplaylist color, <Your Playlist>, 155, 155, 255 For a light blue)", inline=False)
        embed.add_field(name="To edit your PlayScript, do the following command Ø ", value=f"{CLIENT_PREFIX}eplaylist playscript, <Your playlist name>, <Order> (PlayScript is a feature where: if you have a playlist, but the order of songs is not right for you, you can reorder them in the order you want. Example > https://www.youtube.com/watch?v=ylVPnQuVwoI)", inline=False)
        embed.set_footer(text="Note Ø Here is a list of colours, > blue, red, yellow, green, white, light blue, I will add more as time goes on, and you can can add your own colours by using RGB Values, like 0, 128, 255 for a light blue.")

    finally:
        await ctx.send(embed=embed)

@client.command()
async def link(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)
    args = parseArgs(ctx)
    sendEmbed = True
    done = False

    try:
        if len(args) >= 1:

            command = args[0]
            authorID = ctx.author.id
            linkLocation = f"{user_location}\\{ctx.guild.id}\\{authorID}\\{authorID}-links.json"

            if command == "make":
                try:
                    try:
                        linkedServers = args[1]
                        guildPath = f"{guild_location}\\{linkedServers}\\{linkedServers}-LINKS.json"

                        userGlobalPath = f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json"
                        globalData = return_data(userGlobalPath)

                        guildLinkData = return_data(guildPath)
                        memberData = return_data(linkLocation)
                        linkedServersName = client.get_guild(int(linkedServers))

                        if linkedServers == str(ctx.guild.id) and guildLinkData is not None:
                            await ctx.send("You cannot make a link to THIS server :joy:")
                            sendEmbed = False
                        else:
                            if memberData["member-link"]["link-enabled"] != True:
                                embed.set_author(name=f'Link is not enabled. To enable it, do this command "{CLIENT_PREFIX}link link, True"')
                            else:

                                if globalData["global"]["has-link"] is True:
                                    embed.set_author(name="You already have a link.")
                                else:

                                    await ctx.send('Are you sure? this will delete any Profile Experience data you have on this server, and the server you want to make the link with. (This will not delete playlists nor your playlist records)(Type: "True" to continue, Type: "False" or any other text to exit)')

                                    while done is False:

                                        args = await client.wait_for('message')
                                        args = getUserArgs(ctx, args)

                                        if args == "True":

                                            memberData["member-link"]["links"].append(linkedServers)
                                            memberData["member-link"]["links"].append(f"{ctx.guild.id}")
                                            globalData["global"]["has-link"] = True
                                            globalData["global"]["link-id"] = str(linkedServers)
                                            globalData["global"]["link-made-id"] = str(ctx.guild.id)


                                            guildLinkData["guild-links"][f"{ctx.author.id}"] = []
                                            guildLinkData["guild-links"][f"{ctx.author.id}"].append(f"{ctx.author.id}")
                                            guildLinkData["guild-links"][f"{ctx.author.id}"].append(f"{ctx.guild.id}")


                                            make_asset(linkLocation, "w", memberData, 4)
                                            make_asset(guildPath, "w", guildLinkData, 4)
                                            make_asset(userGlobalPath, "w", globalData, 4)

                                            embed.set_author(name=f"Added '{linkedServersName}' to your link")
                                            done = True
                                        elif args == None:
                                            pass
                                        else:
                                            await ctx.send("Cancelled Link")
                                            done = True
                                            sendEmbed = False

                    except IndexError:
                        return

                except TypeError:
                    embed.set_author(name="Error")
                    embed.add_field(name="Help > ", value=f"I cannot find the specified server, remember, you need to put in a server ID, not the name. Example, the server ID you sent this message in, is {ctx.guild.id} (PS: You need developer mode to get the ID, search on google of how to do that, Good luck, and I'm sorry this is so complicated...)")
            elif command == "link":
                try:
                    value = args[1]

                    actualValue = (value == "True")
                    memberData = return_data(linkLocation)

                    memberData["member-link"]["link-enabled"] = actualValue
                    embed.set_author(name=f"Link is now {actualValue} (Note: if you put anything other than True or False, it will default to False.)")

                    make_asset(linkLocation, "w", memberData, 4)
                except IndexError:
                    pass

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
                embed.set_author(name=f"'{command}' is not a link attribute, here is some help")

                embed.add_field(name=f"{CLIENT_PREFIX}link link, <True | False>", value='This will just enable or disable your link, "True" to enable, "False" to disable')
                embed.add_field(name=f"{CLIENT_PREFIX}link make, <Server ID>", value="Will make a link to another server (You will earn EXP on both servers, and will be counted on one account)")
                embed.add_field(name=f"{CLIENT_PREFIX}link remove", value="Will remove your link, you can reconnect later")

                sendEmbed = False
                await ctx.send(embed=embed)

        else:
            raise IndexError

    except AttributeError as e:
        embed.set_author(name=f"Missing Arguments, Actual Console Error>{e}")

    finally:
        if sendEmbed is True:
            try:
                await ctx.send(embed=embed)
            except discord.errors.HTTPException:
                await ctx.send("Missing Arguments")
        else:
            return

@client.command()
async def lyrics(ctx):
    try:
        try:
            args = parseArgs(ctx)
            await ctx.send(f"Searching for: {args[1]}\n\nBy: {args[0]}")
            artist = genius.search_song(args[1], args[0])

            if artist is None:
                await ctx.send(f'No song with the name "{args[1]}" by "{args[0]}"')
            else:
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

@client.command()
@commands.is_owner()
async def database(ctx):
    text = "No data"
    args = parseArgs(ctx, Type="url")


    try:
        path = args[0]
    except IndexError:
        path = args[0]

    try:
        dataPath = f"{file_path}\\{path}"
        if path.endswith(".json"):
            data = return_data(dataPath, ty="text")
        else:
            data = os.listdir(dataPath)

        text = f"{data}\n\n\nDATA PATH: Database\\{path}"
    except Exception as e:
        text = f"ERROR @ {e}"

    await ctx.send(text)

@client.command()
@commands.has_permissions(administrator=True)
async def sell(ctx):

    args = parseArgs(ctx, Type="url")
    guildID = str(ctx.guild.id)
    bankLocation = f"{guild_location}\\{guildID}\\{guildID}-INVENTORY.json"
    text = "CHECK CONSOLE FOR ERROR"
    count = None
    bankData = return_data(bankLocation)

    try:
        strn = args[0]
        itemType = args[1]

        if strn == "Sami" or strn == "sami":
            text = "You cannot name a an item with this name, it represents a dark past."
        else:
            strnSplit = strn.split(" ")
            e = []

            for x in range(len(strnSplit)):
                e.append(strnSplit[x])

                strn = "-".join(e)

            if itemType == "role":

                try:
                    role = args[2]
                    description = args[3]
                    price = args[4]
                    count = int(args[5])

                except IndexError:
                    count = None

                finally:
                    try:

                        roleID = discord.utils.get(client.get_guild(int(guildID)).roles, name=role)


                        bankData[guildID]["items"].append(strn)
                        bankData[f"{guildID}"]["guild-items"][strn] = {
                        "role-name": roleID.id,
                        "role-description": description,
                        "role-price": price,
                        "item-type": itemType,
                        "buy-count": count
                        }

                        make_asset(bankLocation, "w", bankData, 4)

                        if count is None:
                            realCount = "Unlimited"
                        else:
                            realCount = count


                    except AttributeError:
                        text = f'No role with the name "{role}" (Note: It has to be spelling perfect) :D'

                    finally:
                        text = f"Made Role for sale in shop:\n\n**Item Name**\n{args[0]}\n\n**Role Name**\n{role}\n\n**Role Description**\n{description}\n\n**Role Price**\n{price}$\n\n**Item Displayname and Codename**\n{strn}\n\n**Item Stock**\n{realCount}"


            elif itemType == "text":
                try:
                    itemText = args[2]
                    description = args[3]
                    price = args[4]
                    count = int(args[5])
                except IndexError:
                    count = None

                finally:

                    bankData[guildID]["items"].append(strn)
                    bankData[f"{guildID}"]["guild-items"][strn] = {
                    "role-name": itemText,
                    "role-description": description,
                    "role-price": price,
                    "item-type": itemType,
                    "buy-count": count
                    }

                    make_asset(bankLocation, "w", bankData, 4)

                    if count is None:
                        realCount = "Unlimited"
                    else:
                        realCount = count

                    text = f"Made Message for sale in shop:\n\n**Item Name**\n{args[0]}\n\n**Message Description**\n{description}\n\n**Message Price**\n{price}$\n\n**Item Displayname and Codename**\n{strn}\n\n**Item Stock**\n{realCount}\n\n\n*note: If you want to change anything in this item.\nYou will have to delete this item with /remove\nAnd remake it.*"
                    await ctx.author.send(f"{bankData[f'{guildID}']['guild-items'][strn]}\n\n\n\nNOTE: THIS IS YOUR SHOP ITEM IN RAW FORM, IN THE FUTURE i AM PLANNING TO MAKE IT SO YOU CAN MAKE A SHOP ITEM WITH\nTHIS TEMPLATE, IF YOU DO NOT KNOW HOW TO PROGRAM IN JSON, i WILL GIVE YOU INSTRUCTIONS SOON.\n\nEnjoy ^^")




            else:
                text = f'No item type matching the name "{itemType}"'
    except IndexError:
        text = "Missing Arguments"

    finally:
        await ctx.send(text)


@client.command()
async def buy(ctx):

    args = parseArgs(ctx)
    guildID = str(ctx.guild.id)
    memberID = str(ctx.author.id)

    done1 = False

    guildShopPath = f"{guild_location}\\{guildID}\\{guildID}-INVENTORY.json"
    userBankPath = f"{user_location}\\{guildID}\\{memberID}\\{memberID}-bank.json"

    guildShopData = return_data(guildShopPath)
    userBankData = return_data(userBankPath)

    itemName = replaceSpaces(args[0])

    if itemName in guildShopData[guildID]["guild-items"]:

        if int(userBankData[memberID]["balance"]) >= int(guildShopData[guildID]["guild-items"][itemName]["role-price"]):
            if 1 > 0:

                roleID = guildShopData[guildID]["guild-items"][itemName]["role-name"]
                roleName = ctx.guild.get_role(roleID)

                await ctx.send(f'Are you sure you want to buy "{itemName}" for {guildShopData[guildID]["guild-items"][itemName]["role-price"]}$? (Reply "True" to continue with purchase, type anything else to cancel)')

                while done1 is False:
                    args_ = await client.wait_for('message')
                    args_ = getUserArgs(ctx, args_)

                    if args_ == "True":

                        if guildShopData[guildID]["guild-items"][itemName]["item-type"] == "role":
                            await ctx.author.add_roles(roleName)
                            await ctx.send(f'You have bought the role "{itemName}" for {guildShopData[guildID]["guild-items"][itemName]["role-price"]}$!')

                        elif guildShopData[guildID]["guild-items"][itemName]["item-type"] == "text":
                            await ctx.author.send(f"Message > {guildShopData[guildID]['guild-items'][itemName]['role-name']}")

                        else:

                            done1 = True

                        userBankData[memberID]["balance"] = int(userBankData[memberID]["balance"])-int(guildShopData[guildID]["guild-items"][itemName]["role-price"])
                        guildShopData[guildID]["guild-balance"] = int(guildShopData[guildID]["guild-balance"])+int(guildShopData[guildID]["guild-items"][itemName]["role-price"])


                        if guildShopData[guildID]["guild-items"][itemName]["buy-count"] is None:
                            pass
                        else:
                            guildShopData[guildID]["guild-items"][itemName]["buy-count"] = guildShopData[guildID]["guild-items"][itemName]["buy-count"]-1

                            if guildShopData[guildID]["guild-items"][itemName]["buy-count"] == 0:

                                guildShopData[guildID]["items"].remove(itemName)
                                del guildShopData[guildID]["guild-items"][itemName]
                            else:
                                pass

                        make_asset(guildShopPath, "w", guildShopData, 4)
                        make_asset(userBankPath, "w", userBankData, 4)

                        done1 = True

                    else:
                        return await ctx.send("Cancelled Purchase")




        else:
            return await ctx.send("Your too poor to buy this item")
    else:
        return await ctx.send(f'No item with the name "{args[0]}"')

@client.command()
@commands.has_permissions(administrator=True)
async def bank(ctx):

    text = "error"
    embed = discord.Embed(color=LIGHT_BLUE)
    sendMessage = True

    try:
        args = parseArgs(ctx)
        command = args[0]

        guildID = str(ctx.guild.id)
        ownerID = str(ctx.author.id)

        guildBankPath = f"{guild_location}\\{guildID}\\{guildID}-INVENTORY.json"
        ownerBankPath = f"{user_location}\\{guildID}\\{ownerID}\\{ownerID}-bank.json"

        if command == "claim":
            guildBankData = return_data(guildBankPath)
            ownerBankData = return_data(ownerBankPath)

            ownerBankData[ownerID]["balance"] = ownerBankData[ownerID]["balance"]+guildBankData[guildID]["guild-balance"]
            guildBankData[guildID]["guild-balance"] = 0

            make_asset(guildBankPath, "w", guildBankData, 4)
            make_asset(ownerBankPath, "w", ownerBankData, 4)

            text = f"I have taken all cash from the server' balance, your balance is now {ownerBankData[ownerID]['balance']}"

        elif command == "balance":
            guildBankData = return_data(guildBankPath)
            text = f"The guilds balance is {guildBankData[guildID]['guild-balance']}$"

        elif command == "help":
            embed.set_author(name="Bank Help")

            embed.add_field(name=f"{CLIENT_PREFIX}bank claim", value="Claims all money that is in the guilds account, whomever may use this command will get all of the royalties. (Note: Only administrators and owner can do this command)", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}bank balance", value="Shows how much the guild has in savings (You can get money buy making items in your shop)", inline=False)

            sendMessage = False
            return await ctx.send(embed=embed)



        else:
            embed.set_author(name="Bank Help")

            embed.add_field(name=f"{CLIENT_PREFIX}bank claim", value="Claims all money that is in the guilds account, whomever may use this command will get all of the royalties. (Note: Only administrators and owner can do this command)", inline=False)
            embed.add_field(name=f"{CLIENT_PREFIX}bank balance", value="Shows how much the guild has in savings (You can get money buy making items in your shop)", inline=False)

            sendMessage = False
            return await ctx.send(embed=embed)

    except IndexError:
        text = "Missing Arguments"

    finally:
        if sendMessage is True:
            await ctx.send(text)

@client.command()
async def shop(ctx):
    embed = discord.Embed(color=LIGHT_BLUE)

    guildID = str(ctx.guild.id)

    guildBankPath = f"{guild_location}\\{guildID}\\{guildID}-INVENTORY.json"
    guildBankData = return_data(guildBankPath)
    configLocation = return_data(f"{config_location}\\{ctx.guild.id}\\config.json")

    try:
        embed.set_author(name=configLocation["config"]["shop_name"])
    except:
        embed.set_author(name=f"{ctx.guild}s Shop")
    try:
        embed.set_image(url=configLocation["config"]["shop_image"])
    except:
        embed.set_image(url=vorbis_img2)

    finally:
        for x in range(len(guildBankData[guildID]["items"])):

            currentItem = guildBankData[guildID]["items"][x]
            daysLeft = None

            if guildBankData[guildID]['guild-items'][currentItem]['buy-count'] is None:
                daysLeft = "Unlimited"
            else:
                daysLeft = guildBankData[guildID]['guild-items'][currentItem]['buy-count']

            embed.add_field(name=f"Item {x+1}", value="\u200b", inline=False)
            embed.add_field(name=f"Item {x+1} Name  Ø  ", value=f"{currentItem}", inline=False)
            embed.add_field(name=f"Item {x+1} Description  Ø  ", value=f"{guildBankData[guildID]['guild-items'][currentItem]['role-description']}", inline=False)
            embed.add_field(name=f"Item {x+1} Price  Ø  ", value=f"{guildBankData[guildID]['guild-items'][currentItem]['role-price']}$", inline=False)
            embed.add_field(name=f"Item {x+1} Stock  Ø  ", value=daysLeft, inline=False)
            embed.add_field(name=f"Item {x+1} Command  Ø  ", value=f"{CLIENT_PREFIX}buy {currentItem}", inline=False)

            embed.add_field(name="\u200b", value="\u200b", inline=False)

        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def remove(ctx):

    try:
        args = parseArgs(ctx)
        shopItem = replaceSpaces(args[0])
        text = "Error"

        guildID = str(ctx.guild.id)
        guildShopPath = f"{guild_location}\\{guildID}\\{guildID}-INVENTORY.json"
        guildShopData = return_data(guildShopPath)

        try:
            del guildShopData[guildID]["guild-items"][shopItem]
            guildShopData[guildID]["items"].remove(shopItem)

            make_asset(guildShopPath, "w", guildShopData, 4)

            text = f'Deleted shop item: "{shopItem}"'
        except KeyError:
            text = f'No item with the name "{shopItem}"'
    except IndexError:
        text = "Missing Arguments"

    finally:
        await ctx.send(text)

@client.command()
async def ahu(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)

    embed.set_author(name="Administration Command Usage")

    embed.add_field(name=":fist:  Punishment Command Usage  :fist:", value="\u200b", inline=False)
    embed.add_field(name=f"{CLIENT_PREFIX}kick", value=f"{CLIENT_PREFIX}kick <Mention Player> <Reason (Optional)>")
    embed.add_field(name=f"{CLIENT_PREFIX}ban", value=f"{CLIENT_PREFIX}ban <Mention Player> <Reason (Optional)>")
    embed.add_field(name=f"{CLIENT_PREFIX}warn", value=f"{CLIENT_PREFIX}warn <Mention Player> <Reason>")
    embed.add_field(name=":star:  General Administration Command Usage  :star:", value="\u200b", inline=False)
    embed.add_field(name=f"{CLIENT_PREFIX}leave", value=f"{CLIENT_PREFIX}leave")
    embed.add_field(name=f"{CLIENT_PREFIX}server", value=f"{CLIENT_PREFIX}server help")
    embed.add_field(name=f"{CLIENT_PREFIX}purge", value=f"{CLIENT_PREFIX}purge <Amount of Messages>")
    embed.add_field(name=f"{CLIENT_PREFIX}unban", value=f"{CLIENT_PREFIX}unban <Player name and tag, Example: Samy#4995>")
    embed.add_field(name=":money_with_wings:  Administrator Economy Commands  :money_with_wings:", value="\u200b", inline=False)
    embed.add_field(name=f"{CLIENT_PREFIX}bank", value=f"{CLIENT_PREFIX}bank help")
    embed.add_field(name=f"{CLIENT_PREFIX}sell", value=f"{CLIENT_PREFIX}sell <Item Name>, <Item Type (It can be role, or text)>, <Message you want to send player, or the role name depending on what you chose>, <Description of item>, <Price>, <Stock (Optional)>")
    embed.add_field(name=f"{CLIENT_PREFIX}remove", value=f"{CLIENT_PREFIX}remove <Item Name>")
    await ctx.send(embed=embed)

@client.command()
async def comment(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)
    args = parseArgs(ctx)
    metadata = return_data(metadata_location+f"\\{ctx.guild.id}\\payload-data.json")
    fullPlaylistLocation = playlist_location+f"\\{metadata['data']['queued-playlist']}\\{metadata['data']['queued-playlist']}.json"
    playlistLocalLocation = return_data(fullPlaylistLocation)
    messageText = None

    if playlistLocalLocation is None:
        await ctx.send("You have no playlist that is queued")
    else:
        try:
            messageText = args[0]

            playlistLocalLocation["metadata"]["playlist-comment-count"] = playlistLocalLocation["metadata"]["playlist-comment-count"]+1
            playlistLocalLocation["metadata"]["playlist-comments"][playlistLocalLocation["metadata"]["playlist-comment-count"]] = {
                "comment-author": ctx.author.id,
                "comment-guild": ctx.guild.id,
                "comment-text": messageText,
                "comment-publish": str(datetime.datetime.now()).split(".")[0]

            }
        except IndexError:
            await ctx.send("You cannot send an empty message.")

        finally:
            make_asset(fullPlaylistLocation, "w", playlistLocalLocation, 4)

            embed.set_author(name="Posted Comment")
            embed.add_field(name="Comment Text", value=messageText)
            embed.set_footer(text=f"Your comment ID is {playlistLocalLocation['metadata']['playlist-comment-count']}, you may use this while searching for your comment, Example: {CLIENT_PREFIX}read {metadata['data']['queued-playlist']}, {playlistLocalLocation['metadata']['playlist-comment-count']}")

            await ctx.send(embed=embed)

@client.command()
async def read(ctx):

    embed = discord.Embed(color=LIGHT_BLUE)
    args = parseArgs(ctx)
    numbers = []
    chosen_numbers = []
    specifiedComment = None
    try:
        playlist = args[0]
        playlistPath = playlist_location+f"\\{playlist}\\{playlist}.json"
        playlistData = return_data(playlistPath)

        try:
            specifiedComment = int(args[1])
        except IndexError:
            pass

        if playlistData["metadata"]["playlist-comment-count"] == 0:
            await ctx.send("This playlist has no comments.")
        else:
            for x in range(playlistData["metadata"]["playlist-comment-count"]):
                numbers.append(x)

            if isinstance(specifiedComment, int):
                try:
                    embed.set_author(name=f"Comment Number {specifiedComment}")

                    y = specifiedComment
                    author = client.get_user(playlistData["metadata"]["playlist-comments"][str(y)]["comment-author"])
                    guild = client.get_guild(int(playlistData["metadata"]["playlist-comments"][str(y)]["comment-guild"]))
                    text = playlistData["metadata"]["playlist-comments"][str(y)]["comment-text"]
                    time = playlistData["metadata"]["playlist-comments"][str(y)]["comment-publish"]

                    embed.add_field(name=f"At: {time} From: {guild}, User: {author}", value=text, inline=False)
                except KeyError:
                    return await ctx.send(f"There is no comment up to that entry, (Note: you chose a comment by either doing {CLIENT_PREFIX}read <The playlist you want to read comments from>\nor: {CLIENT_PREFIX}read <The playlist you want to read comments from>, <The comment number>\nYou can get how many comments there are by doing:\n{CLIENT_PREFIX}read <The playlist you want to read comments from>\,And it will say at the bottom of the embed message)")
            else:
                embed.set_author(name="Playlist Comments")

                for x in range(5):

                    y = random.choice(numbers)+1

                    if y in chosen_numbers:
                        continue
                    else:

                        author = client.get_user(playlistData["metadata"]["playlist-comments"][str(y)]["comment-author"])
                        guild = client.get_guild(int(playlistData["metadata"]["playlist-comments"][str(y)]["comment-guild"]))
                        text = playlistData["metadata"]["playlist-comments"][str(y)]["comment-text"]
                        time = playlistData["metadata"]["playlist-comments"][str(y)]["comment-publish"]

                        embed.add_field(name=f"At: {time} From: {guild}, User: {author}", value=text, inline=False)
                        chosen_numbers.append(y)

                if playlistData['metadata']['playlist-comment-count'] == 1:
                    embed.set_footer(text=f"There is {playlistData['metadata']['playlist-comment-count']} comment on this playlist")
                else:
                    embed.set_footer(text=f"There are {playlistData['metadata']['playlist-comment-count']} comments on this playlist")

            await ctx.send(embed=embed)

    except IndexError:
        await ctx.send(f"You've not chosen a playlist you want to read comments from")

@client.command()
async def credit(ctx):

    austin, fabian = 400089431933059072, 533285613021954049
    austinName, fabianName = client.get_user(austin), client.get_user(fabian)

    await ctx.send(f"THis bot is made by:\n\n{austinName} & {fabianName}\nBoth on discord")

@client.command()
async def sendfeedback(ctx):
    args = parseArgs(ctx)

    feedbackChannel = client.get_channel(844571632190095401)

    await feedbackChannel.send(f"Feedback from: {ctx.author}\nMember ID: {ctx.author.id}\n\nFeedback: {args}")
    await ctx.send("The feedback has been sent to the testing guild. Thank you so much for the feedback! -Austin")

@client.command()
async def delete(ctx):
    args = parseArgs(ctx)

    try:
        playlist = args[0]
        messageID = args[1]

        try:
            playlistAddress = f"{playlist_location}\\{playlist}\\{playlist}.json"
            playlistData = return_data(playlistAddress)

            if messageID in playlistData["metadata"]["playlist-comments"].keys():
                if ctx.author.id == playlistData["metadata"]["playlist-comments"][messageID]["comment-author"] or ctx.author.id in playlistData["metadata"]["playlist-author"]:

                    del playlistData["metadata"]["playlist-comments"][messageID]
                    playlistData["metadata"]["playlist-comment-count"] = playlistData["metadata"]["playlist-comment-count"]-1

                    await ctx.send(f"Deleted comment: {messageID}")

                    make_asset(playlistAddress, "w", playlistData, 4)
                else:
                    await ctx.send("You're not the owner of this playlist. Nor are you the author of this comment.")
            else:
                await ctx.send("There is no message with that ID")
        except AttributeError:
            await ctx.send(f'Playlist: "{playlist}" does not exist.')
    except IndexError:
        await ctx.send("Missing Arguments")

@client.command()
async def loop(ctx):

    config_path = f"{config_location}\\{ctx.guild.id}\\config.json"
    config = return_data(config_path)

    if config["config"]["loop"] is True:
        config["config"]["loop"] = False
        await ctx.send("I have turned off looping")
    else:
        config["config"]["loop"] = True
        await ctx.send("I have turned on looping")

    make_asset(config_path, "w", config, 4)


@client.command(aliases=["reload"])
async def restart(ctx):
    await ctx.send("Restarting Script...")

    pyautogui.moveTo(955, 71, duration=1)
    mouse.click("left")

@client.command()
async def chatroom(ctx):
    args = parseArgs(ctx)
    id_letters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', "f", '_', '-', '!']
    global_path = f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json"
    global_data = return_data(global_path)
    privacy_opts = ["public", "private"]

    try:
        if global_data["global"]["chatroom"]["connected-chatroom"] is not None:
            return await ctx.send(f"You're already part of a chatroom, to make a new chatroom, you need to leave the one you're in now. (You can do this with {CLIENT_PREFIX}leave)")

        os.chdir(chatroom_location)

        chatroomName = args[0]
        chatroomPassword = args[1]
        try:
            if args[2] in privacy_opts:
                chatroomPrivacy = args[2]

        except IndexError:
            chatroomPrivacy = "public"

        chat_id = random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)

        if chat_id in os.listdir():
            chat_id = random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)+random.choice(id_letters)
        try:
            os.mkdir(f"{chat_id}")

            chat_data = {}
            chat_data["metadata"] = {
            "password": chatroomPassword,
            "name": chatroomName,
            "id": chat_id,
            "privacy": chatroomPrivacy,
            "made-at": str(datetime.datetime.now()),
            "owner": ctx.author.id,
            "description": f"Welcome to the {chatroomName} chatroom",
            "image": "https://cdn.discordapp.com/attachments/800136030228316170/848925796093657128/bubble_consulting_chat-512.png",
            "user-info": {
                "connected-users": [ctx.author.id],
                "all-users": [ctx.author.id],
                "whitelisted-users": [ctx.author.id]
                },
            "message-data": {
                "messages": {
                    "message-1": {
                        "author": 798867893910765579,
                        "text": f'Welcome to the "{chatroomName}", to send a message, do {CLIENT_PREFIX}chat <Your Message>, {CLIENT_PREFIX}leave to disconnect from this chatroom, Enjoy!',
                        "timestamp": str(datetime.datetime.now())
                        }
                    }
                }
            }

            global_data["global"]["chatroom"]["connected-chatroom"] = chat_id

            make_asset(f"{chatroom_location}\\{chat_id}\\{chat_id}.json", "w", chat_data, 4)
            make_asset(global_path, "w", global_data, 4)

            await ctx.author.send(f"Made Chatroom: {chatroomName}\nChatroom Password: {chatroomPassword}\nChatroom ID (Note: If you want anyone to join this chatroom, you'll need this ID): {chat_id}")
        except Exception as e:
            await ctx.send(f"Error: {e}")
    except IndexError:
        await ctx.send("Missing Arguments")

@client.command()
async def connect(ctx):
    args = parseArgs(ctx)
    try:
        chat_id = args[0]
        password = args[1]

        data = return_data(f"{chatroom_location}\\{chat_id}\\{chat_id}.json")
        global_data = return_data(f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json")


        if global_data["global"]["chatroom"]["connected-chatroom"] == data["metadata"]["id"]:
            await ctx.send("You're already connected to this chatroom.")

        elif global_data["global"]["chatroom"]["connected-chatroom"] is not None:
            chatroom_old = global_data["global"]["chatroom"]["connected-chatroom"]
            chatroom = return_data(f"{chatroom_location}\\{chatroom_old}\\{chatroom_old}.json")

            chatroom["metadata"]["user-info"]["connected-users"].remove(ctx.author.id)

            make_asset(f"{chatroom_location}\\{chatroom_old}\\{chatroom_old}.json", "w", chatroom, 4)



        else:

            if data is not None:
                if str(ctx.author.id) in list(data["metadata"]["user-info"]["banned-users"].keys()):
                    await ctx.send("You're banned from this Chatroom.")
                else:
                    if password == data["metadata"]["password"]:
                        if data["metadata"]["privacy"] == "public" or ctx.author.id == data["metadata"]["owner"]:
                            data["metadata"]["user-info"]["connected-users"].append(ctx.author.id)
                            if ctx.author.id in data["metadata"]["user-info"]["all-users"]:
                                pass
                            else:
                                data["metadata"]["user-info"]["all-users"].append(ctx.author.id)
                            global_data["global"]["chatroom"]["connected-chatroom"] = chat_id

                            make_asset(f"{chatroom_location}\\{chat_id}\\{chat_id}.json", "w", data, 4)
                            make_asset(f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json", "w", global_data, 4)

                            await ctx.send(f"Connected to the chatroom: {data['metadata']['name']}")
                        else:
                            await ctx.send("You're not allowed in this chatroom.")
                    else:
                        await ctx.send("Incorrect Password")
            else:
                await ctx.send(f"No chatroom with the ID: {chat_id} Exists.")
    except IndexError:
        await ctx.send("Missing Arguments")

@client.command()
async def chat(ctx):
    args = parseArgs(ctx, "url")
    global_data = return_data(f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json")
    embed = discord.Embed(color=AZURE)

    try:
        message = ", ".join(args)
        chatroom = global_data["global"]["chatroom"]["connected-chatroom"]

        embed.set_author(name=f"{ctx.author}", icon_url=str(ctx.author.avatar_url))
        embed.add_field(name=message, value="\u200b")
        embed.set_footer(text=f"Sent at {str(datetime.datetime.now()).split('.')[0]}")

        if chatroom is not None:
            chatroom_data = return_data(f"{chatroom_location}\\{chatroom}\\{chatroom}.json")
            if chatroom_data is not None:
                chatroom_data["metadata"]["message-data"]["messages"][f"message-{len(chatroom_data['metadata']['message-data']['messages'].keys())+1}"] = {
                    "author": ctx.author.id,
                    "text": message,
                    "timestamp": str(datetime.datetime.now())
                }

                make_asset(f"{chatroom_location}\\{chatroom}\\{chatroom}.json", "w", chatroom_data, 4)

                for y in range(len(chatroom_data["metadata"]["user-info"]["connected-users"])):
                    try:
                        userID = chatroom_data["metadata"]["user-info"]["connected-users"][y]
                        user = client.get_user(userID)

                    except AttributeError:
                        await user.create_dm()

                    finally:
                        await user.send(embed=embed)
            else:
                await ctx.send("This chatroom no longer exists. You've been disconnected from the chatroom.")
                global_data["global"]["chatroom"]["connected-chatroom"] = None

                make_asset(f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json", "w", global_data, 4)


        else:
            await ctx.send("You're not connected to a chat room.")

    except IndexError:
        await ctx.send("Missing Arguments")

@client.command()
async def leave(ctx):

    global_data = return_data(f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json")

    if global_data["global"]["chatroom"]["connected-chatroom"] is None:
        await ctx.send("You're not connected to a chatroom.")
    else:
        chatroom_data = return_data(f"{chatroom_location}\\{global_data['global']['chatroom']['connected-chatroom']}\\{global_data['global']['chatroom']['connected-chatroom']}.json")
        chatroom_id = global_data['global']['chatroom']['connected-chatroom']

        global_data["global"]["chatroom"]["connected-chatroom"] = None
        chatroom_data["metadata"]["user-info"]["connected-users"].remove(ctx.author.id)

        make_asset(f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json", "w", global_data, 4)
        make_asset(f"{chatroom_location}\\{chatroom_id}\\{chatroom_id}.json", "w", chatroom_data, 4)

        await ctx.send(f"Left Chatroom: {chatroom_data['metadata']['name']}")

@client.command()
async def add(ctx):
    global_data = get_user_asset(ctx, "GlobalProfiles")
    args = parseArgs(ctx)

    try:
        if global_data["global"]["chatroom"]["connected-chatroom"] is not None:
            chat_id = global_data["global"]["chatroom"]["connected-chatroom"]
            chat_data = return_data(f"{chatroom_location}\\{chat_id}\\{chat_id}.json")

            if chat_data["metadata"]["owner"] == ctx.author.id:
                for x in range(len(args)):

                    for args[x] in list(client.users):
                        chat_data["metadata"]["user-info"]["whitelisted-users"].append(client.users[x].id)

                make_asset(f"{chatroom_location}\\{chat_id}\\{chat_id}.json", "w", chat_data, 4)

            else:
                await ctx.send("You're not the owner of this chat room.")

        else:
            await ctx.send("You're not connected to a chatroom.")

    except IndexError:
        await ctx.send(f"You need to add some players, Example: ({ctx.author}, Austin Phoenix Ares#2263)")

@client.command()
async def pull(ctx):
    global_data = get_user_asset(ctx, "GlobalProfiles")
    args = parseArgs(ctx)

    try:
        password = args[0]

        if global_data["global"]["chatroom"]["connected-chatroom"] is not None:
            chat_id = global_data["global"]["chatroom"]["connected-chatroom"]
            chat_data = return_data(f"{chatroom_location}\\{chat_id}\\{chat_id}.json")

            if ctx.author.id == chat_data["metadata"]["owner"]:
                if password == chat_data["metadata"]["password"]:
                    os.remove(f"{chatroom_location}\\{chat_id}\\{chat_id}.json")
                    os.rmdir(f"{chatroom_location}\\{chat_id}")
                    global_data["global"]["chatroom"]["connected-chatroom"] = None

                    make_asset(f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json", "w", global_data, 4)
                    await ctx.send(f"Deleted the chatroom: {chat_data['metadata']['name']}")
                else:
                    await ctx.send("Wrong / No password was entered.")
            else:
                await ctx.send("You're not the owner of this chatroom.")

        else:
            await ctx.send("You're not connected to a chatrooom.")
    except AttributeError:
        await ctx.send(f"Missing Arguments, To delete a chatroom, you need to be connected to it, you need to be the owner, and the password. Example: {CLIENT_PREFIX}delete <Chatroom Password>")

@client.command()
async def edit(ctx):
    global_data = get_user_asset(ctx, "GlobalProfiles")
    embed = discord.Embed(color=AZURE)

    try:
        if global_data["global"]["chatroom"]["connected-chatroom"] is not None:
            chat_id = global_data["global"]["chatroom"]["connected-chatroom"]
            chat_data = return_data(f"{chatroom_location}\\{chat_id}\\{chat_id}.json")

            if chat_data is not None:
                if chat_data["metadata"]["owner"] == ctx.author.id:
                    await ctx.send("What aspect of your chatroom do you want to change?\n*react to this message with the :book: emoji to change description\nreact to this message with the :frame_photo: emoji to change the chatroom thumbnail\nreact with anything else to cancel*")

                    def checkEmj(reaction, member):
                        return member == ctx.author

                    def checkMsg(message):
                        return message.author == ctx.author and message.channel == ctx.channel

                    try:
                        reaction, member = await client.wait_for('reaction_add', timeout=30.0, check=checkEmj)

                    except asyncio.TimeoutError:
                        await ctx.message.add_reaction(client.get_guild(MAIN_GUILD).emojis[14])


                    else:
                        if reaction.emoji == "\U0001f4d6":
                            await ctx.send("Please type the name of your description in chat. You have 60 seconds until I time out")

                            try:
                                message = await client.wait_for('message', timeout=30.0, check=checkMsg)

                            except asyncio.TimeoutError:
                                await ctx.message.add_reaction(client.get_guild(MAIN_GUILD).emojis[14])

                            else:
                                chat_data["metadata"]["description"] = message.content
                                make_asset(f"{chatroom_location}\\{chat_id}\\{chat_id}.json", "w", chat_data, 4)

                                await ctx.send(f"Changed chatroom description to: {message.content}")

                        elif reaction.emoji == "\U0001f5bc\uFE0F":
                            await ctx.send("Please type the URL of the image you want to use. You have 60 seconds until I time out")

                            try:
                                message = await client.wait_for('message', timeout=30.0, check=checkMsg)

                            except asyncio.TimeoutError:
                                await ctx.message.add_reaction(client.get_guild(MAIN_GUILD).emojis[14])

                            else:
                                try:

                                    embed.set_thumbnail(url=message.content)

                                    chat_data["metadata"]["image"] = message.content
                                    make_asset(f"{chatroom_location}\\{chat_id}\\{chat_id}.json", "w", chat_data, 4)

                                    embed.set_author(name=f"Changed chatroom image")


                                    await ctx.send(embed=embed)
                                except discord.errors.HTTPException:
                                    await ctx.send("That is not a valid image.")

                        else:
                            await ctx.send("Cancelled")

                else:
                    await ctx.send("You're not the owner of this chatroom")
            else:
                await ctx.send("The chatroom you were connected to was deleted, You have been disconnected from the chatroom")
                global_data["global"]["chatroom"]["connected-chatroom"] = None

                make_asset(f"{chatroom_location}\\{chat_id}\\{chat_id}.json", "w", global_data, 4)

        else:
            await ctx.send("You're not connected to a chatroom.")

    except AttributeError as e:
        await ctx.send(f"Error: {e}")

@client.command()
async def room(ctx):
    global_data = get_user_asset(ctx, "GlobalProfiles")
    embed = discord.Embed(color=AZURE)
    userList = []

    try:

        if global_data["global"]["chatroom"]["connected-chatroom"] is not None:
            chat_id = global_data["global"]["chatroom"]["connected-chatroom"]
            chat_data = return_data(f"{chatroom_location}\\{chat_id}\\{chat_id}.json")

            if chat_data is not None:

                for x in range(len(chat_data["metadata"]["user-info"]["connected-users"])):
                    user = client.get_user(chat_data["metadata"]["user-info"]["connected-users"][x])
                    userList.append(user.name)

                    users = ", ".join(userList)

                if users == "":
                    users = "No users connected"

                embed.set_author(name=f"{chat_data['metadata']['name']} Chatroom")
                embed.set_image(url=chat_data["metadata"]["image"])

                embed.add_field(name="Chatroom ID: ", value=chat_data["metadata"]["id"], inline=False)
                embed.add_field(name="Chatroom Password: ", value=chat_data["metadata"]["password"], inline=False)
                embed.add_field(name="Privacy: ", value=chat_data["metadata"]["privacy"], inline=False)
                embed.add_field(name="Conceived At: ", value=chat_data["metadata"]["made-at"], inline=False)
                embed.add_field(name="Connected Users: ", value=f"{users}", inline=False)
                embed.add_field(name="Message Count: ", value=len(chat_data["metadata"]["message-data"]["messages"].keys()), inline=False)
                embed.add_field(name="Owner: ", value=client.get_user(chat_data["metadata"]["owner"]), inline=False)
                embed.add_field(name="Description: ", value=chat_data["metadata"]["description"], inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send("The chatroom you were connected to was deleted, You have been disconnected from the chatroom")
                global_data["global"]["chatroom"]["connected-chatroom"] = None

                make_asset(f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json", "w", global_data, 4)

        else:
            raise TypeError
    except TypeError:
        await ctx.send("You're not connected to a chatroom.")

@client.command()
async def boot(ctx):
    args = parseArgs(ctx)
    global_path = f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json"
    global_data = return_data(global_path)

    embed = discord.Embed(color=AZURE)
    players = []

    player = None
    reason = None

    player_x_id = 0
    player_x = None

    try:
        player = args[0]
        try:
            reason = args[1]
        except IndexError:
            reason = "None Specified"
        finally:
                try:
                    chatroom_id = global_data['global']['chatroom']['connected-chatroom']
                    chatroom_data = return_data(f"{chatroom_location}\\{chatroom_id}\\{chatroom_id}.json")

                    if ctx.author.id == chatroom_data["metadata"]["owner"]:

                        player_count = len(chatroom_data["metadata"]["user-info"]["connected-users"])

                        for x in range(player_count):

                            player_x_id = chatroom_data["metadata"]["user-info"]["connected-users"][x]
                            player_x = client.get_user(player_x_id)

                            if player == str(player_x):
                                chatroom_data["metadata"]["user-info"]["connected-users"].remove(player_x_id)

                            else:
                                continue

                        if len(chatroom_data["metadata"]["user-info"]["connected-users"]) == player_count:
                            await ctx.send(f"No player with the name: {player}")
                        else:
                            exiled_user_global = return_data(f"{global_profile}\\{player_x_id}\\{player_x_id}.json")
                            exiled_user_global["global"]["chatroom"]["connected-chatroom"] = None

                            make_asset(f"{chatroom_location}\\{chatroom_id}\\{chatroom_id}.json", "w", chatroom_data, 4)
                            make_asset(global_path, "w", global_data, 4)

                            embed.set_author(name=f"Kicked Player from {chatroom_data['metadata']['name']}")

                            embed.add_field(name="Kicked Player: ", value=player, inline=False)
                            embed.add_field(name="Kick Reason: ", value=reason, inline=False)

                            embed.set_footer(text=str(datetime.datetime.now()))

                            await ctx.send(embed=embed)
                    else:
                        await ctx.send("You're not the owner of this chatroom.")
                except (TypeError, AttributeError):
                    await ctx.send(f"You're not connected to a chatroom.\n\n{e}")

    except IndexError:
        await ctx.send("Missing Arguments")


@client.command()
async def exile(ctx):
    args = parseArgs(ctx)
    global_path = f"{global_profile}\\{ctx.author.id}\\{ctx.author.id}.json"
    global_data = return_data(global_path)

    embed = discord.Embed(color=AZURE)
    players = []

    player = None
    reason = None

    player_x_id = 0
    player_x = None

    try:
        player = args[0]

        try:
            reason = args[1]
        except IndexError:
            reason = "None Specified"
        finally:
                try:
                    chatroom_id = global_data['global']['chatroom']['connected-chatroom']
                    chatroom_data = return_data(f"{chatroom_location}\\{chatroom_id}\\{chatroom_id}.json")

                    if ctx.author.id == chatroom_data["metadata"]["owner"]:

                        player_count = len(chatroom_data["metadata"]["user-info"]["connected-users"])

                        for x in range(player_count):

                            player_x_id = chatroom_data["metadata"]["user-info"]["connected-users"][x-1]
                            player_x = client.get_user(player_x_id)

                            if player == str(player_x):
                                chatroom_data["metadata"]["user-info"]["connected-users"].remove(player_x_id)

                                chatroom_data["metadata"]["user-info"]["banned-users"][player_x_id] = {
                                    "reason": reason,
                                    "time": str(datetime.datetime.now()),
                                    "name": str(player_x)
                                }

                            else:
                                continue

                        if len(chatroom_data["metadata"]["user-info"]["connected-users"]) == player_count:

                            if player == "":
                                return await ctx.send("You need to specify a user.")

                            await ctx.send(f"No player with the name: {player}")
                        else:
                            exiled_user_global = return_data(f"{global_profile}\\{player_x_id}\\{player_x_id}.json")
                            exiled_user_global["global"]["chatroom"]["connected-chatroom"] = None

                            make_asset(f"{chatroom_location}\\{chatroom_id}\\{chatroom_id}.json", "w", chatroom_data, 4)
                            make_asset(global_path, "w", global_data, 4)

                            embed.set_author(name=f"Banned Player from {chatroom_data['metadata']['name']}")

                            embed.add_field(name="Banned Player: ", value=player, inline=False)
                            embed.add_field(name="Ban Reason: ", value=reason, inline=False)

                            embed.set_footer(text=str(datetime.datetime.now()))

                            await ctx.send(embed=embed)
                    else:
                        await ctx.send("You're not the owner of this chatroom.")

                except (TypeError, AttributeError):
                    await ctx.send(f"You're not connected to a chatroom.\n\n{e}")

    except AttributeError:
        await ctx.send("Missing Arguments")

@client.command()
async def excuse(ctx):
    args = parseArgs(ctx)
    global_data = return_data(f"{global_profile}\\{ctx.author.id}\{ctx.author.id}.json")

    try:
        if 1 > 0:

            player = args[0]

            if player == "":
                raise IndexError
            else:
                try:
                    chat_id = global_data["global"]["chatroom"]["connected-chatroom"]
                    chat_data = return_data(f"{chatroom_location}\\{chat_id}\\{chat_id}.json")

                    if chat_data is None:
                        raise FileNotFoundError
                    else:
                        b_player_list = list(chat_data["metadata"]["user-info"]["banned-users"].keys())

                        try:
                            for x in range(len(b_player_list)):
                                player_obj = client.get_user(int(b_player_list[x]))

                                if str(player_obj) == player:
                                    del chat_data["metadata"]["user-info"]["banned-users"][b_player_list[x]]
                                    await ctx.send(f"Excused {player} from {chat_data['metadata']['name']}")

                                    make_asset(f"{chatroom_location}\\{chat_id}\\{chat_id}.json", "w", chat_data, 4)
                                else:
                                    continue

                            if len(b_player_list) == len(chat_data["metadata"]["user-info"]["banned-users"]):
                                await ctx.send(f"No player with the name: ''{player}''")

                        except Exception as e:
                            print(e)

                except FileNotFoundError:
                    await ctx.send(f"FileNotFoundError: Only owners of chatooms can excuse people from being banned.\nIf you have deleted your chatroom, you would have been disconnected automatically.\nAnd I would have said: ''You're not connected to a chatroom''\nBut if you are seeing this, You were not disconnected in your user GlobalProfile Config.\nThis is a fatal error, please get in contact with bot author: Austin Ares\nTo get username, please do {CLIENT_PREFIX}credit")

    except IndexError:
        await ctx.send("Missing Arguments")

@client.command()
async def image(ctx):
    try:
        await ctx.send(f"Note: This is still a work in progress, and this image refreshes everytime you do {CLIENT_PREFIX}profile, here.", file=discord.File(f"{user_location}\\{ctx.guild.id}\\{ctx.author.id}\\profile.png"))
    except FileNotFoundError:
        await ctx.send(f"You don't have a Global Image, do {CLIENT_PREFIX}profile, then do this command again.")

for filename in os.listdir(cog_location):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')

client.run(TOKEN)
