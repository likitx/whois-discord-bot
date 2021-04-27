# _*_ coding:utf-8 _*_
import discord, asyncio, json, requests, re
from discord.ext import commands
import os


class UserInfo(commands.Cog):
    def __init__(self, app):
        self.app = app
        
        self.url_user_name = "https://gameinfo.albiononline.com/api/gameinfo/search?q="
        self.url_user_id = "https://gameinfo.albiononline.com/api/gameinfo/players/"
        
    async def temp(self, ctx):
        embed = discord.Embed(title="Char's info", description="", color=0xc16666)
        embed.add_field(name="!who <char>", value="char's basic info", inline=True)
        embed.add_field(name="!gi <char>", value="char's gathering info", inline=False)
        embed.add_field(name="Important !", value="<char> is case sensitive.",inline=False)

        #embed.set_footer(text="<char> is case sensitive.")
        await ctx.send(embed=embed)

    @commands.command()
    async def who(self, ctx, arg = None):
        if(arg == None):
            await self.temp(ctx)
            return None

        if(arg != None):
            arg = re.sub('[^A-Za-z0-9]','',arg)
            
            await ctx.send(f'{arg}? Hmm...')
            
            fullURL = self.url_user_name+arg
            r = requests.get(fullURL)
            data = r.text
            data_load = json.loads(data)
            
            if len(data_load["players"]) == 0:
                await ctx.send(f'\"{arg}\" is not found. <char> is case sensitive.')
                return None
            return

            pName = data_load["players"][0]["Name"]
            pGuild = data_load["players"][0]["GuildName"]
            if pGuild == "":
                pGuild = "<>"
            pAlliance = data_load["players"][0]["AllianceName"]
            if pAlliance == "":
                pAlliance = "<>"
            pKill = data_load["players"][0]["KillFame"]
            pDeath = data_load["players"][0]["DeathFame"]
            pRatio = data_load["players"][0]["FameRatio"]

            if(pName == "" or pName != arg):
                await ctx.send(f'\"{arg}\" is not found. <char> is case sensitive.')
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

    @commands.command()
    async def gi(self, ctx, arg = None):
        if(arg == None):
            await self.temp(ctx)
            return None

        if(arg != None):
            arg = re.sub('[^A-Za-z0-9]','',arg)
            
            await ctx.send(f'{arg}? Hmm...')

            fullURL = self.url_user_name+arg
            r = requests.get(fullURL)
            data = r.text
            data_load = json.loads(data)

            if len(data_load["players"]) == 0:
                await ctx.send(f'\"{arg}\" is not found. <char> is case sensitive.')
                return None
            return

            pName = data_load["players"][0]["Name"]
            pId = data_load["players"][0]["Id"]

            if(pName != arg):
                await ctx.send(f"\"{arg}\" is not found. <char> is case sensitive.")
                
            if(pName == arg):
                embed = discord.Embed(title=arg, description="", color=0xc16666)

                fullURL = self.url_user_id+pId
                with urllib.request.urlopen(fullURL) as url:
                    info_load = json.loads(url.read().decode())

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

def setup(app):
    app.add_cog(UserInfo(app))
    
