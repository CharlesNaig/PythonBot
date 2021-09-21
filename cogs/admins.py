from discord.ext.commands import Cog, command, Greedy, is_owner, has_permissions
from discord import Embed, TextChannel, Status, Activity, ActivityType, File
import config
from io import BytesIO
from PIL import Image 
import requests

def save_image(image):
    f = BytesIO()
    image.save(f, format='PNG')
    f = f.getvalue()
    file = File(fp = BytesIO(f), filename="image.png")
    return file

class AdminCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @has_permissions(manage_roles=True)
    async def status(self, ctx, *, arg):
        await self.bot.change_presence(status=Status.online,
                                       activity=Activity(type=ActivityType.watching,
                                                         name=arg))
        await ctx.send("Status changed successfully")

    @command()
    @has_permissions(manage_roles=True)
    async def send(self, ctx, channel: TextChannel, *, arg = None):
        if arg is None:
            return await ctx.send("Please provide text.")
        em = Embed(color=config.color, description=arg)
        em.set_footer(text="Tagpuan PH")
        if ctx.message.attachments:
            em.set_image(ctx.message.attachments[0].url)
        await channel.send(embed=em)

    @command()
    @has_permissions(manage_roles=True)
    async def say(self, ctx, channel: TextChannel, *, arg = None):
        if arg is None:
            return await ctx.send("Please provide text.")
        if ctx.message.attachments:
            im = Image.open(requests.get(ctx.message.attachments[0].url, stream=True).raw)
            return await channel.send(content=arg, file=save_image(im))
        await channel.send(arg)

    @command(aliases=["edit-message"])
    @has_permissions(manage_roles=True)
    async def edit_message(self, ctx, link: str = None):
        if link is None:
            return await ctx.send("Please provide the jump url of the message that you will edit.")
        if not any(link.startswith(x) for x in ["https://discord.com/channels/", "https://discordapp.com/channels/"]):
            return await ctx.send("InvalidMessageURL, please provide a valid message url..")
        link = link.split("/")
        ch_id, message_id = link[5], link[6]
        message = await self.bot.get_channel(int(ch_id)).fetch_message(int(message_id))
        if message is None or message.author != self.bot.user:
            return await ctx.send("Invalid Message or the message is not mine..")
        await ctx.send("Please enter the message...")
        m = await self.bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
        content = m.content
        if m.attachments:
            content = f"{content}\n{m.attachments[0].url}"
        await message.edit(content=content)
        await ctx.send("Message edited successfully!")

    @command(aliases=["edit-embed"])
    @has_permissions(manage_roles=True)
    async def edit_embed(self, ctx, link: str = None):
        if link is None:
            return await ctx.send("Please provide the jump url of the message that you will edit.")
        if not any(link.startswith(x) for x in ["https://discord.com/channels/", "https://discordapp.com/channels/"]):
            return await ctx.send("InvalidMessageURL, please provide a valid message url..")
        link = link.split("/")
        ch_id, message_id = link[5], link[6]
        message = await self.bot.get_channel(int(ch_id)).fetch_message(int(message_id))
        if message is None or message.author != self.bot.user:
            return await ctx.send("Invalid Message or the message is not mine..")
        await ctx.send("Please enter the message...")
        m = await self.bot.wait_for('message', check =  lambda m: m.author == ctx.author and m.channel == ctx.channel)
        content = m.content
        em = Embed(color=config.color, description=content)
        if m.attachments:
            em.set_image(m.attachments[0].url)
        em.set_footer(text="Vibez PH")
        await message.edit(embed=em, content=None)
        await ctx.send("Message edited successfully!")

    @command()
    @has_permissions(manage_roles=True)
    async def purge(self, ctx, num):
        await ctx.channel.purge(limit=int(num)+1)
        await ctx.send("Purge Successful", delete_after=2)


def setup(bot):
    bot.add_cog(AdminCommands(bot))