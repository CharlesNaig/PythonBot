from discord.ext.commands import Cog, command
from discord import Embed
from asyncio import sleep

color = 0x47BFAA
emoji = "<:red:854875046173999105>"
"<:creditstoTW:862573705901375529>"
class INTRODUCTION(Cog):
	def __init__(self, bot):
		self.client = bot

	@command(pass_context=True)
	async def intro(self, ctx):
		emoji1 = self.client.get_emoji(842310019520921610)
		emoji2 = self.client.get_emoji(842310113578450964)
		left = self.client.get_emoji(843673553617289276)
		right = self.client.get_emoji(865063545002393621)
		ID = self.client.get_emoji(862573705901375529)
		sign = self.client.get_emoji(862573927317766164)
		tagpuan = self.client.get_emoji(887873249701163018)
		if ctx.guild:
			await ctx.send(embed=Embed(color=color, description=f"{emoji} **Only This Introduction can be only through DM**"))
			return
		questions = [f"{emoji1} **Please input your Name**",
					 f"{emoji2} __**Please input you nickname**__",
					 f"{emoji1} __**Please input your Age**__",
					 f"{emoji2} __**Please input you Gender**__",
					 f"{emoji1} __**Please input your Relationship Status**__",
					 f"{emoji2} __**Please input you Birthdate**__",
					 f"{emoji1} __**Please input your Nationality**__",
					 f"{emoji2} __**What are your hobbies?**__",
					 f"{emoji1} __**What are the things you like?**__",
					 f"{emoji2} __**What are the things you don't like?**__",
					 f"{emoji1} __**Describe yourself**__",
					 f"{emoji2} __**What is your motto?**__"]
		message = await ctx.send(embed=Embed(color=color, description=f"           {left} I N T R O D U C T I O N {right}\n\nPlease wait for 5 seconds..."))
		await sleep(5)
		answers = []
		for question in questions:
			await message.edit(embed=Embed(color=color, description=question))
			answer = await self.client.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
			answers.append(str(answer.content))
		fields = [f"╭ {ID}╔════════◥◣◆◢◤════════╗\n{emoji1} **ID:** __{ctx.author.id}__\n{emoji2} **Name**",
				  f"{emoji2} **Nickname**",
				  f"{emoji1} **Age**",
				  f"{emoji2} **Gender**",
				  f"{emoji1} **Relationship Status**",
				  f"{emoji2} **Birthdate**",
				  f"{emoji1} **Nationality**",
				  f"{emoji2} **Hobbies**",
				  f"{emoji1} **Likes**",
				  f"{emoji2} **Dislikes**",
				  f"{emoji1} **Describe yourself**",
				  f"{emoji2} **Motto**"]
		em = Embed(color=color, title=f"{tagpuan} INTRODUCTION").set_thumbnail(url=ctx.author.avatar_url)
		em.description= '\n'.join([f"{fields[idx]}: __{ans}__" for idx, ans in enumerate(answers)]) + f"\n╰{sign}╚════════◢◤◆◥◣════════╝"
		channel = self.client.get_channel(800578313490923521)
		await channel.send(embed=em, content=str(ctx.author.mention))
		await ctx.send("**Your Introduction was sent successfully**")


def setup(bot):
	bot.add_cog(INTRODUCTION(bot))