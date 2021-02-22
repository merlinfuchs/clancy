import random

from dbots.cmd import *

from util import *
from .transform import NUMBERS


class FunModule(Module):
    @Module.command(extends=dict(
        count="The count of dice to roll",
        private="Whether the result should be shown to everyone"
    ))
    async def roll(self, ctx, count: int = 1, public: bool = True):
        """
        Role one or multiple dice
        """
        count = min(max(count, 1), 50)

        if count > 1:
            result = {}
            for i in range(count):
                value = random.randint(1, 6)
                if value in result:
                    result[value] += 1

                else:
                    result[value] = 1

            total = sum([k * v for k, v in result.items()])
            result_text = "\n".join([
                f"**{NUMBERS[r].title()}** was rolled **{result[r]}** time(s)."
                for r in sorted(result)
            ])
            text = f":game_die: **I rolled {count} dice**:\n" \
                   f"{result_text}\n" \
                   f"The total is: **{total}**."

        else:
            value = random.randrange(1, 6)
            text = f":game_die: I rolled a die and the result is **{NUMBERS[value].title()}**."

        if public:
            await send_webhook_response(ctx, text)

        else:
            await ctx.respond(text, ephemeral=True)

    @Module.command(extends=dict(
        public="Whether the result should be shown to everyone"
    ))
    async def choose(self, ctx, option_a, option_b, option_c=None, option_d=None, option_e=None, public: bool = True):
        """
        Randomly choose between two or more options
        """
        options = list(filter(lambda o: o is not None, [option_a, option_b, option_c, option_d, option_e]))
        result = random.choice(options)
        option_text = " and ".join(", ".join([f"**{o}**" for o in options]).rsplit(", ", 1))
        text = f"I chose between {option_text} and my choice is: **{result}**."
        if public:
            await send_webhook_response(ctx, text)

        else:
            await ctx.respond(text, ephemeral=True)

    @Module.command(extends=dict(
        public="Whether the result should be shown to everyone"
    ))
    async def coin(self, ctx, public: bool = True):
        """
        Flip a coin
        """
        result = random.choice(["Heads", "Tails"])
        text = f":coin: I flipped a coin and it landed on: **{result}**!"
        if public:
            await send_webhook_response(ctx, text)

        else:
            await ctx.respond(text, ephemeral=True)

    @Module.command(extends=dict(
        min="The minimum number",
        max="The maximum number",
        public="Whether the result should be shown to everyone"
    ))
    async def random(self, ctx, min: int = 0, max: int = 100, public: bool = True):
        """
        Get a random number between min and max
        """
        result = random.randint(min, max)
        text = f"I chose a number between **{min}** and **{max}** and my choice is: **{result}**."
        if public:
            await send_webhook_response(ctx, text)

        else:
            await ctx.respond(text, ephemeral=True)

    @Module.command()
    async def monox(self, ctx, message=""):
        """
        monox
        """
        await send_webhook_response(ctx, f"{message} <a:monoxpat:797866087000702986>")
