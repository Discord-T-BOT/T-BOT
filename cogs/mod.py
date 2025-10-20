import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from func.ready import bot_ready_print
from func.tools import color_code
from typing import Union, Optional

class ModCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("ModCog")

    @app_commands.command(name="kick",description="Kick")
    async def kick(self,interaction:discord.Interaction, user:discord.Member, reason:str=None):
        if interaction.user.guild_permissions.kick_members or interaction.user.guild_permissions.administrator:
            await interaction.guild.kick(user=user, reason=reason)
            await interaction.response.send_message(
                content=f"{user.name}は正常にサーバーからKickされました！\n理由:`{reason}`"
            )
        else:
            await interaction.response.send_message("この操作をするには`メンバーのキック`権限が必要です。",ephemeral=True)

    class channel1(app_commands.Group):
        pass
    channel = channel1(name="channel", description="チャンネル操作")
    @channel.command(name="create", description="チャンネルを作成します。")
    async def channel_create(self,interaction:discord.Interaction, name:str, category:discord.CategoryChannel = None):
        if interaction.user.guild_permissions.manage_channels:
            channel = await interaction.guild.create_text_channel(name=name,category=category,reason=f"channel_create command. By:{interaction.user.name}")
            await interaction.response.send_message(embed=discord.Embed(
                title="チャンネルの作成",
                description=f"チャンネルが作成されました。 <#{channel.id}>",
                colour=discord.Colour.green()
            ))
        else:
            await interaction.response.send_message("この操作をするには`チャンネルの管理`権限が必要です。")

    # @channel.command(name="permisson_all",description="指定した権限をすべてのチャンネルで切り替えます。")
    # @app_commands.choices(perm=[
    #     Choice(name="チャンネルを見る",value="read_messages"),
    #     Choice(name="チャンネルの管理",value="manage_channels"),
    #     Choice(name="権限の管理",value="manage_permissions"),
    #     Choice(name="ウェブフックの管理",value="manage_webhooks"),
    #     Choice(name="招待を作成",value="create_instant_invite"),
    #     Choice(name="メッセージを送信",value="send_messages"),
    #     Choice(name="スレッドでメッセージを送信",value="send_messages_in_threads"),
    #     Choice(name="公開スレッドの作成",value="create_public_threads"),
    #     Choice(name="プライベートスレッドの作成",value="create_private_threads"),
    #     Choice(name="埋め込みリンク",value="embed_links"),
    #     Choice(name="ファイルを添付",value="attach_files"),
    #     Choice(name="リアクションの追加",value="add_reactions"),
    #     Choice(name="外部の絵文字を使用する",value="use_external_emojis"),
    #     Choice(name="外部のスタンプを使用する",value="use_external_stickers"),
    #     Choice(name="@everyone、@here、全てのロールにメンション",value="mention_everyone"),
    #     Choice(name="メッセージの管理",value="manage_messages"),
    #     Choice(name="スレッドの管理",value="manage_threads"),
    #     Choice(name="メッセージ履歴を読む",value="read_messages_history"),
    #     Choice(name="テキスト読み上げメッセージを送信する",value="send_tts_messages"),
    #     Choice(name="ボイスメッセージを送信",value="send_voice_messages"),
    #     Choice(name="投票の作成",value="create_polls"),
    #     Choice(name="接続",value="")
    # ])
    
    class role1(app_commands.Group):
        pass

    role = role1(name="role", description="ロールに関する操作を行います。")
    @role.command(name="create",description="ロールを作成します。")
    @app_commands.describe(name="ロール名", color="色(16進数 | ex:02ffda)", mentionable="@メンションを誰でも行えるようにするか", hoist="オンラインメンバーとは別に表示するか")
    async def role_create(self, interaction:discord.Interaction, name:str, color:str=None, mentionable:bool = False, hoist:bool = False):
        if interaction.user.guild_permissions.manage_roles:
            if color:
                colors = color_code(color)
            else:
                colors = discord.Colour.default()
            role = await interaction.guild.create_role(name=name,color=colors, mentionable=mentionable, hoist=hoist, reason=f"role create by {interaction.user.name}")
            await interaction.response.send_message(embed=discord.Embed(
                title="ロールの作成",
                description=f"ロールが作成されました。 <@&{role.id}>",
                colour=colors
            ))
        else:
            await interaction.response.send_message("この操作をするには`ロールの管理`権限が必要です。")
    
    @role.command(name="info",description="ロールの情報を表示します。")
    async def role_info(self, interaction:discord.Interaction, role:discord.Role):
        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"ロール情報",
                description=f"""名前: {role.name}
色: {role.color}
メンションできるか: {role.mentionable}
別表示か: {role.hoist}""",
                color=role.colour
            )
        )
    
    @role.command(name="give", description="ロールを付与します。")
    async def role_give(self, interaction:discord.Interaction, member:discord.Member, role:discord.Role):
        if interaction.user.guild_permissions.manage_roles:
            if role in member.roles:
                await interaction.response.send_message("すでに付与されています。")
            else:
                
                await member.add_roles(role, f"role give by {interaction.user.name}",)
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="ロール付与完了",
                        description=f"<@{member.id}> に <@&{role.id}> を付与しました。"
                    )
                )
        else:
            await interaction.response.send_message("この操作をするには`ロールの管理`権限が必要です。")
    
    @role.command(name="remove",description="ロールを剥奪します。")
    async def role_remove(self, interaction:discord.Interaction, member:discord.Member, role:discord.Role):
        if interaction.user.guild_permissions.manage_roles:
            if role in member.roles:
                await member.remove_roles(role=role, reason=f"role remove by {interaction.user.name}")
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="ロール剥奪完了",
                        description=f"<@{member.id}> に <@&{role.id}> を剥奪しました。"
                    )
                )
            else:
                await interaction.response.send_message("付与されていません。")
        else:
            await interaction.response.send_message("この操作をするには`ロールの管理`権限が必要です。")

    @role.command(name="color", description="ロールの色を変更します。")
    async def role_color(self, interaction:discord.Interaction, role:discord.Role, color:str):
        if interaction.user.guild_permissions.manage_roles:
            old = role.colour
            if color.lower() == "reset":
                colors = discord.Colour.default()
            else:
                colors = color_code(color)
            
            await role.edit(colour=colors, reason=f"role remove by {interaction.user.name}")
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="ロール色変更完了",
                    description=f"{old} -> {colors}",
                    colour=colors
                )
            )
        else:
            await interaction.response.send_message("この操作をするには`ロールの管理`権限が必要です。")

    @role.command(name="name", description="ロールの名前を変更します")
    async def role_name(self, interaction:discord.Interaction, role:discord.Role, name:str):
        if interaction.user.guild_permissions.manage_roles:
            old = role.name
            await role.edit(name=name, reason=f"role edit name by {interaction.user.name}")
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="ロール名変更完了",
                    description=f"{old} -> {name}",
                    colour=role.colour
                )
            )
        else:
            await interaction.response.send_message("この操作をするには`ロールの管理`権限が必要です。")
    
    @role.command(name="hoist", description="ロールをオンラインメンバーとは別に表示するかの設定を変更します。")
    async def role_hoist(self, interaction:discord.Interaction, role:discord.Role, bool:bool):
        if interaction.user.guild_permissions.manage_roles:
            old = role.hoist
            await role.edit(hoist=bool, reason=f"role edit hoist by {interaction.user.name}")
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="ロール表示設定変更",
                    description=f"{old} -> {bool}",
                    colour=role.colour
                )
            )
        else:
            await interaction.response.send_message("この操作をするには`ロールの管理`権限が必要です。")
    
    

async def setup(bot):
    await bot.add_cog(ModCog(bot))