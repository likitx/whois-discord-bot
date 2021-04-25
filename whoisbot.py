# _*_ coding:utf-8 _*_
import discord, asyncio, json, requests, re
from discord.ext import commands

token = "ODM1NjgyMTI1Njg0MTQ2MjE4.YIS_oA.oTv9YAYne5pX4jcaErFFawXbsvs"
client = discord.Client()

bot = commands.Bot(command_prefix='!')

url_user_name = "https://gameinfo.albiononline.com/api/gameinfo/search?q="
url_user_id = "https://gameinfo.albiononline.com/api/gameinfo/players/"

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Hmm..."))
    print("ready")
       
@bot.command()
async def who(ctx, arg = None):
    if(arg == None):
        embed = discord.Embed(title="char's guild, alliance, etc.", description="usage : !who [char name]\n[char name] is case sensitive.", color=0xc16666)
        await ctx.send(embed=embed)
        return None

    if(arg != None):
        arg = re.sub('[^A-Za-z0-9]','',arg)
        
        await ctx.send(f'{arg}? Hmm...')

        r = requests.get(url_user_name+arg)
        data = r.text
        data_load = json.loads(data)

        pName = data_load["players"][0]["Name"]
        pGuild = data_load["players"][0]["GuildName"]
        pAlliance = data_load["players"][0]["AllianceName"]
        pTotal = data_load["players"][0]["KillFame"]
        pKill = data_load["players"][0]["KillFame"]
        pDeath = data_load["players"][0]["DeathFame"]
        pRatio = data_load["players"][0]["FameRatio"]

        if(pName == "" or pName != arg):
            await ctx.send(f'{arg} is not found')
            return None
            
        if(pName == arg):
            embed = discord.Embed(title=arg, description="", color=0xc16666)
            embed.add_field(name="Guild", value=pGuild, inline=True)
            embed.add_field(name="Alliance", value=pAlliance, inline=False)
            embed.add_field(name="K/F:", value="{0:,}".format(pKill), inline=True)
            embed.add_field(name="D/F:", value="{0:,}".format(pDeath), inline=True)
            embed.add_field(name="Ratio:", value=pRatio, inline=True)

            await ctx.send(embed=embed)
            return None
bot.run(token)