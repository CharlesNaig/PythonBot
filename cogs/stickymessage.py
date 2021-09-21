from discord.ext.commands import command, Cog, Greedy, has_any_role, has_permissions
from discord import Embed, TextChannel
from sqlite3 import connect
from asyncio import run_coroutine_threadsafe as safe
import config

db = connect("./data/data.db")
c = db.cursor()

def get_data(ch):
	c.execute(f"SELECT * FROM stick WHERE ch = {ch}")
	result = c.fetchone()
	if result is None:
		c.execute("INSERT INTO stick (ch, message, mode, stick) VALUES (?, ?, ?, ?)", (ch, "message", "normal", 0))
		db.commit()
	c.execute(f"SELECT stick FROM stick WHERE ch = {ch}")
	return c.fetchone()


class ProudBisayaStickMessageHandler(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command()
	@has_permissions(manage_roles=True)
	async def stick(self, ctx, channel: TextChannel, mode, *, message):
		if channel is None:
			return await ctx.send("Please mention a channel.")
		result = get_data(channel.id)
		if not any(mode.lower() == x for x in ["normal", "embed"]):
			return await ctx.send("InvalidArgument, you can only choose any of this modes `embed | normal`")
		c.execute("UPDATE stick SET message = ?, mode = ?, stick = 1 WHERE ch = ?", (message, mode, channel.id))
		db.commit()
		await ctx.send(embed=Embed(color=config.color, description=f"Successfully updated/created the sticky message in {channel.mention}"))

	@command(aliases=['delete-sticky'])
	@has_permissions(manage_roles=True)
	async def delete_stick(self, ctx, channel: TextChannel = None):
		result = get_data(channel.id)
		if result == 0:
			return await ctx.send(f"There are no sticky messages in {channel.mention}")
		c.execute(f"UPDATE stick SET stick = 0 WHERE ch = {channel.id}")
		db.commit()
		await ctx.send(embed=Embed(color=config.color, description=f"Successfully deleted the sticky message in {channel.mention}"))

	@command(aliases=['sticky-channels'])
	@has_permissions(manage_roles=True)
	async def stick_channels(self, ctx):
		c.execute("SELECT ch FROM stick WHERE stick = 1")
		result = c.fetchall()
		result = [list(res)[0] for res in result]
		description = ",".join([self.bot.get_channel(x).mention for x in result])
		await ctx.send(embed=Embed(color=config.color, description=description, title="Enabled Stickied Channels"))

	@Cog.listener()
	async def on_message(self, msg):
		if msg.author == self.bot.user:
			return
		res = get_data(msg.channel.id)
		res = list(res)[0]
		if res == 1:
			c.execute(f"SELECT message, mode FROM stick WHERE ch = {msg.channel.id}")
			message, mode = c.fetchone()
			
			if mode == 'embed':
				safe(msg.channel.purge(limit=5, check = lambda m: m.author == self.bot.user and m.embeds[0].description == message), self.bot.loop)
				safe(msg.channel.send(embed=Embed(color=config.color, description=message)), self.bot.loop)
			elif mode == 'normal':
				safe(msg.channel.purge(limit=5, check = lambda m: m.author == self.bot.user and m.content == message), self.bot.loop)
				safe(msg.channel.send(message), self.bot.loop)

def setup(bot):
	bot.add_cog(ProudBisayaStickMessageHandler(bot))