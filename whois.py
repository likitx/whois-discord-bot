# _*_ coding:utf-8 _*_
import discord, asyncio, json, requests


token = "ODM1NjgyMTI1Njg0MTQ2MjE4.YIS_oA.oTv9YAYne5pX4jcaErFFawXbsvs"
client = discord.Client()
url_user_name = "https://gameinfo.albiononline.com/api/gameinfo/search?q="
url_user_id = "https://gameinfo.albiononline.com/api/gameinfo/players/"

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Hmm..."))
       
@client.event
async def on_message(message):
    msg_arg = message.content
    list_arg = msg_arg.split()
    if message.author.bot:
        return None
    if len(list_arg) > 2 :
        return None
    if len(list_arg) ==  1 and list_arg[0] == "!who" :
        embed = discord.Embed(title="char's guild, alliance, etc.", description="usage : !who [char name]", color=0xc16666)
        embed.set_footer(text="usage : !who [char name]")
        await message.channel.send(embed=embed)
    if len(list_arg) ==  2 and list_arg[0] == "!who" :
        await message.channel.send("Hmm...")

        r = requests.get(url_user_name+list_arg[1])
        data = r.text
        data_load = json.loads(data)
        pName = data_load["players"][0]["Name"]
        pGuild = data_load["players"][0]["GuildName"]
        pAlliance = data_load["players"][0]["AllianceName"]
        pTotal = data_load["players"][0]["KillFame"]
        pKill = data_load["players"][0]["KillFame"]
        pDeath = data_load["players"][0]["DeathFame"]
        pRatio = data_load["players"][0]["FameRatio"]

        if pName == "" :
            await message.channel.send(list_arg[1]+" is not found")
            return None
        else :
            embed = discord.Embed(title=list_arg[1], description="", color=0xc16666)
            embed.add_field(name="Guild", value=pGuild, inline=True)
            embed.add_field(name="Alliance", value=pAlliance, inline=False)
            embed.add_field(name="K/F:", value="{0:,}".format(pKill), inline=True)
            embed.add_field(name="D/F:", value="{0:,}".format(pDeath), inline=True)
            embed.add_field(name="Ratio:", value=pRatio, inline=True)

            await message.channel.send(embed=embed)
        
client.run(token)