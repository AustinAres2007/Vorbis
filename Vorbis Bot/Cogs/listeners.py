import discord, json, os, datetime, random, requests, shutil, asyncio

from discord.ext import tasks, commands
from discord.utils import get
from PIL import Image, ImageFont, ImageDraw

file_path = "C:\\Users\\Default\\Documents\\Python\\Scripts\\Vorbis"
#file_path = "A:\\Documents\\Python\\Scripts\\Vorbis"

user_location = file_path+"\\Members"
guild_location = file_path+"\\Guilds"
config_location = file_path+"\\Config"
global_profile = file_path+"\\GlobalProfiles"
metadata_location = file_path+"\\Metadata"
queue_location = file_path+"\\Queue"
asset_location = file_path+"\\Assets"
vorbis_img = "https://cdn.discordapp.com/attachments/800136030228316170/802961405296902154/icon2.jpg"

WHITE = discord.Color.from_rgb(255, 255, 255)
TERQ = discord.Color.from_rgb(49,171,159)
RED = discord.Color.from_rgb(255, 0, 0)
YELLOW = discord.Color.from_rgb(255, 255, 0)
LIGHT_BLUE = discord.Color.from_rgb(155, 155, 255)
GREEN = discord.Color.green()
MAGENTA = discord.Color.magenta()
DARK_RED = discord.Color.dark_red()
DARK_BLUE = discord.Color.dark_blue()
DARK_ORANGE = discord.Color.dark_orange()
ORANGE = discord.Color.orange()
PURPLE = discord.Color.purple()

def filt_str_mod(string : str):

    filtered_1 = ''.join(filter(lambda char: char != '"', string))
    filtered_2 = ''.join(filter(lambda char: char != ':', filtered_1))
    filtered_3 = ''.join(filter(lambda char: char != '|', filtered_2))
    filtered_4 = ''.join(filter(lambda char: char != '.wav', filtered_3))
    filtered_5 = ''.join(filter(lambda char: char != ']', filtered_4))
    filtered_6 = ''.join(filter(lambda char: char != '[', filtered_5))
    filtered_7 = ''.join(filter(lambda char: char != "'", filtered_6))

    return filtered_7

def make_asset(file : os.PathLike, mode : str, data : dict=None, indent : int=4):
    if data is None:
        with open(file, mode) as make_file:
            make_file.close()
    with open(file, mode) as make_json:
        json.dump(obj=data, fp=make_json, indent=indent)
        make_json.close()

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

def check_dirfile(path : os.PathLike, Type : str):

    if Type == "dir":
        if os.path.isdir(path):
            return True
        else:
            return False

    elif Type == "file":
        if os.path.isfile(path):
            return True
        else:
            return False
    else:
        raise TypeError(f"There is no file type with the type: {Type}! (Chose only > dir | file)")

