import discord, aiohttp, re
from discord.ext import commands

TOKEN = input('Token: ')

async def create_session(loop):
    return aiohttp.ClientSession(loop=loop)

class NitroSniper(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = self.loop.run_until_complete(create_session(self.loop))
        
    async def close(self):
        await self.session.close()
        await super().close()

    def check(self, content):
        e = re.compile("(https://)?(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")
        r = e.match(content)
        if r:
            return r.group().split("/")[-1]

    async def on_message(self, message):
        code = self.check(message.content)
        if code and len(code) == 16:
            async with self.session.post(f"https://discord.com/api/v7/entitlements/gift-codes/{code}/redeem?",headers={"authorization":TOKEN,"Content-Type":"application/json"},json={"channel_id":message.channel.id,"payment_source_id":None}) as r:
                res = await r.json() 
                if res.get("message"):
                    print(f"{code} - {res['message']} ({res['code']})")
                if res.get("subscription_plan"):
                    print(f"{code} - {res['subscription_plan']['name']} ({res['gifter_user_id']})")

client = NitroSniper(command_prefix='8===D')
client.run(TOKEN, bot=False)