from discord.ext.commands import command, Cog, Greedy, has_permissions
from discord import Embed, TextChannel
from sqlite3 import connect
from json import load, dump
import config

def get_data():
	with open("./data/dbs/message.json", "r") as f:
		return load(f)

def commit(data):
	with open("./data/dbs/message.json", "w") as wf:
		dump(data, wf)
	return True

def get_time_format(num):
	if num < 60:
		return f"{num}s"
	if num < 3600:
		return f"{num/60}m"
	if num < 60*60*24:
		return f"{num/60/60}h"
	else:
		return f"{num/60/60/24}d"

class GreetingsHandler(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(aliases=['enable-greeting'])
	@has_permissions(manage_roles=True)
	async def enable_greeting(self, ctx, channels: Greedy[TextChannel]):
		if not len(channels):
			return await ctx.send("Please mention a channel or two.")
		data = get_data()
		for channel in channels:
			if not channel.id in data['channels']:
				data['channels'].append(channel.id)
		commit(data)
		await ctx.send("The welcome greeting was successfully enabled in those mentioned channels.")

	@command(aliases=['disable-greeting'])
	@has_permissions(manage_roles=True)
	async def disable_message(self, ctx, channels: Greedy[TextChannel]):
		if not len(channels):
			return await ctx.send("Please mention a channel or two.")
		data = get_data()
		for channel in channels:
			if channel.id in data['channels']:
				data['channels'].remove(channel.id)
			else:
				continue

		commit(data)
		await ctx.send("The welcome greeting was successfully disabled in those mentioned channels.")

	@command(aliases=['greeting-status'])
	async def greeting_status(self, ctx):
		data = get_data()
		
		if data['status'] is False:
			return await ctx.send("The message was not yet configured, use `/configure-greeting`")
		else:
			description = '\n'.join([f"{self.bot.get_channel(x)} : [{x}]" for x in data['channels']])
			if not len(data['channels']):
				description = "No Channels Configured."
			em = Embed(color=config.color, title="Welcome Greeting Status")
			fields = [("Channels", description),
					  ("Time", get_time_format(data['time'])),
					  ("Embed", data['embed'])]
			for name, value in fields:
				em.add_field(name=name, value=value, inline=False)
			em.set_footer(text="Greeting System")
			await ctx.send(embed=em)

	@command(aliases=['configure-greeting'])
	@has_permissions(manage_roles=True)
	async def edit_greeting_message(self, ctx):
		await ctx.send("Please type your message below.\n\nPossible controls: `{membercount}`, `{membername}`, `{membermention}`")
		m = await self.bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
		content = m.content
		data = get_data()
		data['message'] = content
		data['status'] = True
		await ctx.send("Greeting was successfully configured!")
		commit(data)

	@command(aliases=['edit-duration'])
	@has_permissions(manage_roles=True)
	async def edit_duration(self, ctx, time):
		if not any(time.lower().endswith(x) for x in ['s', 'm', 'h', 'd']):
			return await ctx.send("Invalid time format, use the following: `s|m|h|d`")
		def get_seconds(time):
			if time.lower().endswith("s"):
				return int(time[:-1])
			if time.lower().endswith("m"):
				return int(time[:-1])*60
			if time.lower().endswith("h"):
				return int(time[:-1])*60*60
			if time.lower().endswith("d"):
				return int(time[:-1])*60*60*24
		data = get_data()
		data['time'] = get_seconds(time)
		commit(data)
		return await ctx.send(f"Duration of the message was succesffully changed to `{time}`")


	@command(aliases=['greet-test'])
	@has_permissions(manage_roles=True)
	async def greetingtest(self, ctx):
		mem = ctx.author
		data = get_data()
		content = data['message'].replace("{membercount}", str(len(ctx.guild.members))).replace("{membername}", str(mem.name)).replace("{membermention}",str(mem.mention))
		if data['embed'] == False:
			return await ctx.send(content, delete_after = data['time'])
		em = Embed(color=config.color, description=content)
		await ctx.send(embed=em, delete_after=data['time'])

	@command(aliases=["edit-greeting-mode"])
	@has_permissions(manage_roles=True)
	async def edit_greetings_mode(self, ctx, mode):
		if not any(mode.lower() == c for c in ["embed", "normal"]):
			return await ctx.send("Invalid mode, you can only use `normal` or `embed`")
		data = get_data()
		if mode.lower() == 'normal':
			data['embed'] = False
		else:
			data['embed'] = True
		commit(data)
		await ctx.send(f"Greetings has been set successfully to `{mode}`")

	@Cog.listener()
	@has_permissions(manage_roles=True)
	async def on_member_join(self, mem):
		data = get_data()
		if not len(data['channels']):
			return
		for channel in data['channels']:

			ch = self.bot.get_channel(channel)
			if ch is None:
				continue
			content = data['message'].replace("{membercount}", str(len(mem.guild.members))).replace("{membername}", str(mem.name)).replace("{membermention}",str(mem.mention))
			if data['embed'] == False:
				return await ch.send(content, delete_after = data['time'])
			em = Embed(color=config.color, description=content)
			await ch.send(embed=em, delete_after=data['time'])


def setup(bot):
	bot.add_cog(GreetingsHandler(bot))