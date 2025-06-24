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

@client.event
async def on_ready():
	logging.info(f'Logged in as {client.user} (ID: {client.user.id}, INVITE: "https://discord.com/outh2/authorize?client_id={client.user.id}&permissions=8&scope=bot")')
	guild = client.get_guild(MY_GUILD.id)

@client.event
async def on_message(message: discord.Message):
	a = random.random()
	for prompt in call_and_response.prompts.items():
		if re.match(prompt[0],message.content,flags=re.IGNORECASE + re.MULTILINE) and a <= prompt[1].chance:
			await message.channel.send(prompt[1].response)
			break

	# use a different random variable to prevent monty hall problem
	b = random.random()
	# tell tristian to shut up
	if message.author.id == 501528347591835648 and b <= 0.1:
		await message.channel.send("lalalala I can't hear you")
	# tell vresod to shut up
	if message.author.id == 431978032094380043 and b <= 0.05:
		await message.channel.send("SHUT THE FUCK UP I HATE YOU!! GOD")
	# correct kav's grammar
	if message.author.id == 793877493958311936 and "your" in message.content.lower() and b <= 0.33:
		await message.channel.send("you're*")

@client.tree.command()
async def echo(interaction:discord.Interaction,text:str):
	"""Possess APOR!"""
	await interaction.channel.send(text)
	await interaction.response.send_message(f'Echoed',ephemeral=True)

if __name__ == "__main__":
	env = dotenv.dotenv_values()
	client.run(env['TOKEN'])