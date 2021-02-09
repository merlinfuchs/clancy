from xenon import *
from xenon.cmd import *
import dc_interactions as dc
from motor.motor_asyncio import AsyncIOMotorClient
import aioredis
import json
from os import environ as env
import asyncio
import traceback
import sys
from datetime import datetime

from util import *


class Xenon(dc.InteractionBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, ctx_klass=CustomContext)
        self.mongo = AsyncIOMotorClient(env.get("MONGO_URL", "mongodb://localhost"))
        self.db = self.mongo.xenon
        self.redis = None
        self.http = None
        self.relay = None

        self._receiver = aioredis.pubsub.Receiver()

    async def on_command_error(self, ctx, e):
        if isinstance(e, asyncio.CancelledError):
            raise e

        elif isinstance(e, MissingWebhookPermissions):
            await ctx.respond("The bot **needs `Manage Webhooks` permissions** for this command.", ephemeral=True)

        else:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            print("Command Error:\n", tb, file=sys.stderr)

            error_id = unique_id()
            await self.redis.setex(f"cmd:errors:{error_id}", 60 * 60 * 24, json.dumps({
                "command": ctx.command.full_name,
                "timestamp": datetime.utcnow().timestamp(),
                "author": ctx.author.id,
                "traceback": tb
            }))
            await ctx.respond_with_source(
                "An unexpected error occurred. Please report this on the "
                "[Support Server](discord.gg/).\n\n"
                f"**Error Code**: `{error_id.upper()}`"
            )

    async def prepare(self):
        self.redis = await aioredis.create_redis_pool(env.get("REDIS_URL", "redis://localhost"))

        ratelimits = rest.RedisRatelimitHandler(self.redis)
        self.http = rest.HTTPClient(self.token, ratelimits)

        await super().prepare()
        # await self.flush_commands()
        self.loop.create_task(self.push_commands())

    def make_request(self, method, path, data=None, **params):
        req = rest.Request(method, path, **params)
        self.http.start_request(req, json=data)
        return req
