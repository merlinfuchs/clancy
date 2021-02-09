import dc_interactions as dc
from xenon import rest
import string

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


class TransformModule(dc.Module):
    @dc.Module.command()
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

    @dc.Module.command()
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

    @dc.Module.command()
    async def unbottom(self, ctx, bottom):
        """
        Decode bottom to the original message 🥺
        """
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
                                      "Use `/bottom` to create bottom text.")
                    return

            raw += value.to_bytes(1, "big")

        await ctx.respond(f"The original message is:\n```{raw.decode()}```", ephemeral=True)
