import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from os import getenv, listdir
from datetime import datetime, timedelta
from discord import Status, app_commands
from typing import List
import asyncio
import sys
import json
from dotenv import load_dotenv
load_dotenv()
from func.tools import is_bot_admin, kusa, Sender_Guild

now_status = 0

@tasks.loop(seconds=20)
async def status():
    global now_status

    if now_status == 0:
        data1 = discord.Activity(type=discord.ActivityType.playing, name="T-BOT | TAMAGO55123")
        now_status = 1
    elif now_status == 1:
        data1 = discord.Activity(type=discord.ActivityType.competing, name=f"{len(bot.guilds)}サーバー")
        now_status =0

    await bot.change_presence(activity=data1)



async def main(bot:commands.Bot):

    @bot.event
    async def on_ready():
        print(f'{bot.user} としてログインしました^o^')
        status.start()
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} commands')
        except Exception as e:
            print(f'Error syncing commands: {e}')
        # 起動したことを送信
        await send_update_message()

    for cog in listdir("cogs"):
        if cog.endswith(".py"):
            await bot.load_extension(f"cogs.{cog[:-3]}")

    @bot.tree.context_menu(name="草を生やしまくる")
    async def kusa_boubou(interaction:discord.Interaction, message:discord.Message):
            
            await interaction.response.defer(thinking=True)
            for i in kusa:
                if i not in message.reactions:
                    await message.add_reaction(i)
            await interaction.followup.send(content="草を生やしました。")
    
    class SendEmbedModal(discord.ui.Modal):
        def __init__(self, channel:discord.TextChannel, message:str):
            super().__init__(
                title="フォーム",
                timeout=None,
            )

            self.messages = discord.ui.TextInput(
                label="Color Code",
                style=discord.TextStyle.short,
                max_length=6,
                required=False,
            )
            self.add_item(self.messages)

            self.channel = channel
            self.message = message

        async def on_submit(self, interaction:discord.Interaction):
            if self.messages.value:
                a = int(f"0x{self.messages.value}", 16)
            else:
                a = None
            await self.channel.send(embed=discord.Embed(description=self.message, color=a))
            await interaction.response.send_message("sended.",ephemeral=True)

    @bot.tree.context_menu(name="メッセージを再送信",guilds=Sender_Guild)
    async def message_re_send(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            await message.channel.send(content=message.content, embeds=message.embeds)
            await interaction.response.send_message(content="sended.",ephemeral=True)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)

    @bot.tree.context_menu(name="メッセージを埋め込みに変換",guilds=Sender_Guild)
    async def message_send_embed(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            modal = SendEmbedModal(channel=message.channel, message=message.content)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)
    
    class SendModal(discord.ui.Modal):
        def __init__(self, channel:discord.TextChannel, ifembed:bool,user:discord.Member):
            super().__init__(
                title="フォーム",
                timeout=None,
            )

            self.messages = discord.ui.TextInput(
                label="メッセージ",
                style=discord.TextStyle.paragraph,
                required=True,
            )
            self.add_item(self.messages)

            self.channel = channel
            self.ifembed = ifembed
            self.user = user

        async def on_submit(self, interaction:discord.Interaction):
            if self.ifembed:
                a = await self.channel.send(embed=discord.Embed(description=self.messages))
            else:
                a = await self.channel.send(content=self.messages)
            await interaction.response.send_message("sended.",ephemeral=True)

    @bot.tree.command(name="send", description="送信", guilds=Sender_Guild)
    async def send(interaction:discord.Interaction, channel:discord.TextChannel = None, ifembed:bool = True):
        if interaction.user.guild_permissions.administrator:
            if channel == None:
                send_channel = interaction.channel
            else:
                send_channel = channel
            modal = SendModal(channel=send_channel,ifembed=ifembed,user=interaction.user)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)

    async def send_update_message():
        update_id = 1391902989069058050
        update = await bot.fetch_channel(update_id)
        embed = discord.Embed(title='BOTが起動しました^o^',description="BOTが起動されました",color=0x0004ff,timestamp=datetime.now())
        await update.send(embed=embed)
    
    await bot.start(getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True

    bot = commands.Bot(command_prefix="t!", intents=intents)
    discord.utils.setup_logging()
    asyncio.run(main(bot))
