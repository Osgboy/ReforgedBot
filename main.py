import discord
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

mods = {
	'Modern Hooks': 'MSUTeam/Modern-Hooks',
	'MSU Launcher': 'MSUTeam/MSU',
	'Nested Tooltips Framework': 'MSUTeam/nested-tooltips',
	'Dynamic Perks Framework (DPF)': 'Battle-Modders/Dynamic-Perks-Framework',
	'Unified Perk Descriptions (UPD)': 'Battle-Modders/Unified-Perk-Descriptions',
	'Stack Based Skills': 'Battle-Modders/stack-based-skills',
	'Dynamic Spawns': 'Battle-Modders/Dynamic-Spawns-Framework',
	'Item Tables': 'Battle-Modders/Item-Tables-Framework',
	'Modular Vanilla': 'Battle-Modders/mod_modular_vanilla',
	'Reforged Mod': 'Battle-Modders/mod-reforged'
}


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("\nRunning on the following guilds:")
    for guild in client.guilds:
        print('\t' + guild.name)


def compare_versions(installed: str, newest: str) -> str:
    if installed == newest:
        return f':white_check_mark: {installed} = {newest}'
    else:
        return f':x: {installed} != {newest}'
    

def parse_log(log: str) -> discord.Embed:
    embed = discord.Embed()
    newestBBversion = '1.5.0.15'

    BBversion = re.search(r"<html><head><title>Battle Brothers ([\d\.]*.?)</title>", log).group()
    embed.add_field(name='BB Version', value=compare_versions(BBversion, currentBBversion))
    print(BBversion)
    for name, repo in mods.items():
        installed = re.search(rf"<span style=\"color:#FFFFFF\">{re.escape(name)}</span> (?:.*?) version <span (?:.*?)>([\d\.]*.?)</span>", log).group()
        
        embed.add_field(name=name, value=compare_versions(installed, '1.5.0.15'))
        print(installed)

def embed_log(dict) -> discord.Embed:
    pass


@client.event
async def on_message(message: discord.Message):
    print(message.content)
    for attachment in message.attachments:
        if attachment.filename == 'log.html' and attachment.content_type[:5] == 'text/':
            if attachment.size <= 10000000:
                message.channel.send(embed_log(parse_log(str(attachment.read(), 'UTF-8'))))
            else:
                message.channel.send("Log file exceeds 10 MB!")


client.run(TOKEN)