class listeners(commands.Cog):

    def __init__(self, client):
        print("Loaded Listeners")
        self.client = client





    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id == 798867893910765579:
            return

        channel = None
        member = message.author
        main_usr_data = return_data(f"{user_location}\\{message.guild.id}\\{message.author.id}\\{message.author.id}.json")
        true_false = [True, False, True, None]

        #if random.choice(true_false) is True:
        #    pass
        #else:
        #    return

        try:
            if return_data(f"{config_location}\\{message.guild.id}\\config.json", "config", "log_channel") is not None:
                pass
            else:
                channel = self.client.get_channel(message.channel.id)

            try:
                guild = f"\\{message.guild.id}"
                full_user_path = user_location+guild
                channel_path = f"{config_location}\\{message.guild.id}\\config.json"

            except AttributeError:
                pass



            usr_exp = 0
            until_nxt_lvl = None
            usr_lvl = 0

            embed = discord.Embed(color=message.author.colour)
            member_id = message.author.id

            def make_plr():

                name = message.author.name
                avatar = message.author.avatar_url

                with open(f"{full_user_path}\\{member_id}\\{member_id}.json", "w+") as write_member:
                    global_path = global_profile+f"\\{message.author.id}"

                    if check_dirfile(global_path, Type="dir") != True:
                        os.makedirs(global_path)

                        if check_dirfile(global_path+f"\\{message.author.id}.json", "file") != True:

                            global_data = {}
                            global_data["global"] = ({
                                "has-link": False,
                                "link-id": None,
                                "playlist-list": {},
                                "listened-playlist-list": [],
                                "auto-correct": {
                                    "failure": {
                                        "failure-name": None,
                                        "command-completion": False,
                                        "failure-count": 0,
                                        "correct-playlist": None
                                    }
                                },
                                "chatroom": {
                                    "connected-chatroom": None
                                }
                            })
                            make_asset(global_path+f"\\{message.author.id}.json", "w", global_data, indent=4)

                    member_metadata = {}

                    member_metadata[f'{member_id}'] = ({
                        "member-id": str(member_id),
                        "member-name": str(name),
                        "member-avatar": str(avatar),
                        "member-joindate": str(message.author.joined_at)
                    })

                    member_metadata[f'progress-bar'] = ({
                        "progress-bar-count": 0
                    })
                    json.dump(member_metadata, write_member, indent=4)

                    write_member.close()

            try:

                with open(full_user_path+f"\\{member_id}\\{member_id}-exp.json", "r") as read_current_level:

                    text = read_current_level.read()
                    json_readable = json.loads(text)

                    usr_exp = json_readable[f'{member_id}']['member-exp']
                    usr_lvl = json_readable[f'{member_id}']['member-level']
                    until_nxt_lvl = json_readable[f'{member_id}']['member-until-next-lvl']

                    read_current_level.close()

                    with open(full_user_path+f"\\{message.author.id}\\{message.author.id}-exp.json", "w") as write_data:

                        userBankPath = f"{user_location}\\{message.guild.id}\\{member_id}\\{member_id}-bank.json"
                        userBankData = return_data(userBankPath)

                        data = {}
                        numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                        level_numbers = [50, 60, 70, 80, 90, 100]

                        if message.guild.premium_tier == 0:
                            new_exp = usr_exp+1
                            userBankData[f"{member_id}"]["balance"] = userBankData[f"{member_id}"]["balance"]+5
                        elif message.guild.premium_tier == 1:
                            new_exp = usr_exp+2
                            userBankData[f"{member_id}"]["balance"] = userBankData[f"{member_id}"]["balance"]+10
                        elif message.guild.premium_tier == 2:
                            new_exp = usr_exp+3
                            userBankData[f"{member_id}"]["balance"] = userBankData[f"{member_id}"]["balance"]+15

                        make_asset(userBankPath, "w", userBankData, 4)

                        if new_exp >= until_nxt_lvl:


                            until_nxt_lvl = int(random.choice(level_numbers))
                            curnt_time = str(datetime.datetime.now())

                            new_exp = 0
                            usr_lvl = usr_lvl+1
                            role = None
                            next_milestone = None

                            if usr_lvl in numbers:
                                role = discord.utils.get(self.client.get_guild(message.guild.id).roles, name=f"Level {usr_lvl}")
                                if usr_lvl == 10:
                                    pass
                                else:
                                    roleToRemove = discord.utils.get(self.client.get_guild(message.guild.id).roles, name=f"Level {usr_lvl-10}")
                            else:
                                for x in range(len(numbers)):
                                    if usr_lvl < numbers[x] and usr_lvl > numbers[x-1]:
                                        next_milestone = numbers[x]

                            if next_milestone is None:
                                next_milestone = usr_lvl+10
                            if usr_lvl >= 100:
                                next_milestone = "No more milestones"

                            main_usr_data["progress-bar"]["progress-bar-count"] = 0

                            embed.set_author(name="Level Up \u200b")
                            embed.set_image(url=message.author.avatar_url)

                            embed.add_field(name=f"Ø   {message.author} levelled up to level {usr_lvl}!", value="\u200b")
                            embed.add_field(name=f"Ø   Next milestone   Ø   {next_milestone}", value="\u200b", inline=False)

                            embed.set_footer(text="Time of Level Up Ø {}  UTC".format(curnt_time.split(".")[0]))



                            if channel is not None:
                                await channel.send(embed=embed)
                            else:
                                await self.client.get_guild(message.guild.id).get_channel(message.channel.id).send(embed=embed)

                            if role is not None:
                                await message.author.add_roles(role)
                                if usr_lvl == 10:
                                    pass
                                else:
                                    await message.author.remove_roles(roleToRemove)
                            else:
                                pass

                        if usr_exp % 2 == 0:
                            pass
                        else:
                            main_usr_data["progress-bar"]["progress-bar-count"] = main_usr_data["progress-bar"]["progress-bar-count"]+1

                        data[member_id] = ({
                            "member-exp": new_exp,
                            "member-level": usr_lvl,
                            "member-until-next-lvl": until_nxt_lvl

                        })

                        userID = str(message.author.id)

                        globalData = return_data(global_profile+f"\\{member_id}\\{member_id}.json")
                        serverLinks = return_data(f"{guild_location}\\{message.guild.id}\\{message.guild.id}-LINKS.json")["guild-links"]
                        userLinks = return_data(f"{full_user_path}\\{userID}\\{userID}-links.json")
                        userMetadata = return_data(metadata_location+f"\\{message.guild.id}\\payload-data.json")
                        userMetadata['data']['message-id'] = message.id

                        if userID in serverLinks:

                            if serverLinks["links-enabled"]:

                                linkedData = f"{serverLinks[userID]}".split("'")
                                userData = f"{user_location}\\{linkedData[3]}\\{linkedData[1]}\\{linkedData[1]}-exp.json"

                                make_asset(userData, "w", data, 4)

                        if userLinks["member-link"]["link-enabled"]:
                            try:
                                link = int(userLinks["member-link"]["links"][0])
                                guildName = self.client.get_guild(link)

                                if guildName is not None:
                                    guildPath = f"{user_location}\\{link}\\{userID}\\{userID}-exp.json"

                                    make_asset(guildPath, "w", data, 4)
                                    make_asset(f"{user_location}\\{message.guild.id}\\{message.author.id}\\{message.author.id}.json", "w", main_usr_data, 4)
                                    make_asset(metadata_location+f"\\{message.guild.id}\\payload-data.json", "w", userMetadata, 4)

                                else:
                                    print(f"{globalData['global']['has-link']} >>>> {self.client.get_guild(globalData['global']['link-id'])}")
                                    if globalData["global"]["has-link"] is True and self.client.get_guild(globalData["global"]["link-id"]) is None:

                                        userLinks["member-link"]["links"].clear()
                                        globalData["global"]["has-link"] = False

                                        linkUser = self.client.get_user(member_id)
                                        await linkUser.send("The server you made a link on has since been deleted or I was kicked, I have severed your link.\nAnd you have kept all Experience data you gathered from both servers, sorry for the inconvinience. (Note: Of course, I can only make a link to a server if I'm in it)")

                                        make_asset(f"{full_user_path}\\{userID}\\{userID}-links.json", "w", userLinks, 4)
                                        make_asset(global_profile+f"\\{member_id}\\{member_id}.json", "w", globalData, 4)

                                    else:
                                        pass


                            except IndexError:
                                pass

                        make_asset(f"{user_location}\\{message.guild.id}\\{message.author.id}\\{message.author.id}.json", "w", main_usr_data, 4)
                        make_asset(metadata_location+f"\\{message.guild.id}\\payload-data.json", "w", userMetadata, 4)
                        json.dump(data, write_data, indent=4)

            except FileNotFoundError:
                if os.path.isdir(f"{user_location}\\{message.guild.id}\\{message.author.id}"):
                    pass
                else:
                    os.mkdir(f"{user_location}\\{message.guild.id}\\{message.author.id}")

                make_plr()

                data = {}
                member_links = {}
                bank = {}

                data[member_id] = ({
                    "member-exp": 0,
                    "member-level": 0,
                    "member-until-next-lvl": 5
                })
                member_links[f"member-link"] = ({
                    "link-enabled": False,
                    "links": []
                })

                bank[f"{member_id}"] = ({
                    "balance": 50,
                    "inventory": {}
                })


                make_asset(file=f"{full_user_path}\\{member_id}\\{member_id}-exp.json", mode="w+", data=data, indent=4)
                make_asset(file=f"{full_user_path}\\{member_id}\\{member_id}-links.json", mode="w+", data=member_links, indent=4)
                make_asset(file=f"{full_user_path}\\{member_id}\\{member_id}-bank.json", mode="w+", data=bank, indent=4)


        except AttributeError:
            pass



    @commands.Cog.listener()
    async def on_member_join(self, member):

        embed = discord.Embed(color=TERQ)
        c_path = f"{config_location}\\{member.guild.id}"
        guild = member.guild.id
        full_user_path = user_location+f"\\{guild}"
        user_path = f"{full_user_path}\\{member.id}"

        g_img = None
        g_txt = None
        g_chl = None

        try:
            if return_data(file=f"{c_path}\\whitelist.json", tabel="setting1", sub_tabel="whitelist") == bool(True):

                embed.set_author(name="Whitelist is enabled on this server, you cannot join.")
                print("Player got kicked becuase of whitelist")

                await member.send(embed=embed)
                return await member.kick(reason="Whitelist is enabled")


        except FileNotFoundError:
            pass

        os.chdir(full_user_path)

        if os.path.isdir(full_user_path+f"\\{member.id}") != True:
            os.mkdir(f"{member.id}")

        name = member.name
        avatar = member.avatar_url

        data = {}
        member_level = {}
        member_metadata = {}
        member_links = {}
        member_bank = {}

        data['setting1'] = ({
            "warnings": 0
        })

        member_metadata[f'{member.id}'] = ({
            "member-id": str(member.id),
            "member-name": str(name),
            "member-avatar": str(avatar),
            "member-joindate": str(member.joined_at),
            "member-exp": 0,
            "member-link": {
                "link-enabled": False,
                "links": []
            }
        })

        member_metadata['progress-bar'] = ({
            "progress-bar-count": 0
        })
        member_links[f"member-link"] = ({
            "link-enabled": False,
            "links": []
        })

        member_level[member.id] = ({
            "member-exp": 0,
            "member-level": 0,
            "member-until-next-lvl": 50
        })

        member_bank[f"{member.id}"] = ({
            "balance": 50,
            "inventory": {}
        })

        make_asset(file=f"{user_path}\\{member.id}.json", mode="w+", data=member_metadata, indent=4)
        make_asset(file=f"{user_path}\\{member.id}-warnings.json", mode="w+", data=data, indent=4)
        make_asset(file=f"{user_path}\\{member.id}-exp.json", mode="w+", data=member_level, indent=4)
        make_asset(file=f"{user_path}\\{member.id}-links.json", mode="w+", data=member_links, indent=4)
        make_asset(file=f"{user_path}\\{member.id}-bank.json", mode="w+", data=member_bank, indent=4)

        cfg_g = f"{config_location}\\{member.guild.id}"

        if check_dirfile(path=f"{cfg_g}\\join_channel.json", Type="file") and check_dirfile(path=f"{cfg_g}\\join_image.json", Type="file") and check_dirfile(path=f"{cfg_g}\\join_message.json", Type="file"):
            pass
        else:
            return False

        try:
            g_chl = return_data(file=f"{cfg_g}\\config.json", tabel="config", sub_tabel="join_channel")
        except KeyError:
            return
        try:
            g_img = return_data(file=f"{cfg_g}\\config.json", tabel="config", sub_tabel="join_image")

            if g_img is None:
                g_img = vorbis_img
        except KeyError:
            g_img = vorbis_img
        try:
            g_txt = return_data(file=f"{cfg_g}\\config.json", tabel="config", sub_tabel="join_message")

            if g_txt is None:
                g_txt = f"{member} has joined the guild, Please give them a warm welcome."
        except KeyError:
            g_txt = f"{member} has joined the guild, Please give them a warm welcome."

        embed.set_author(name="Notification")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=f"{member} has joined {member.guild}", value=g_txt)
        embed.set_image(url=g_img)

        try:
            await self.client.get_channel(int(g_chl)).send(embed=embed)
        except discord.errors.Forbidden:
            pass

        image = str(member.avatar_url)


        if os.path.isfile(f"{c_path}\\join_role.json"):
            try:
                role = return_data(file=f"{c_path}\\join_role.json", tabel="join_role", sub_tabel="role")
                role_to_give = discord.utils.get(self.client.get_guild(member.guild.id).roles, name=role)

                await member.add_roles(role_to_give)
            except AttributeError:
                pass
    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        async def make_role(role_name : str, color):
            await guild.create_role(name=f"{role_name}", colour=color)

        channel = None

        try:
            channel = await self.client.get_channel(guild.system_channel.id).create_invite(reason="For security purposes.")
        except AttributeError:
            pass

        directories = ['Music', 'Queue', 'Temp', 'Members', 'Metadata', 'Resources', 'Config']

        colors = {}

        colors = ({
            "COLOR": {
                "GREEN": {
                    "COLOR": GREEN,
                    "ID": 0
                },
                "LIGHT_BLUE": {
                    "COLOR": LIGHT_BLUE,
                    "ID": 1
                },
                "TERQ": {
                    "COLOR": TERQ,
                    "ID": 2
                },
                "YELLOW": {
                    "COLOR": YELLOW,
                    "ID": 3
                },
                "RED": {
                    "COLOR": RED,
                    "ID": 4
                },
                "DARK_RED": {
                    "COLOR": DARK_RED,
                    "ID": 5
                },
                "DARK_BLUE": {
                    "COLOR": DARK_BLUE,
                    "ID": 6
                },
                "DARK_ORANGE": {
                    "COLOR": DARK_ORANGE,
                    "ID": 7
                },
                "ORANGE": {
                    "COLOR": ORANGE,
                    "ID": 8
                },
                "PURPLE": {
                    "COLOR": PURPLE,
                    "ID": 9
                }
            }
        })

        if str(guild) != "tt":
            try:
                for x in range(len(directories)):
                    if os.path.isdir(f"{file_path}\\{directories[x]}\\{guild.id}") != True:
                        os.mkdir(f"{file_path}\\{directories[x]}\\{guild.id}")

            except FileExistsError:
                pass

        make_roles = True

        num = []
        color = []


        while make_roles is True:

            role_id = None
            role_colour = None
            roles = colors["COLOR"]
            role_l = list(colors["COLOR"])
            role_color = random.choice(role_l)
            role_full = roles[f"{role_color}"]
            role_id = role_full["ID"]
            role_colour = role_full["COLOR"]

            if role_id is not None:

                colors["COLOR"][f"{role_color}"]["ID"] = None

                num.append(".")
                color.append(role_colour)

            else:
                if len(num) > 9:
                    for y in range(0, 10):

                        await make_role(role_name=f"Level {y+1}0", color=color[y])

                    break
                else:
                    pass



        if str(guild) == "tt":
            return False

        config = {}
        links = {}
        bank = {}
        payload = {}
        metadata = {}

        config['config'] = ({
            "vol": 0.3,
            "loop": False
        })

        links["guild-links"] = ({
            "links-enabled": True
        })

        bank[f"{guild.id}"] = ({
            "guild-balance": 0,
            "items": [],
            "guild-items": {}
        })

        metadata['metadata'] = ({
            "name": None,
            "views": None,
            "author": None,
            "queued-playlist": None
        })
        payload["data"] = ({
            "author-id": None,
            "message-id": None,
            "og-message-id": None
        })


        make_asset(file=f"{config_location}\\{guild.id}\\config.json", mode="w+", data=config, indent=4)
        make_asset(file=f"{metadata_location}\\{guild.id}\\metadata.json", mode="w+", data=metadata, indent=4)
        make_asset(file=f"{metadata_location}\\{guild.id}\\payload-data.json", mode="w+", data=payload, indent=4)


        os.chdir(guild_location)

        def mk_metadata():
            if os.path.isdir(guild_location+f"\\{guild.id}") == False:
                os.mkdir(guild_location+f"\\{guild.id}")


            with open(guild_location+f"\\{guild.id}\\{guild.id}.json", "w+") as edit_svr_metadata:

                server_matadata = {}
                server_matadata[guild.id] = ({
                    f"{guild.id}-id": str(guild.id),
                    f"{guild.id}-ico": str(guild.icon),
                    f"{guild.id}-nm": str(guild.name),
                    f"{guild.id}-bnr": str(guild.banner),
                    f"{guild.id}-desc": str(guild.description),
                    f"{guild.id}-cunrt-boosts": str(guild.premium_subscription_count),
                    f"{guild.id}-roles": str(guild.roles),
                    f"{guild.id}-member-count": str(guild.member_count),
                    f"{guild.id}-invite": str(channel)

                })

                json.dump(server_matadata, edit_svr_metadata, indent=4)
                make_asset(file=f"{guild_location}\\{guild.id}\\{guild.id}-LINKS.json", mode="w+", data=links, indent=4)
                make_asset(file=f"{guild_location}\\{guild.id}\\{guild.id}-INVENTORY.json", mode="w+", data=bank, indent=4)

                print("Made Assets")

        embed = discord.Embed(color=self.client.get_user(guild.owner_id).color)
        fabian, austin = self.client.get_user(533285613021954049), self.client.get_user(400089431933059072)

        embed.set_author(name=f"I have joined {guild}!")
        embed.add_field(name="I am Vorbis!", value="I can play songs, make playlists, queue songs, and I have a level system! do /help for help, and /usage for command usage!\n(This is Austin Talking) And here is Vorbis' YouTube Channel, I will upload tutorials on how to operate Vorbis. As I understand it is difficult to use, I apologise.")
        embed.set_footer(text=f"Programmed by {fabian} and {austin} (On discord) 👩‍💻")
        embed.set_thumbnail(url=vorbis_img)

        mk_metadata()

        try:
            await self.client.get_guild(guild.id).get_channel(guild.system_channel.id).send(embed=embed)
            await self.client.get_user(guild.owner_id).send('Note for Owner / Administrators : Do "/server help" in server\nAnd if/when you want the bot to leave the server\nDo /leave')

        except AttributeError:
            print("Server has no system channel, not sending welcome message..")
            mk_metadata()

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):

        guild = after
        guild_data = {}

        guild_data[guild.id] = ({
                    f"{guild.id}-id": str(guild.id),
                    f"{guild.id}-ico": str(guild.icon),
                    f"{guild.id}-nm": str(guild.name),
                    f"{guild.id}-bnr": str(guild.banner),
                    f"{guild.id}-desc": str(guild.description),
                    f"{guild.id}-cunrt-boosts": str(guild.premium_subscription_count),
                    f"{guild.id}-roles": str(guild.roles)
        })

        make_asset(file=guild_location+f"\\{guild.id}\\{guild.id}.json", mode="w+", data=guild_data, indent=4)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        embed = discord.Embed(color=DARK_BLUE)
        g_id = member.guild.id

        if member.id == 798867893910765579:
            return

        location_msg = f"{config_location}\\{g_id}\\config.json"
        location_img = f"{config_location}\\{g_id}\\config.json"
        location_chnl = f"{config_location}\\{g_id}\\config.json"

        l_value = None
        l_img = None
        chnl_id = None
        if check_dirfile(path=location_msg, Type="file") and check_dirfile(path=location_img, Type="file") and check_dirfile(path=location_chnl, Type="file"):
            pass
        else:
            return False

        l_name = f"{member} left {member.guild}!"
        try:
            l_value = return_data(file=location_msg, tabel="config", sub_tabel="leave_message")

            if l_value is None:
                l_value = f"{member} has left the guild."

        except KeyError:
            l_value = f"{member} has left the guild."
        try:
            l_img = return_data(file=location_img, tabel="config", sub_tabel="leave_image")

            if l_img is None:
                l_img = vorbis_img
        except KeyError:
            l_img = vorbis_img
        try:
            chnl_id = return_data(file=location_chnl, tabel="config", sub_tabel="leave_channel")
        except KeyError:
            return

        embed.set_author(name="Notification")
        embed.add_field(name=l_name, value=l_value)
        embed.set_image(url=l_img)

        await self.client.get_guild(g_id).get_channel(chnl_id).send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        ctx, member = self.client.get_channel(payload.channel_id), payload.member
        messageChannel = self.client.get_channel(payload.channel_id)
        message = await messageChannel.fetch_message(payload.message_id)
        embed = discord.Embed(color=LIGHT_BLUE)

        try:
            channel, vorbis = member.voice.channel, self.client.get_user(self.client.user.id)
            guild = self.client.get_guild(payload.guild_id)
            voice = get(self.client.voice_clients, guild=guild)

            metadata = return_data(metadata_location+f"\\{payload.guild_id}\\payload-data.json")
            config = return_data(f"{config_location}\\{payload.guild_id}\\config.json")

            if member.id != 798867893910765579:
                if member in channel.members and vorbis in channel.members:
                    if payload.message_id == metadata["data"]["message-id"] or payload.message_id == metadata["data"]["og-message-id"] and member.id == metadata["data"]["author-id"]:

                        if payload.emoji.name == "\U0001f3b5":
                            voice.pause()

                        elif payload.emoji.name == "\U0001f3b6":
                            voice.pause()
                            voice.stop()

                            config["config"]["loop"] = False
                            make_asset(f"{config_location}\\{payload.guild_id}\\config.json", "w", config, 4)

                            await message.remove_reaction("\U0001f3b6", member)
                        elif payload.emoji.name == "\U0001f4fc":
                            song_list = []
                            songsList = os.listdir(queue_location+f"\\{payload.guild_id}")

                            embed.set_author(name="Queued Songs")



                            for x in range(len(songsList)):
                                song = songsList[x].split(".wav")[0]

                                embed.add_field(name=f"Song {x+1}  Ø ", value=song, inline=False)

                            embed.set_footer(text=f"Amount of songs left: {len(songsList)}")
                            await ctx.send(embed=embed, delete_after=10)
                            await message.remove_reaction("\U0001f4fc", member)
                        elif payload.emoji.name == "\U0001f502":
                            config["config"]["loop"] = True
                            make_asset(f"{config_location}\\{payload.guild_id}\\config.json", "w", config, 4)


                    else:
                        return
                else:
                    return
            else:
                return
        except AttributeError:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        emoji, guildID = payload.emoji.name, payload.guild_id
        metadata = return_data(f"{metadata_location}\\{guildID}\\payload-data.json")
        messageChannel = self.client.get_channel(payload.channel_id)
        message = await messageChannel.fetch_message(payload.message_id)
        config = return_data(f"{config_location}\\{guildID}\\config.json")

        try:
            guild = self.client.get_guild(payload.guild_id)
            voice = get(self.client.voice_clients, guild=guild)

            if message.author.id == metadata["data"]["author-id"] and message.id == metadata["data"]["message-id"] or message.id == metadata["data"]["og-message-id"]:
                if emoji == "\U0001f502":
                    config["config"]["loop"] = False
                    make_asset(f"{config_location}\\{guildID}\\config.json", "w", config, 4)
                elif emoji == "\U0001f3b5":
                    voice.resume()
                else:
                    return
            else:
                return
        except AttributeError:
            pass

def setup(client):
    client.add_cog(listeners(client))
