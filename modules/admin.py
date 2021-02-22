import json
from datetime import datetime

from dbots.cmd import *


class AdminModule(Module):
    @Module.command()
    async def error(self, ctx, error_id: str.lower):
        """
        Get information about an error
        """
        allowed = False
        app = await ctx.bot.http.get_application()
        if ctx.author.id == app["owner"]["id"]:
            allowed = True

        else:
            team = app.get("team")
            if team is not None:
                members = [tm["user"]["id"] for tm in team["members"]]
                if ctx.author.id in members:
                    allowed = True

        if not allowed:
            await ctx.respond("This command can **only** be used by the **bot owner(s)**.", ephemeral=True)

        error = await ctx.bot.redis.get(f"cmd:errors:{error_id}")
        if error is None:
            await ctx.respond_with_source(f"**Unknown error** with the id `{error_id.upper()}`.", ephemeral=True)
            return

        data = json.loads(error)
        messages = [
            f"<@{data['author']}> used `/{data['command']} at {datetime.fromtimestamp(data['timestamp'])}`"
        ]
        current = ""
        for line in data["traceback"].splitlines():
            if (len(current) + len(line)) > 2000:
                messages.append(f"```py\n{current}```")
                current = ""

            else:
                current += f"\n{line}"

        if len(current) > 0:
            messages.append(f"```py\n{current}```")

        for msg in messages:
            await ctx.respond(msg, ephemeral=True)
