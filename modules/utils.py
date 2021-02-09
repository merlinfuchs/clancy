import dc_interactions as dc

from util import *


class UtilsModule(dc.Module):
    @dc.Module.command()
    async def nopings(self, ctx, message):
        """
        Send the message without having to worry about pings
        """
        await send_webhook_response(ctx, message)

    @dc.Module.command()
    async def embed(self, ctx, title, url, description):
        """
        Create a simple embed message
        """
        await send_webhook_response(ctx, embeds=[{
            "title": title,
            "url": url,
            "description": description
        }])

    @dc.Module.command(
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

    # @dc.Module.command(
    #     extends=dict(
    #         message_url="The URL or ID of the message to quote",
    #         text="Your response text"
    #     )
    # )
    async def quote(self, message_url: str.strip, text):
        """
        Use this to quote message from other channels
        """
