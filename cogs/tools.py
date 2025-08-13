import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
from func.database import tag as tag_db
from func.database import set_auto_pub
from func.data import HELP_Commands

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
    
    class auto_pub(app_commands.Group):
        pass

    a_pub = auto_pub(name="pub",description="アナウンス公開設定")

    @a_pub.command(name="add", description="アナウンスを自動で公開します。")
    async def auto_publish(self, interaction:discord.Interaction, channel:discord.TextChannel = None):
        if interaction.user.guild_permissions.manage_channels | interaction.user.guild_permissions.administrator:
            pub = set_auto_pub()
            channels = channel | interaction.channel
            if pub.get_channel(channels.id):
                await interaction.response.send_message("すでに有効化されています。")
            else:
                if channels.is_news():
                    pub.add_channel(channels.id)
                    await interaction.response.send_message("追加しました！")
                else:
                    await interaction.response.send_message("このチャンネルはアナウンスチャンネルではありません。")
        else:
            await interaction.response.send_message("この操作をするには`チャンネルの管理`権限が必要です。",ephemeral=True)
    
    @a_pub.command(name="del", description="アナウンス公開をオフにします")
    async def auto_publish_del(self, interaction:discord.Interaction):
        if interaction.user.guild_permissions.manage_channels | interaction.user.guild_permissions.administrator:
            pub = set_auto_pub()
            if pub.get_channel(interaction.channel.id):
                pub.del_channel(interaction.channel.id)
                await interaction.response.send_message("無効にしました！")
            else:
                await interaction.response.send_message("すでに無効化されています。")
        else:
            await interaction.response.send_message("この操作をするには`チャンネルの管理`権限が必要です。",ephemeral=True)
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        pub = set_auto_pub()
        res = pub.get_channel(message.channel.id)
        if res:
            await message.publish()
    
    @app_commands.command(name="help", description="ヘルプ")
    async def help_command(self, interaction:discord.Interaction, command:str=None):
        if(command):
            if(command in HELP_Commands.keys()):
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=command,
                        description=HELP_Commands[command],
                        color="#00ff00"
                    )
                )
            else:
                await interaction.response.send_message("コマンドが見つかりませんでした。グループの場合は、 `fun kusa`のようにグループとコマンドをつけてお試しください。")
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="T-BOT ヘルプ",
                    description="""**コマンド一覧**

                    /bal
                    /channel create
                    /fun kaso_gif
                    /fun kick_vc
                    /fun kusa
                    /help
                    /kick
                    /role color
                    /role create
                    /role give
                    /role hoist
                    /role info
                    /role name
                    /role remove
                    /tag search
                    /tag submit
                    /work
                    """
                )
            )


async def setup(bot):
    await bot.add_cog(ToolsCog(bot))