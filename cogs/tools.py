import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
from func.database import tag as tag_db

class ToolsCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("ToolsCog")

    class tag1(app_commands.Group):
        pass
    tag = tag1(name="tag", description="サーバータグに関するコマンド (Powerted By Tags Collections)")

    @tag.command(name="search", description="タグを検索します。")
    @app_commands.describe(name="タグの名前")
    async def search_tag(self, interaction:discord.Interaction, name:str):
        tags = tag_db()
        thread = tags.get_tag(name)
        
        if(thread is None):
            await interaction.response.send_message(embed=discord.Embed(
                title="検索",
                description="タグが見つかりませんでした。\nリンクを持っていたら、</tag submit:1392168772382756985>からタグの追加申請をしてみよう！",
                color=0xd450b7
            ))
        else:
            tagth = interaction.guild.get_thread(int(thread[1]))
            oya = tagth.parent.name
            tag = tagth

            await interaction.response.send_message(embed=discord.Embed(
                title="検索",
                description=f"タグ: {tag.name}\nここからサーバーに飛ぶことができます-> {thread[0]}",
                color=0x0bd708
            ))
    
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