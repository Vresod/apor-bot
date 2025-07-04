import logging
import re

import dotenv
import discord
from discord import app_commands
from discord.ext import tasks
import sys
import random

import call_and_response

# CONSTS
MY_GUILD = discord.Object(id=1373444116700205178)
STARBOARD_CHANNEL = discord.Object(id=1389822600124825600)
PIN_EMOJIS = {"💀","⭐","📌"}

class MyClient(discord.Client):
	def __init__(self):
		intents = discord.Intents.default()
		intents.message_content = True
		super().__init__(intents=intents)
		# A CommandTree is a special type that holds all the application command
		# state required to make it work. This is a separate class because it
		# allows all the extra state to be opt-in.
		# Whenever you want to work with application commands, your tree is used
		# to store and work with them.
		# Note: When using commands.Bot instead of discord.Client, the bot will
		# maintain its own tree instead.
		self.tree = app_commands.CommandTree(self)

	# In this basic example, we just synchronize the app commands to one guild.
	# Instead of specifying a guild to every command, we copy over our global commands instead.
	# By doing so, we don't have to wait up to an hour until they are shown to the end-user.
	async def setup_hook(self):
		# This copies the global commands over to your guild.
		self.tree.copy_global_to(guild=MY_GUILD)
		await self.tree.sync(guild=MY_GUILD)


client = MyClient()
discord.utils.setup_logging(level=logging.DEBUG)
debugging = hasattr(sys, 'gettrace') and sys.gettrace() is not None

# directly copied and pasted from lunch table
async def pin_message(message: discord.Message, starboard: discord.TextChannel):
	embed = discord.Embed(
		title=f"#{message.channel}",
		description=message.content,
		url=f"https://discord.com/channels/{message.guild.id}/{message.channel.id}"
	)
	embed.set_author(name=message.author.display_name, icon_url=str(message.author.avatar))
	# embed.set_footer(text=f"[Jump]({message.jump_url})")
	embed.add_field(name="Original Message:", value=f"[Jump]({message.jump_url})")
	if len(message.attachments) > 0:
		embed.set_image(url=message.attachments[0].url)
	await starboard.send(embed=embed, content="", allowed_mentions=discord.AllowedMentions.none())

@client.event
async def on_ready():
	logging.info(f'Logged in as {client.user} (ID: {client.user.id}, INVITE: "https://discord.com/outh2/authorize?client_id={client.user.id}&permissions=8&scope=bot")')
	guild = client.get_guild(MY_GUILD.id)

@client.event
async def on_message(message: discord.Message):
	# because `and` only evaluates the second condition if the first one is falsy, it isn't actually an optimization
	# to store a random variable and use it multiple times.
	# it's better for readability, imo, to just call `random.random()` each time.
	for prompt in call_and_response.prompts.items():
		if re.match(prompt[0],message.content,flags=re.IGNORECASE + re.MULTILINE) and random.random() <= prompt[1].chance:
			await message.channel.send(prompt[1].response)
			return

	# tell tristian to shut up
	if message.author.id == 501528347591835648 and random.random() <= 0.0667: # 1/15
		await message.channel.send("lalalala I can't hear you")
		return
	# tell vresod to shut up
	if message.author.id == 431978032094380043 and random.random() <= 0.03333: # 1/30
		await message.channel.send("SHUT THE FUCK UP I HATE YOU!! GOD")
		return
	# correct kav's grammar
	if message.author.id == 793877493958311936 and "your" in message.content.lower() and random.random() <= 0.41667: # 2/3
		await message.channel.send("you're*")
		return

	if random.random() <= 0.00667: # 1/150
		await message.channel.send("AHH!!! HELP!!!!!!!!!! HELP ME!!!! IT'S UNBEARABLE PLEASE HELP!!!!!! AAAAGGGHHHHHHH")
		return

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
	if payload.emoji.name not in PIN_EMOJIS:
		return
	message: discord.Message = await (client.get_channel(payload.channel_id).get_partial_message(payload.message_id)).fetch()
	starboard: discord.TextChannel = client.get_channel(STARBOARD_CHANNEL.id)
	for reaction in message.reactions:
		if reaction.count != 2 and reaction.emoji in PIN_EMOJIS:
			return
	await pin_message(message, starboard)

@client.tree.command()
async def echo(interaction:discord.Interaction,text:str):
	"""Possess APOR!"""
	await interaction.channel.send(text)
	await interaction.response.send_message(f'Echoed',ephemeral=True)

if __name__ == "__main__":
	env = dotenv.dotenv_values()
	client.run(env['TOKEN'])