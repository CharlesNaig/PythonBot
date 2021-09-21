from discord.ext.commands import Cog, command, has_any_role
from discord import Embed, Member, File
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import textwrap

class ImageManipulator(Cog):
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

    @command()
    @has_any_role(757287613404151898, 769223107050340434)
    async def album(self, ctx, *, arg: str = None):
    	if arg is None:
    		await ctx.send("**Please provide text**")
    		return
    	if len(arg) >= 35:
    		await ctx.send("**Your text must be less than or equal to 35 characters**")
    		return
    	pfp = await self.pic(ctx.author.avatar_url_as(size=128))
    	pfp = pfp.resize((164, 164))
    	image = Image.open('./data/images/album.jpg').convert('RGBA')
    	font = ImageFont.truetype('./data/fonts/apple regular.otf', 17)
    	font1 = ImageFont.truetype('./data/fonts/apple.otf', 15)
    	draw = ImageDraw.Draw(image)
    	w, h = font.getsize(arg)
    	W, H = font1.getsize(ctx.author.name)
    	draw.text(((320-w)/2, 245), arg, (255,255,255), font=font)
    	draw.text(((320-W)/2, 265), ctx.author.name, (255,255,255), font=font1)
    	image.paste(pfp, (78,70), pfp)
    	await ctx.send(file=self.image(image))   


    @command()
    @has_any_role(757287613404151898, "Achieve 2")
    async def player(self, ctx, *, arg: str = None):
    	if arg is None:
    		await ctx.send("**Please provide text**")
    		return
    	if len(arg) >= 35:
    		await ctx.send("**Your text must be less than or equal to 35 characters**")
    		return
    	pfp = await self.pic(ctx.author.avatar_url_as(size=128))
    	pfp = pfp.resize((164, 164))
    	image = Image.open('./data/images/player.jpg').convert('RGBA')
    	font = ImageFont.truetype('./data/fonts/apple regular.otf', 17)
    	font1 = ImageFont.truetype('./data/fonts/apple.otf', 15)
    	draw = ImageDraw.Draw(image)
    	w, h = font.getsize(arg)
    	W, H = font.getsize(ctx.author.name)
    	draw.text(((320-w)/2, 245), arg, (255,255,255), font=font)
    	draw.text(((320-W)/2, 265), ctx.author.name, (255,255,255), font=font1)
    	image.paste(pfp, (78,70), pfp)
    	await ctx.send(file=self.image(image))

    @command()
    @has_any_role(757287613404151898, "Achieve 2")
    async def tab(self, ctx, *, arg = None):
    	if arg is None:
    		return await ctx.send("Please provide text.")
    	if len(arg) > 600:
    		return await ctx.send("Should not be more than 600 characters")
    	image = Image.open('./data/images/alb.png').convert('RGBA')
    	draw = ImageDraw.Draw(image)
    	font = ImageFont.truetype('./data/fonts/apple regular.otf', 17)
    	arg = '\n'.join(textwrap.wrap(arg, 50))
    	draw.text((100,220), arg, (0,0,0), font=font)
    	await ctx.send(file=self.image(image))

    @command()
    @has_any_role("Achieve")
    async def vtab(self, ctx, *, arg = None):
        if arg is None:
            return await ctx.send("Please provide text.")
        if len(arg) > 100:
            return await ctx.send("Text must not be more than 50 characters.")
        image = Image.open('./data/images/persento.png')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('./data/fonts/apple.otf', 25)
        draw.text((71, 202), '\n'.join(textwrap.wrap(arg, 40)), (0,0,0), font)
        await ctx.send(file=self.image(image))

    @command(aliases=['border'])
    async def _border(self, ctx):
        mem = ctx.author
        asset = mem.avatar_url_as(size=128)
        pfp = await self.pic(asset)
        pfp = self.mask(pfp)
        pfp = self.border(pfp)
        await ctx.send(file=self.image(pfp))
    

def setup(bot):
    bot.add_cog(ImageManipulator(bot))