from dbots.cmd import *
from dbots import rest

from util import *


class UtilsModule(Module):
    @Module.command()
    async def nopings(self, ctx, message):
        """
        Send the message without having to worry about pings
        """
        await send_webhook_response(ctx, message)

    @Module.command()
    async def embed(self, ctx, title, url, description):
        """
        Create a simple embed message
        """
        try:
            await send_webhook_response(ctx, embeds=[{
                "title": title,
                "url": url,
                "description": description
            }])
        except rest.HTTPBadRequest:
            await ctx.respond("Something went wrong :(\n"
                              "Did you use a valid url?", ephemeral=True)

    @Module.command(
        extends=dict(
            expression="The expression to evaluate (e.g. 1+1)"
        )
    )
    async def calculate(self, ctx, expression):
        """
        Evaluate a math expression
        """
        async with ctx.bot.session.post("http://api.mathjs.org/v4/", json={"expr": expression}) as resp:
            data = await resp.json()

        if data["error"] is not None:
            await ctx.respond(data["error"], ephemeral=True)
            return

        await send_webhook_response(ctx, f"`{expression} = {data['result']}`")

    # @Module.command(
    #     extends=dict(
    #         message_url="The URL or ID of the message to quote",
    #         text="Your response text"
    #     )
    # )
    async def quote(self, message_url: str.strip, text):
        """
        Use this to quote message from other channels
        """
