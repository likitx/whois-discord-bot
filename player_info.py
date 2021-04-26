# _*_ coding:utf-8 _*_
import discord, asyncio, json, requests, re
from discord.ext import commands
import os

client = discord.Client()

bot = commands.Bot(command_prefix='!')

url_user_name = "https://gameinfo.albiononline.com/api/gameinfo/search?q="
url_user_id = "https://gameinfo.albiononline.com/api/gameinfo/players/"

async def temp(ctx=None):
    embed = discord.Embed(title="Char's info", description="", color=0xc16666)
    embed.add_field(name="!who <char>", value="char's basic info", inline=True)
    embed.add_field(name="!gi <char>", value="char's gathering info", inline=False)
    embed.add_field(name="Important !", value="<char> is case sensitive.",inline=False)

    #embed.set_footer(text="<char> is case sensitive.")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Hmm..."))
    print("ready")
       
@bot.command()
async def gi(ctx, arg = None):
    if(arg == None):
        #embed = discord.Embed(title="char's guild, alliance, etc.", description="usage : !gi [char name]\n[char name] is case sensitive.", color=0xc16666)
        #await ctx.send(embed=embed)
        await temp(ctx)

    if(arg != None):
        arg = re.sub('[^A-Za-z0-9]','',arg)
        
        await ctx.send(f'{arg}? Hmm...')

        r = requests.get(url_user_name+arg)
        data = r.text
        data_load = json.loads(data)

        pName = data_load["players"][0]["Name"]
        pId = data_load["players"][0]["Id"]

        if(pName == "" or pName != arg):
            await ctx.send(f"\"{arg}\" is not found. <char> is case sensitive.")
            
        if(pName == arg):
            embed = discord.Embed(title=arg, description="", color=0xc16666)
            s = requests.get(url_user_id+pId)
            info = s.text
            info_load = json.loads(info)

            pGTotal = info_load["LifetimeStatistics"]["Gathering"]["All"]["Total"]
            pFiber = info_load["LifetimeStatistics"]["Gathering"]["Fiber"]["Total"]
            pHide = info_load["LifetimeStatistics"]["Gathering"]["Hide"]["Total"]
            pOre = info_load["LifetimeStatistics"]["Gathering"]["Ore"]["Total"]
            pRock = info_load["LifetimeStatistics"]["Gathering"]["Rock"]["Total"]
            pWood = info_load["LifetimeStatistics"]["Gathering"]["Wood"]["Total"]
            pFishing = info_load["LifetimeStatistics"]["FishingFame"]
            
            gTotal = pGTotal + pFishing
            embed.add_field(name="Total(resources+fishing) : ", value="{0:,}".format(gTotal), inline=False)
            embed.add_field(name="Fiber:", value="{0:,}".format(pFiber), inline=True)
            embed.add_field(name="Hide:", value="{0:,}".format(pHide), inline=True)
            embed.add_field(name="Ore:", value="{0:,}".format(pOre), inline=True)
            embed.add_field(name="Rock:", value="{0:,}".format(pRock), inline=True)
            embed.add_field(name="Wood:", value="{0:,}".format(pWood), inline=True)
            embed.add_field(name="Fishing:", value="{0:,}".format(pFishing), inline=False)
            
            await ctx.send(embed=embed)
@bot.command()
async def who(ctx, arg = None):
    if(arg == None):
        await temp(ctx)
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
            await ctx.send(f'{arg} is not found. <char> is case sensitive.')
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

bot.run(str(os.environ.get('token')))
