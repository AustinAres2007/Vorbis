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

    with open(f"{file}") as data:

        RwText_Data = data.read()
        RwJSON_Data = json.loads(RwText_Data)

        return RwJSON_Data[tabel][sub_tabel]

class listeners(commands.Cog):

    def __init__(self, client):
        self.client = client

    

        
    
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            guild = f"\\{message.guild.id}"
            full_user_path = user_location+guild
        except AttributeError:
            pass
        if message.author.id == 798867893910765579:
            return

        global usr_exp, until_nxt_lvl, usr_lvl

        usr_exp = 0
        until_nxt_lvl = None
        usr_lvl = 0

        embed = discord.Embed(color=message.author.colour)
        member_id = message.author.id
        guild_id = message.guild.id
        
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
            print("Reading Users Current Level Data..")
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
                    level_numbers = [10, 20, 30, 40, 50]
                    boosts = int(return_data(file=f"{guild_location}\\{guild_id}\\{guild_id}.json", tabel=f"{guild_id}", sub_tabel=f"{guild_id}-cunrt-boosts"))

                    if boosts == 0:
                        new_exp = usr_exp+1
                    elif boosts == 2:
                        new_exp = usr_exp+2
                    elif boosts == 4:
                        new_exp = usr_exp+3


                    if new_exp > until_nxt_lvl:
                
                        embed.set_author(name="Level Up")
                        embed.add_field(name=f"You leveled up to level {usr_lvl+1}!", value="|")
                        embed.set_image(url=message.author.avatar_url)

                        await self.client.get_guild(message.guild.id).get_channel(message.channel.id).send(embed=embed)

                        until_nxt_lvl = int(random.choice(level_numbers))
                        new_exp = 0
                        usr_lvl = usr_lvl+1
                        role = None

                        if usr_lvl in numbers:
                            print(self.client.get_guild(message.guild.id).roles)
                            role = discord.utils.get(self.client.get_guild(message.guild.id).roles, name=f"Level {usr_lvl}")
                        else:
                            print("User did not hit a milestone")
                        if role is not None:
                            await message.author.add_roles(role)
                        else:
                            pass

                    print("Updated Member EXP")
                    data[member_id] = ({
                        "member-exp": new_exp,
                        "member-level": usr_lvl,
                        "member-until-next-lvl": until_nxt_lvl

                    })

                    json.dump(data, write_data, indent=4)
            
                make_plr()
                
        except FileNotFoundError:
            print("Making User")
            if os.path.isdir(f"{user_location}\\{message.guild.id}\\{message.author.id}"):
                pass
            else:
                os.mkdir(f"{user_location}\\{message.guild.id}\\{message.author.id}")

            make_plr()

            with open(f"{full_user_path}\\{member_id}\\{member_id}-exp.json", "w") as write_base_data:
                
                data = {}

                data[member_id] = ({
                    "member-exp": 0,
                    "member-level": 0,
                    "member-until-next-lvl": 5
                })

                json.dump(data, write_base_data, indent=4)
        
        
            
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild.id
        full_user_path = user_location+f"\\{guild}"

        os.chdir(full_user_path)

        if os.path.isdir(full_user_path+f"\\{member.id}"):
            pass
        else:
            os.mkdir(f"{member.id}")

        name = member.name
        avatar = member.avatar_url

        print(name)
        print(avatar)

        with open(f"{full_user_path}\\{member.id}\\{member.id}.json", "w+") as write_member:

            member_metadata = {}
            member_metadata[f'{member.id}'] = ({
                "member-id": str(member.id),
                "member-name": str(name),
                "member-avatar": str(avatar),
                "member-joindate": str(member.joined_at),
                "member-exp": 0
            })

            json.dump(member_metadata, write_member, indent=4)

            write_member.close()
        
        with open(f"{full_user_path}\\{member.id}\\{member.id}-exp.json", "w") as write_base_data:

            data = {}

            data[member.id] = ({
                "member-exp": 0,
                "member-level": 0,
                "member-until-next-lvl": 5
            })

            json.dump(data, write_base_data, indent=4)
        
        if os.path.isfile(f"{config_location}\\{member.guild.id}\\join_role.json"):
            with open(f"{config_location}\\{member.guild.id}\\join_role.json", "r") as read_join_role:

                text = read_join_role.read()
                json_readable = json.loads(text)
                
                role = json_readable['join_role']['role']
                
                role_to_give = discord.utils.get(self.client.get_guild(member.guild.id).roles, name=role)
                await member.add_roles(role_to_give)
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        print(file_path)
        directories = ['Music', 'Queue', 'Temp', 'Members', 'Metadata', 'Resources', 'Config']
        try:
            for x in range(len(directories)):
                print(directories[x])
                if os.path.isdir(f"{file_path}\\{directories[x]}\\{guild.id}"):
                    pass
                else:
                    os.mkdir(f"{file_path}\\{directories[x]}\\{guild.id}")


        except FileExistsError:
            pass

        try:
            await guild.create_role(name="Level 100", colour=PURPLE)
            await guild.create_role(name="Level 90", colour=ORANGE)
            await guild.create_role(name="Level 80", colour=DARK_ORANGE)
            await guild.create_role(name="Level 70", colour=DARK_BLUE)
            await guild.create_role(name="Level 60", colour=DARK_RED)
            await guild.create_role(name="Level 50", colour=RED)
            await guild.create_role(name="Level 40", colour=YELLOW)
            await guild.create_role(name="Level 30", colour=TERQ)
            await guild.create_role(name="Level 20", colour=LIGHT_BLUE)            
            await guild.create_role(name="Level 10", colour=GREEN)

            
        except Exception as e:
            print(e)

        
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
                    f"{guild.id}-roles": str(guild.roles)

                })

                json.dump(server_matadata, edit_svr_metadata, indent=4)

        embed = discord.Embed(color=self.client.get_user(guild.owner_id).color)

        embed.set_author(name=f"I have joined {guild}!")
        embed.add_field(name="I am Vorbis!", value="I can play songs, make playlists, queue songs, and I have a level system! do /help for help, and /usage for command usage!")
        embed.set_footer(text="Note for Owner / Administrators : Do /setup help")
        embed.set_thumbnail(url=vorbis_img)

        try:
            await self.client.get_guild(guild.id).get_channel(guild.system_channel.id).send(embed=embed)
            await self.client.get_user(guild.owner_id).send('Note for Owner / Administrators : Do "/setup help" in server')
            mk_metadata()
        except AttributeError:
            print("Server has no system channel, not sending welcome message..")
            mk_metadata()

def setup(client):
    client.add_cog(listeners(client))
    

