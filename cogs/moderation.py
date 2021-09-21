from discord.ext.commands import command, Cog, Greedy, has_permissions
from discord import Embed, Member
from discord.utils import get 
from sqlite3 import connect
import config
import asyncio
import json

db = connect('./data/data.db')
c = db.cursor()

def make_data(user):
    c.execute("SELECT * FROM bans WHERE user = ?", (user,))
    res = c.fetchone()
    if res is None:
        c.execute("INSERT INTO bans (user, roles, ban) VALUES (?, ?, ?)", (user, "[]", 0))
        db.commit()
        return user, "[]", 0
    return res

class VibezModeration(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_time(self, str_time: str):
        secs = 0
        t = str_time.split(" ")
        seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        for i in t:
            secs += int(i[:-1]) * seconds_per_unit[i[-1]]
        return secs

    @command()
    async def ban(self, ctx, member: Member):
        role_data = [role.id for role in member.roles]
        c.execute("UPDATE bans SET roles = ?, ban = 1 WHERE user = ?", (str(role_data), member.id))
        db.commit()
        for role in member.roles:
            try: await member.remove_roles(role)
            except: continue
        await member.add_roles(get(ctx.guild.roles, id = 839917167490105354))
        ch = self.bot.get_channel(839917321711779900)
        await ctx.send(embed=Embed(color=config.color, description=f'{member.mention} has been banned.'))
        await ch.send(embed=Embed(color=config.color, description=f'{member.mention} has been banned.'))
        return

    @command()
    async def unban(self, ctx, member: Member):
        user, roles, ban = make_data(member.id)
        if ban == 0:
            return await ctx.send(f"{member.mention} is not banned..")
        if ban == 1:
            c.execute("UPDATE bans SET roles = ?, ban = 0 WHERE user = ?", ("[]", member.id))
            db.commit()
            ch = self.bot.get_channel(839917321711779900)
            roles = json.loads(roles)
            guild = self.bot.get_guild(733175002383253636)
            for role in roles:
                r = get(guild.roles, id = int(role))
                try: await member.add_roles(r)
                except: continue
            await member.remove_roles(get(ctx.guild.roles, id = 839917167490105354))
            await ch.send(embed=Embed(color=config.color, description=f"{member.mention} has been unbanned."))
            await ctx.send(embed=Embed(color=config.color, description=f"{member.mention} has been unbanned."))


def setup(bot):
    bot.add_cog(VibezModeration(bot))