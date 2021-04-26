# _*_ coding:utf-8 _*_
import discord, asyncio, json, urllib.request, re
from discord.ext import commands
import os

app = commands.Bot(command_prefix="!")

# first loading cogs
for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        app.load_extension(f"Cogs.{filename[:-3]}")


@app.event
async def on_ready():
    print(app.user.name)
    print(app.user.id)
    game = discord.Game("Hmm...");
    await app.change_presence(status=discord.Status.online, activity=game)

# load cogs
@app.command()
async def load_cogs(ctx, extension):
    app.load_extension(f"Cogs.{extension}")
    await ctx.send(f"{extension} is loaded")

# unload cogs
@app.command()
async def unload_cogs(ctx, extension):
    app.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"{extension} is unloaded")

# reload cogs
@app.command()
async def reload_cogs(ctx, extension=None):
    if extension is None:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                app.unload_extension(f"Cogs.{filename[:-3]}")
                app.load_extension(f"Cogs.{filename[:-3]}")
                await ctx.send("all extension is reloaded")
    else:
        app.unload_extension(f"Cogs.{extension}")
        app.load_extension(f"Cogs.{extension}")
        await ctx.send(f"{extension} is reloaded")


#app.remove_command("help")
app.run(token)
#app.run(str(os.environ.get('token')))