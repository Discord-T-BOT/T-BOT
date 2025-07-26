import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print

class ToolsCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("ToolsCog")

    class tag1(app_commands.Group):
        pass
    tag = tag1(name="tag", description="サーバータグに関するコマンド (Powerted By Tags Collections)")

    @tag.command(name="search",description="サーバータグを検索します。")
    @app_commands.describe(name="タグの名前")
    async def search_tag(self, interaction:discord.Interaction, name:str):
        normal = self.bot.get_channel(1384535117199839272)
        nsfw = self.bot.get_channel(1384544581063802900)#1384544581063802900
        join_seigen = self.bot.get_channel(1390436292411785317)#1390436292411785317
        threads = normal.threads
        threads.extend(nsfw.threads)
        threads.extend(join_seigen.threads)
        thread = [i for i in threads if i.name.lower() == name.lower()]
        # print(thread)
        # print(len(thread))
        
        if(len(thread) == 0):
            await interaction.response.send_message(embed=discord.Embed(
                title="検索",
                description="タグが見つかりませんでした。\nリンクを持っていたら、</tag submit:1392168772382756985>からタグの追加申請をしてみよう！",
                color=0xd450b7,
            ),ephemeral=True)
        else:
            oya = thread[0].parent.name
            tag = thread[0]
            
            message1 = tag.get_partial_message(tag.id)
            message2 = await message1.fetch()
            await interaction.response.send_message(embed=discord.Embed(
                title="検索",
                description=f"タグ: {tag.name}\nここからサーバーに飛ぶことができます-> {message2.content}\n分類: {oya}",
                color=0x0bd708
            ),ephemeral=True)
    
    @tag.command(name="submit", description="新しいタグを申請します。")
    async def tag_submit(self, interaction:discord.Interaction, name:str, invite:str):
        if len(name) > 4:
            await interaction.response.send_message("タグの名前は4文字までです。", ephemeral=True)
        else:
            try:
                invites = await self.bot.fetch_invite(url=invite)
                channel = self.bot.get_channel(1392165674532470845)
                await channel.send(f"{name} , {invites.url}\n{interaction.user.name}")
                await interaction.response.send_message("申請しました！",ephemeral=True)
            except (discord.NotFound, discord.HTTPException) as e:
                await interaction.response.send_message(f"エラーが発生しました。\n`{e}`\n存在しない招待の可能性があります。")


async def setup(bot):
    await bot.add_cog(ToolsCog(bot))