from discord.enums import Status
from discord.ext.commands import command, Cog
from discord import Embed, Member
from sqlite3 import connect
import config
from discord.utils import get
db = connect('./data/data.db')
con = db.cursor()

class StarBoardHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ["🌟", "💫","✨", "⭐"]
        self.starboard = 804320221812228107


    @Cog.listener()
    async def on_raw_reaction_add(self, pl):
        message = await self.bot.get_channel(pl.channel_id).fetch_message(pl.message_id)
        if pl.member.bot:
            return
        ch = self.bot.get_channel(self.starboard)
        if not str(pl.emoji) in self.emojis:
            return
        reactions = list(r.emoji for r in message.reactions)
        count = message.reactions[reactions.index(str(pl.emoji))].count
        em = Embed(color=config.color, description=message.content)
        em.add_field(name='Source', value=f"[Jump!]({message.jump_url})")
        em.set_author(name=message.author, icon_url=message.author.avatar_url)
        em.set_footer(text="Vibez PH Starboard")
        if count == 3:
            m = await ch.send(embed=em, content = f"{count} {str(pl.emoji)} {message.channel.mention}")
            con.execute("INSERT INTO starboard (id, mid) VALUES (?, ?)", (message.id, m.id))
            db.commit()
        if count > 3:
            con.execute(f"SELECT * FROM starboard WHERE id = {message.id}")
            res = con.fetchone()
            mess = await ch.fetch_message(list(res)[1])
            await mess.edit(embed=em, content=f"{count} {str(pl.emoji)} {message.channel.mention}")
        if count >= 10:
            role = get(pl.member.guild.roles, id = 803934101542797363)
            if not role in message.author.roles:
                await message.author.add_roles(role)
            else:
                return
        

def setup(bot):
    bot.add_cog(StarBoardHandler(bot))