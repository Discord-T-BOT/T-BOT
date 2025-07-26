import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
from func.data import kusa
from random import sample

class FunCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("FunCog")

    class fun (app_commands.Group):
        pass
    fun1 = fun(name="fun",description="おもしろコマンド")

    @fun1.command(name="kaso_gif",description="tenorの過疎gifを送りつけます")
    async def kaso_gif(self, interaction:discord.Interaction):
        await interaction.response.send_message("https://tenor.com/view/%E9%81%8E%E7%96%8E-%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC-server-gif-24904455")

    @fun1.command(name="kick_vc",description="退出させます")
    async def kick_fake(self, interaction:discord.Interaction):
        if interaction.user.voice:
            await interaction.user.move_to(None)
            await interaction.user.send("正常にKickしました。")
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="自爆しました。",
                    description=f"{interaction.user.mention}は、偽KickをしたことによりVCから退出しました。",
                    color=0xff0000
                )
            )
        else:
            await interaction.response.send_message("エラーが発生しました。")
    @fun1.command(name="kusa",description="草をランダムで生やします🌱")
    async def kusa_nyoki(self, interaction:discord.Interaction, count:int = 1):
        if count > len(kusa):
            a = len(kusa)
        else:
            a = count
        await interaction.response.send_message(content=" ".join(sample(kusa,k=a)))


async def setup(bot):
    await bot.add_cog(FunCog(bot))