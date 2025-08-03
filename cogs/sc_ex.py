import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
import aiohttp
import re
from func.database import set_sc_ex

class ScExCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("SCEXCog")
    
    async def scratch_expand(self, channel_id:int, id:int, message:discord.Message):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.scratch.mit.edu/projects/{id}/") as resp:
                data = await resp.json()
                print(data)
                if data["code"] == "NotFound":
                    await message.reply(embed=discord.Embed(
                        title="エラー",
                        description="無効なURLです",
                        color=0xff0000
                    ),allowed_mentions=discord.AllowedMentions(users=False, replied_user=False, roles=False,everyone=False))
                else:
                    embeds = []
                    embeds.append(discord.Embed(
                        title=data["title"],
                        url=f"https://scratch.mit.edu/projects/{id}/",
                        color=0xfda747,
                    ))
                    if data["instructions"] != None:
                        
                        embeds.append(discord.Embed(
                            title="使い方",
                            description=(len(data["instructions"]) if len(data["instructions"]) < 15 else "\n".join(re.split("\n",data["instructions"])[:5])),
                            color=0xfda747
                        ))
                    if data["description"] != None:
                        embeds.append(discord.Embed(
                            title="メモとクレジット",
                            description=(len(data["description"]) if len(data["description"]) < 15 else "\n".join(re.split("\n",data["description"])[:5])),
                            color=0xfda747
                        ))
                    embeds.append(discord.Embed(
                        title="ステータス",
                        description=f"<:love:1401290862956253324> : {data['stats']['loves']} | <:fav:1401290849857310800> : {data['stats']['favorites']} | <:remix:1401290874784190484> : {data['stats']['remixes']} | <:views:1401290886205411560> : {data['stats']['views']}",
                        color=0xfda747
                    ))
                    embeds[0].set_author(name=data["author"]["username"],icon_url=data["author"]["profile"]["images"]["90x90"])
                    embeds[0].set_thumbnail(url=data["image"])

                    await self.bot.get_channel(channel_id).send(embeds=embeds)

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        scex = set_sc_ex()
        res = scex.get_channel(message.channel.id)
        if res:
            channel_id = message.channel.id

            if "scratch.mit.edu/projects/" in message.content:
                one_re = re.findall('scratch.mit.edu/projects/.*', message.content)
                url_re_id = []
                for i in one_re:
                    url_re_id.append(re.findall('[0-9]+', i)[0])
                # print(url_re_id)
                
                for i in url_re_id:
                    await self.scratch_expand(channel_id=channel_id, id=i, message=message)
    
    class scex1(app_commands.Group):
        pass

    scex_c = scex1(name="scex",description="Scratchのリンク展開機能について")

    @scex_c.command(name="add",description="このチャンネルで有効化します。")
    async def scex_add(self, interaction:discord.Interaction):
        if interaction.user.guild_permissions.manage_channels | interaction.user.guild_permissions.administrator:
            scex = set_sc_ex()
            if scex.get_channel(interaction.channel.id):
                await interaction.response.send_message("すでに有効化されています。")
            else:
                scex.add_channel(interaction.channel.id)
                await interaction.response.send_message("追加しました！")
        else:
            await interaction.response.send_message("この操作をするには`チャンネルの管理`権限が必要です。",ephemeral=True)
    
    @scex_c.command(name="del",description="このチャンネルで無効化します。")
    async def scex_add(self, interaction:discord.Interaction):
        if interaction.user.guild_permissions.manage_channels | interaction.user.guild_permissions.administrator:
            scex = set_sc_ex()
            if scex.get_channel(interaction.channel.id):
                scex.del_channel(interaction.channel.id)
                await interaction.response.send_message("無効にしました！")
            else:
                await interaction.response.send_message("すでに無効化されています。")
        else:
            await interaction.response.send_message("この操作をするには`チャンネルの管理`権限が必要です。",ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(ScExCog(bot))