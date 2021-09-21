from discord.ext.commands import Bot, when_mentioned_or
from discord import Intents, Activity, ActivityType, Status
from discord.ext.commands.core import command
import config
from pathlib import Path
from keep_alive import keep_alive
keep_alive()


class Tagpuan_PH_2_0(Bot):
    def __init__(self):
        self.owner_ids = [481374570130046976, 817701164258689054]
        super().__init__(command_prefix=when_mentioned_or("/"), intents=Intents.all())

    def setup(self):
        cogs = [u.stem for u in Path(".").glob("./cogs/*.py")]
        for cog in cogs:
            self.load_extension(f'cogs.{cog}')
    
    def run(self):
        self.setup()
        super().run(config.token, reconnect=True)

    async def on_ready(self):
        await self.change_presence(status=Status.online,
                                   activity=Activity(type=ActivityType.watching,
                                                     name="Tagpuan PH"))
        print("Bot is ready.")


def main():
    bot = Tagpuan_PH_2_0()
    bot.run()

if __name__ == '__main__':
    main()