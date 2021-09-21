from discord.ext.commands import Cog, command 
from discord import Embed
from discord.utils import get


class StatusSupporter(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_member_update(self, before, after):
		guild = self.bot.get_guild(774633117918035969)
		role = get(guild.roles, id = 885704798140248064)
		status = ["https://discord.gg/eFyDY2Ndh5", "discord.gg/tagpuanph", "discord.gg/eFyDY2Ndh5", "https://discord.gg/tagpuanph"]
		if any(x in str(after.activities) for x in status):
			print("StatusSupporter Loaded")
			if not role in after.roles:
				await after.add_roles(role)
			else:
				return
		else:
			if role in after.roles:
				await after.remove_roles(role)
			else:
				return

def setup(bot):
	bot.add_cog(StatusSupporter(bot))