import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
from func.database import eco as eco1
from random import randint
import time


class EcoCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.eco = eco1()
        self.last_command_time = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("EcoCog")
    
    @app_commands.command(name="work",description="稼ぎます")
    async def work(self, interaction:discord.Interaction):
        current_time = time.time()
        last_time = self.last_command_time.get(interaction.user.id, 0)
        if current_time - last_time < 600:
            remaining_time = 600 - (current_time - last_time)
            await interaction.response.send_message(f"このコマンドは10分に1回しか使用できません。あと{int(remaining_time)}秒待ってください。", ephemeral=True) 
        else: 
            a = randint(150,900)
            b = self.eco.get_eco(interaction.user.id)
            self.eco.update_eco(interaction.user.id, a+b)
            amount = self.eco.get_eco(interaction.user.id)
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Work",
                    description=f"{a} TM 稼ぎました！\n現在の所持金: {amount} TM"
                )
            )
            self.last_command_time[interaction.user.id] = current_time
    @app_commands.command(name="bal",description="現在の残高を確認します")
    async def bal(self, interaction:discord.Interaction):
        amount = self.eco.get_eco(interaction.user.id)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Balance",
                description=f"現在の所持金: {amount} TM"
            )
        )

async def setup(bot):
    await bot.add_cog(EcoCog(bot))