import discord, json, os, datetime, random

from discord.ext import tasks, commands

file_path = "C:\\Users\\Default\\Documents\\Python\\Scripts\\Vorbis"
user_location = file_path+"\\Members"
guild_location = file_path+"\\Guilds"
config_location = file_path+"\\Config"
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

def make_asset(file : os.PathLike, mode : str, data : dict, indent : int=4):

    with open(file, mode) as make_json:
        json.dump(obj=data, fp=make_json, indent=indent)
        make_json.close()
        
def return_data(file : str, tabel : str, sub_tabel : str):

    if check_dirfile(path=file, Type="file"):
        with open(f"{file}") as data:

            RwText_Data = data.read()
            RwJSON_Data = json.loads(RwText_Data)

            return RwJSON_Data[tabel][sub_tabel]

    else:
        raise FileNotFoundError(f"{file} Path Not Found")     
        
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
        self.client = client

    

        
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if check_dirfile(path=f"{config_location}\\{message.guild.id}\\log_channel.json", Type="file") is True:
            pass
        else:
            print("Server has no log_channel")
            return False

        print(f"{message.author}: "+message.content)
        try:
            guild = f"\\{message.guild.id}"
            full_user_path = user_location+guild
            channel_path = f"{config_location}\\{message.guild.id}\\log_channel.json"
        except AttributeError:
            pass
        if message.author.id == 798867893910765579:
            return

        if check_dirfile(path=channel_path, Type="file"):
            channel_id = return_data(file=channel_path, tabel="setting1", sub_tabel="channel")

            channel = self.client.get_channel(int(channel_id))
        global usr_exp, until_nxt_lvl, usr_lvl

        usr_exp = 0
        until_nxt_lvl = None
        usr_lvl = 0

        embed = discord.Embed(color=message.author.colour)
        member_id = message.author.id
        
        def make_plr():

            name = message.author.name
            avatar = message.author.avatar_url

            with open(f"{full_user_path}\\{member_id}\\{member_id}.json", "w+") as write_member:

                member_metadata = {}
                member_metadata[f'{member_id}'] = ({
                    "member-id": str(member_id),
                    "member-name": str(name),
                    "member-avatar": str(avatar),
                    "member-joindate": str(message.author.joined_at),
                    "member-exp": 0
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

                    data = {}
                    numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                    level_numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

                    if message.guild.premium_tier == 0:
                        new_exp = usr_exp+1
                    elif message.guild.premium_tier == 1:
                        new_exp = usr_exp+2
                    elif message.guild.premium_tier == 2:
                        new_exp = usr_exp+3


                    if new_exp >= until_nxt_lvl:
                        

                        until_nxt_lvl = int(random.choice(level_numbers))
                        curnt_time = str(datetime.datetime.now())

                        new_exp = 0
                        usr_lvl = usr_lvl+1
                        role = None
                        next_milestone = None

                        if usr_lvl in numbers:
                            print(self.client.get_guild(message.guild.id).roles)
                            role = discord.utils.get(self.client.get_guild(message.guild.id).roles, name=f"Level {usr_lvl}")
                        else:
                            for x in range(len(numbers)):
                                if usr_lvl < numbers[x] and usr_lvl > numbers[x-1]:
                                    next_milestone = numbers[x]
                            
                        if next_milestone is None:
                            next_milestone = usr_lvl+10
                        if usr_lvl >= 100:
                            next_milestone = "No more milestones"
                        

                        embed.set_author(name="Level Up \u200b")
                        embed.set_image(url=message.author.avatar_url)

                        embed.add_field(name=f"Ø   {message.author} levelled up to level {usr_lvl}!", value="\u200b")
                        embed.add_field(name=f"Ø   Eperience Needed to level up   Ø   {until_nxt_lvl}", value="\u200b", inline=False)
                        embed.add_field(name=f"Ø   Next milestone   Ø   {next_milestone}", value="\u200b", inline=False)

                        embed.set_footer(text="Time of Level Up Ø {}  UTC".format(curnt_time.split(".")[0]))



                        if channel is not None:
                            await channel.send(embed=embed)
                        else:
                            await self.client.get_guild(message.guild.id).get_channel(message.channel.id).send(embed=embed)

                        
                        

                            print("User did not hit a milestone")
                        if role is not None:
                            await message.author.add_roles(role)
                        else:
                            pass

                    data[member_id] = ({
                        "member-exp": new_exp,
                        "member-level": usr_lvl,
                        "member-until-next-lvl": until_nxt_lvl

                    })

                    json.dump(data, write_data, indent=4)
            
                make_plr()
                
        except FileNotFoundError:
            if os.path.isdir(f"{user_location}\\{message.guild.id}\\{message.author.id}"):
                pass
            else:
                os.mkdir(f"{user_location}\\{message.guild.id}\\{message.author.id}")

            make_plr()
                
            data = {}

            data[member_id] = ({
                "member-exp": 0,
                "member-level": 0,
                "member-until-next-lvl": 5
            })

            make_asset(file=f"{full_user_path}\\{member_id}\\{member_id}-exp.json", mode="w+", data=data, indent=4)
        
        
            
    
    @commands.Cog.listener()
    async def on_member_join(self, member):

        embed = discord.Embed(color=TERQ)
        c_path = f"{config_location}\\{member.guild.id}"
        guild = member.guild.id
        full_user_path = user_location+f"\\{guild}"
        user_path = f"{full_user_path}\\{member.id}"

        try:
            if return_data(file=f"{c_path}\\whitelist.json", tabel="setting1", sub_tabel="whitelist") == bool(True):

                embed.set_author(name="Whitelist is enabled on this server, you cannot join.")
                print("Player got kicked becuase of whitelist")
                
                await member.send(embed=embed)
                return await member.kick(reason="Whitelist is enabled")

      
        except FileNotFoundError:
            pass
        
        try:
            blacklist = list(return_data(file=f"{c_path}\\blacklist.json", tabel="setting1", sub_tabel="blacklist"))

        
            if str(member.id) in blacklist:
            
                await member.send("You're blacklisted from this server.")
                await member.kick(reason="Player was blacklisted from server")

                if check_dirfile(path=f"{c_path}\\log_channel.json", Type="file") is True:
                    channel_id = int(return_data(file=f"{c_path}\\log_channel.json", tabel="setting1", sub_tabel="channel")) 
                    channel = self.client.get_channel(channel_id)

                    if channel is None:
                        return
                    else:
                        embed.set_author(name=f"Kicked {member.name}, Reason: Player was blacklisted")
                        return await channel.send(embed=embed)
                else:
                    return

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

        data['setting1'] = ({
            "warnings": 0
        })

        member_metadata[f'{member.id}'] = ({
            "member-id": str(member.id),
            "member-name": str(name),
            "member-avatar": str(avatar),
            "member-joindate": str(member.joined_at),
            "member-exp": 0
        })

        member_level[member.id] = ({
            "member-exp": 0,
            "member-level": 0,
            "member-until-next-lvl": 5
        })

        make_asset(file=f"{user_path}\\{member.id}.json", mode="w+", data=member_metadata, indent=4)
        make_asset(file=f"{user_path}\\{member.id}-warnings.json", mode="w+", data=data, indent=4)
        make_asset(file=f"{user_path}\\{member.id}-exp.json", mode="w+", data=member_level, indent=4)

        cfg_g = f"{config_location}\\{member.guild.id}"

        if check_dirfile(path=f"{cfg_g}\\join_channel.json", Type="file") and check_dirfile(path=f"{cfg_g}\\join_image.json", Type="file") and check_dirfile(path=f"{cfg_g}\\join_message.json", Type="file"):
            pass
        else:
            return False

        g_chl = return_data(file=f"{cfg_g}\\join_channel.json", tabel="setting1", sub_tabel="channel")
        g_img = return_data(file=f"{cfg_g}\\join_image.json", tabel="setting1", sub_tabel="url")
        g_txt = return_data(file=f"{cfg_g}\\join_message.json", tabel="setting1", sub_tabel="text")
        
        
        embed.set_author(name="Notification")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=f"{member} has joined {member.guild}", value=g_txt)
        embed.set_image(url=g_img)
        
        await self.client.get_channel(int(g_chl)).send(embed=embed)
        
        if os.path.isfile(f"{c_path}\\join_role.json"):

            role = return_data(file=f"{c_path}\\join_role.json", tabel="join_role", sub_tabel="role")  
            role_to_give = discord.utils.get(self.client.get_guild(member.guild.id).roles, name=role)

            await member.add_roles(role_to_give)
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        async def make_role(role_name : str, color):
            await guild.create_role(name=f"{role_name}", colour=color)

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

                #print(f"\n\nMade Role>\nNAME>{name_final}\nCOLOR>{role_colour}\nNAME_L>{name_l}\nNAME_NUMBER>{name_number}\nNAME_ID>{name_id}\nNUM>{num}")
                
            else:
                if len(num) > 9:
                    for y in range(0, 10):

                        await make_role(role_name=f"Level {y+1}0", color=color[y])
                    
                    break
                else:
                    pass
                    #print(f"\n\nMade Role>\nNAME>{name_final}\nCOLOR>{role_colour}\nNAME_L>{name_l}\nNAME_NUMBER>{name_number}\nNAME_ID>{name_id}\nNUM>{num}")
                    
                
        if str(guild) == "tt":
            print(guild)
            return False
        else:
            print(f"Not Debug Server>{guild}")
        New_vol = {}
        New_vol['volume'] = ({
            "vol": 1.0
        })
        max_warnings = {}
        max_warnings["setting1"] = {
            "warnings": 3
        }

        make_asset(file=file_path+f"\\Config\\{guild.id}\\volume.json", mode="w+", data=New_vol, indent=4)
        make_asset(file=file_path+f"\\Config\\{guild.id}\\max_warnings.json", mode="w+", data=max_warnings, indent=4)

        os.chdir(guild_location)

        def mk_metadata():
            if os.path.isdir(guild_location+f"\\{guild.id}") == False:
                print("Bot has not been in this server before, making assets...")
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
                    f"{guild.id}-member-count": str(guild.member_count)

                })

                json.dump(server_matadata, edit_svr_metadata, indent=4)

        embed = discord.Embed(color=self.client.get_user(guild.owner_id).color)

        embed.set_author(name=f"I have joined {guild}!")
        embed.add_field(name="I am Vorbis!", value="I can play songs, make playlists, queue songs, and I have a level system! do /help for help, and /usage for command usage!")
        embed.set_footer(text="Programmed by Austin Ares#0001")
        embed.set_thumbnail(url=vorbis_img)

        try:
            await self.client.get_guild(guild.id).get_channel(guild.system_channel.id).send(embed=embed)
            await self.client.get_user(guild.owner_id).send('Note for Owner / Administrators : Do "/server help" in server\nAnd if/when you want the bot to leave the server\nDo /leave')
            mk_metadata()
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

        location_msg = f"{config_location}\\{g_id}\\leave_message.json"
        location_img = f"{config_location}\\{g_id}\\leave_image.json"
        location_chnl = f"{config_location}\\{g_id}\\leave_channel.json"
        
        if check_dirfile(path=location_msg, Type="file") and check_dirfile(path=location_img, Type="file") and check_dirfile(path=location_chnl, Type="file"):
            pass
        else:
            return False
    
        l_name = f"{member} left {member.guild}!"
        l_value = return_data(file=location_msg, tabel="setting1", sub_tabel="text")
        l_img = return_data(file=location_img, tabel="setting1", sub_tabel="url")
        chnl_id = return_data(file=location_chnl, tabel="setting1", sub_tabel="channel")
        
        embed.set_author(name="Notification")
        embed.add_field(name=l_name, value=l_value)
        embed.set_image(url=l_img)
        
        await self.client.get_guild(g_id).get_channel(chnl_id).send(embed=embed)
        
def setup(client):
    client.add_cog(listeners(client))