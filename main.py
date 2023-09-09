import asyncio
import nextcord
from nextcord.ext import commands
import os

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="--", intents=intents)

cogs = [

    "cogs.levels",
]

@bot.event
async def on_ready():

    print("Bot is ready")

if __name__ == "__main__":

    for cog in cogs:
        bot.load_extension(cog)

@bot.event
async def on_ready():
  guilds = len(bot.guilds)
  info = "/"
  print(f"{bot.user.name} запущен(а))".format(info)) #в командную строку идёт инфа о запуске
  while True:
    await bot.change_presence(status = nextcord.Status.dnd, activity = nextcord.Activity(name = f'/rank', type = nextcord.ActivityType.playing)) #Идёт инфа о команде помощи (префикс изменить)
    await asyncio.sleep(15)
    await bot.change_presence(status = nextcord.Status.dnd, activity = nextcord.Activity(name = f'behind {len(bot.guilds)} servers', type = nextcord.ActivityType.watching)) #Инфа о количестве серверов, на котором находится бот.
    await asyncio.sleep(15)
    members = 0
    for guild in bot.guilds:
      for member in guild.members:
        members += 1
    await bot.change_presence(status = nextcord.Status.idle, activity = nextcord.Activity(name = f'behind {members} members', type = nextcord.ActivityType.watching)) #Общее количество участников, за которыми следит бот (Находятся на серверах)
    await asyncio.sleep(15)

bot.run("token")