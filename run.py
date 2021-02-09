import asyncio
from os import environ as env
from aiohttp import web

from bot import Xenon
from modules import ascii, transform, utils, fun, info


bot = Xenon(
    public_key=env.get("PUBLIC_KEY"),
    token=env.get("TOKEN"),
    guild_id=env.get("GUILD_ID")
)
modules = {
    ascii.AsciiModule,
    transform.TransformModule,
    utils.UtilsModule,
    fun.FunModule,
    info.InfoModule
}
for module in modules:
    bot.load_module(module(bot))

app = web.Application()


@app.on_startup.append
async def prepare_bot(*_):
    await bot.prepare()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app.add_routes([web.post("/entry", bot.aiohttp_entry)])
    web.run_app(app, host=env.get("HOST", "127.0.0.1"), port=env.get("PORT"))
