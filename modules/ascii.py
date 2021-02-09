import dc_interactions as dc

from util import *


APPEND_COMMANDS = [
    ("flipall", "┻━┻︵ \(°□°)/ ︵ ┻━┻"),
    ("rageflip", "(ノಠ益ಠ)ノ彡┻━┻"),
    ("bearflip", "ʕノ•ᴥ•ʔノ ︵ ┻━┻"),
    ("jakeflip", "(┛❍ᴥ❍﻿)┛彡┻━┻"),
    ("flipbattle", "(╯°□°)╯︵ ┻━┻ ︵ ╯(°□° ╯)"),
    ("magicflip", "(/¯◡ ‿ ◡)/¯ ~ ┻━┻"),
    ("flipdude", "(╯°Д°）╯︵ /(.□ . \)"),
    ("herculesflip", "(/ .□.)\ ︵╰(゜Д゜)╯︵ /(.□. \)"),
    ("happyflip", "┻━┻ ︵ ლ(⌒-⌒ლ)"),
    ("fucktable", "(┛◉Д◉) ┛彡┻━┻"),
    ("fixtable", "┬──┬ ¯\_(ツ)"),

    ("smirk", "¬‿¬"),
    ("creapy", "(◕‿◕)"),
    ("disapprove", "ಠ_ಠ"),
    ("lenny", "( ˘ ͜ʖ ˘)"),
    ("cool", "(⌐■_■)"),
    ("smug", "⚈ ̫ ⚈"),
    ("fight", "(ง ͠° ͟ل͜ ͡°)ง"),
    ("dead", "(✖╭╮✖)"),
    ("glomp", "(づ￣ ³￣)づ"),
    ("bearhug", "ʕっ• ᴥ • ʔっ")
]


class AsciiModule(dc.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def make_callable(_value):
            async def cmd_func(ctx, message=""):
                await send_webhook_response(ctx, f"{message} {_value}")

            return cmd_func

        for name, value in APPEND_COMMANDS:
            self.commands.append(dc.Command(
                name=name,
                description=f"Append {value} to your message.",
                callable=make_callable(value),
                options=[dc.CommandOption(
                    type=dc.CommandOptionType.STRING,
                    name="message",
                    description="Your message",
                    required=False
                )]
            ))
