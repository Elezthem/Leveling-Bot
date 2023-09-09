import nextcord
from nextcord.ext import commands
import vacefron
import math
import random
import sqlite3

database = sqlite3.connect("database.sqlite")
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS levels(user_id INTEGER, guild_id INTEGER, exp INTEGER, level INTEGER, last_lvl INTEGER)""")

class Leveling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        
        cursor.execute(f"SELECT user_id, guild_id, exp, level, last_lvl FROM levels WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}")
        result = cursor.fetchone()
        if result is None:

            cursor.execute(f"INSERT INTO levels(user_id, guild_id, exp, level, last_lvl) VALUES({message.author.id}, {message.guild.id}, 0, 0, 0)")
            database.commit()
        
        else:

            exp = result[2]
            lvl = result[3]
            last_lvl = result[4]
            
            exp_gained = random.randint(1, 20)
            exp += exp_gained
            lvl = 0.1*(math.sqrt(exp))
            
            cursor.execute(f"UPDATE levels SET exp = {exp}, level = {lvl} WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}")
            database.commit()

            if int(lvl) > last_lvl:

                await message.channel.send(f"{message.author.mention} has leveled up to level {int(lvl)}!")
                cursor.execute(f"UPDATE levels SET last_lvl = {int(lvl)} WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}")
                database.commit()
        
    @nextcord.slash_command()
    async def rank(self, interaction : nextcord.Interaction):
        
        rank = 1
        
        descending = "SELECT * FROM levels WHERE guild_id = ? ORDER BY exp DESC"
        cursor.execute(descending, (interaction.guild.id,))
        result = cursor.fetchall()

        for i in range(len(result)):

            if result[i][0] == interaction.user.id:
                break
            else:
                rank += 1
                
        cursor.execute(f"SELECT exp, level, last_lvl FROM levels WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}")
        result = cursor.fetchone()

        level = result[1]
        exp = result[0]
        last_lvl = result[2]

        next_lvl_xp = ((int(level) + 1) / 0.1) ** 2
        next_lvl_xp = int(next_lvl_xp)

        rank_card = vacefron.Rankcard(
            username = interaction.user.display_name,
                avatar_url = interaction.user.avatar.url,
                current_xp = exp,
                next_level_xp = next_lvl_xp,
                previous_level_xp = 0,
                level = int(level),
                rank = rank,
            )
        
        card = await vacefron.Client().rankcard(rank_card)
        await interaction.response.send_message(card.url)







    


def setup(bot):
    bot.add_cog(Leveling(bot))