from discord.ext.commands import Cog, command
from discord import Embed, Member, File
from io import BytesIO
from PIL import Image, ImageOps, ImageFont, ImageDraw
import config

with open('./data/vibes.txt', 'r', encoding='utf-8') as text:
    text=text.read()

class VibezWelcomerHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def pic(self, asset):
        asset = BytesIO(await asset.read())
        pfp = Image.open(asset).convert('RGBA')
        return pfp
    
    def border(self, pfp):
        image = Image.open('./data/images/border.png').convert('RGBA')
        image = image.resize(pfp.size)
        pfp.paste(image, (0,0), image)
        return pfp

    def image(self, image):
        f = BytesIO()
        image.save(f, format='PNG')
        f = f.getvalue()
        file = File(fp = BytesIO(f), filename="image.png")
        return file

    def mask(self, pfp):
        l, w = pfp.size
        mask = Image.new('L', (int(l), int(w)), 0)
        praw = ImageDraw.Draw(mask)
        praw.ellipse((0, 0) + (int(l), int(w)), fill=255)
        av = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        av.putalpha(mask)
        return av

    async def get_welcome(self, mem):
        asset = mem.avatar_url_as(size=128)
        pfp = await self.pic(asset)
        pfp = self.mask(pfp)
        pfp = self.border(pfp)
        pfp = pfp.resize((280,280))
        image = Image.open('./data/welcome/wc.png').convert('RGBA')
        image.paste(pfp, (530,20), pfp)
        return image

    @Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        star = self.bot.get_emoji(786913050141261874)
        LP = self.bot.get_emoji(786471462738329621)
        blings = self.bot.get_emoji(786211970939879442)
        HF = self.bot.get_emoji(786471464324169738)
        channel = self.bot.get_channel(809819395282698291)
        await member.send(embed=Embed(color=config.color, description=text))
        image = await self.get_welcome(member)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('./data/fonts/apple.otf', 50)
        l, w = font.getsize(f"{member.name}#{member.discriminator}")
        draw.text(((905-l)/2, 400), f"{member.name}#{member.discriminator}", (255,255,255), font=font)
        font = ImageFont.truetype('./data/fonts/apple regular.otf', 40)
        l, w = font.getsize("WELCOME")
        draw.text(((905-l)/2, 350), "WELCOME", (255,255,255), font=font)
        em = Embed(title="Welcome to Vibezᴾᴴ", color=0x47BFAA,
                   description=f"**{member.mention}, enjoy your stay!**")
        em.set_footer(text=f"We now have {'{:,}'.format(guild.member_count)} members")
        em.set_image(url="attachment://image.png")
        await channel.send(file=self.image(image), embed=em, content = f"{member.mention}")

    @command()
    async def testjoin(self, ctx):
        star = self.bot.get_emoji(786913050141261874)
        LP = self.bot.get_emoji(786471462738329621)
        blings = self.bot.get_emoji(786211970939879442)
        HF = self.bot.get_emoji(786471464324169738)
        member = ctx.author
        channel = ctx.channel
        await ctx.author.send(embed=Embed(color=config.color, description=text))
        image = await self.get_welcome(ctx.author)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('./data/fonts/apple.otf', 50)
        l, w = font.getsize(f"{member.name}#{member.discriminator}")
        draw.text(((905-l)/2, 400), f"{member.name}#{member.discriminator}", (255,255,255), font=font)
        font = ImageFont.truetype('./data/fonts/apple regular.otf', 40)
        l, w = font.getsize("WELCOME")
        draw.text(((905-l)/2, 350), "WELCOME", (255,255,255), font=font)
        em = Embed(title="Welcome to Vibezᴾᴴ", color=0x47BFAA,
                   description=f"**{member.mention}, enjoy your stay!**")
        em.set_footer(text=f"We now have {'{:,}'.format(ctx.guild.member_count)} members")
        em.set_image(url="attachment://image.png")
        await channel.send(file=self.image(image), embed=em, content = f"{member.mention}")


def setup(bot):
    bot.add_cog(VibezWelcomerHandler(bot))
