from discord.ext.commands import command, Cog 
from discord import Embed, Member
import config
from datetime import datetime, timedelta
from discord.utils import get

class Utilities(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['server-info'])
    async def server(self, ctx):
        guild = ctx.guild
        em = Embed(color=config.color)
        em.set_author(name="Tagpuan PH Server Info")
        em.set_thumbnail(url=ctx.guild.icon_url)
        fields = [("ID", f"```{guild.id}```"),
                  ("Date of Creation", (guild.created_at + timedelta(hours=8)).strftime("```%A %B %d,%Y | %I:%M %p ASIA TIME```")),
                  (f"Members [{len(guild.members)}]", f"```Members: {len(list(filter(lambda m: not m.bot, guild.members)))} | Bots: {len(list(filter(lambda m: m.bot, guild.members)))}```"),
                  (f"Channels [{len(guild.channels)}]", f"```Text Channels: {len(guild.text_channels)} | Voice Channels: {len(guild.voice_channels)}```")]
        for name, value in fields:
            em.add_field(name=name, value=value, inline=False)
        em.set_footer(text="/server-info")
        await ctx.send(embed=em)

    @command(aliases=['nn'])
    async def nickname_change(self, ctx, *, nick = None):
        all_star = get(ctx.guild.roles, id = 887879651677077564)
        astro = get(ctx.guild.roles, id = 887879756283019274)
        babe_clan = get(ctx.guild.roles, id = 887879651677077564)
        nn_of_roles = {887879651677077564: "★", 887879756283019274: "⟁", 887879651677077564:"❥"}
        if not ctx.channel.id == 849487803451572264:
            return
        role = get(ctx.guild.roles, id = 866626644231979008)
        if role in ctx.author.roles:
          return await ctx.send(embed=Embed(color=config.color, description = f"**You must have the {role.mention} role**"))
        if nick is None:
            return await ctx.send(embed=Embed(color=config.color, description = f"**:x: Please provide your nickname**"))
        if len(nick) > 24:
            return await ctx.send(embed=Embed(color=config.color, description = f"**:x: Nickname cannot be 25 characters or longer**"))
        if not any(c in ctx.author.roles for c in [all_star, astro, babe_clan]):
            await ctx.author.edit(nick=f"友 {nick}")
            return await ctx.send(f"Nickname changed to `友 {nick}`")
        for role in [all_star, astro, babe_clan]:
            if role in ctx.author.roles:
                await ctx.author.edit(nick=f"{nn_of_roles[role.id]} {nick}")
                await ctx.send(f"Nickname changed to `{nn_of_roles[role.id]} {nick}`")

    @command(aliases=['bot-suggest'])
    async def botsuggest(self, ctx, *, suggestion = None):
        hat = self.bot.get_user(573709909594734603)
        if suggestion is None: return await ctx.send(":x: Invalid Arguments. Provide your suggestion.")
        em = Embed(color=config.color, description=suggestion, timestamp=ctx.message.created_at)
        em.set_footer(text=f"Bot Suggestion | {ctx.author.name}")
        await ctx.send("Your suggestion has been sent successfully to the developer.")
        ch = self.bot.get_channel(849487803451572264)
        await ch.send(embed=em, content=hat.mention)

def setup(bot):
    bot.add_cog(Utilities(bot))