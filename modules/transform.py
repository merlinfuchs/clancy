import string
import re

from dbots.cmd import *
from dbots import rest

from util import *

NUMBERS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
EXTRA_EMOJIS = {
    "#": ":hash:",
    "*": ":asterisk:",
    "!": ":exclamation:",
    "?": ":question:"
}

BOTTOM_VALUES = {
    "🫂": 200,
    "💖": 50,
    "✨": 10,
    "🥺": 5,
    ",": 1,
    "❤️": 0
}
BOTTOM_SEPARATOR = '👉👈'


class TransformModule(Module):
    @Module.command()
    async def big(self, ctx, message: str.lower):
        """
        Convert text to emojis
        """
        result = ""
        for char in message:
            if char in string.ascii_letters:
                result += f":regional_indicator_{char}:"

            elif char in string.digits:
                result += f":{NUMBERS[int(char)]}:"

            elif char in EXTRA_EMOJIS:
                result += EXTRA_EMOJIS[char]

            else:
                result += char

        await send_webhook_response(ctx, result)

    @Module.command()
    async def bottom(self, ctx, message):
        """
        Convert your message to bottom 🥺
        """
        raw = bytearray()
        for char in message.encode():
            while char != 0:
                for target, value in BOTTOM_VALUES.items():
                    if char >= value:
                        char -= value
                        raw += target.encode()
                        break

            raw += BOTTOM_SEPARATOR.encode()

        try:
            await send_webhook_response(ctx, raw.decode())
        except rest.HTTPBadRequest:
            await ctx.respond("Your text is too long to be converted to bottom 🥺", ephemeral=True)

    @Module.command(extends=dict(
        bottom="The bottom text or id of the message to decode"
    ))
    async def unbottom(self, ctx, bottom):
        """
        Decode bottom to the original message 🥺
        """
        if re.match(r"\d", bottom):
            try:
                msg = await ctx.bot.http.get_channel_message(ctx.channel_id, bottom)
            except rest.HTTPNotFound:
                await ctx.respond("Can't find that message in this channel :(", ephemeral=True)
            else:
                bottom = msg.content

        raw = bytearray()
        text = bottom.strip()
        if text.endswith(BOTTOM_SEPARATOR):
            text = text[:-len(BOTTOM_SEPARATOR)]

        for char in text.split(BOTTOM_SEPARATOR):
            value = 0
            for emoji in char:
                try:
                    value += BOTTOM_VALUES[emoji]
                except KeyError:
                    await ctx.respond("That text is not valid bottom :pleading_face:\n"
                                      "Use `/bottom` to create bottom text.", ephemeral=True)
                    return

            raw += value.to_bytes(1, "big")

        await ctx.respond(f"The original message is:\n```{raw.decode()}```", ephemeral=True)

    @Module.command()
    async def reverse(self, ctx, message):
        """
        Reverse your message
        """
        await send_webhook_response(ctx, message[::-1])
