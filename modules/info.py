from dbots.cmd import *
from dbots import rest


class InfoModule(Module):
    @Module.command()
    async def avatar(self, ctx, user: CommandOptionType.USER):
        """
        Get the avatar url for an user
        """
        resolved = ctx.resolved.users.get(user)
        if resolved is None:
            try:
                resolved = await ctx.bot.http.get_user(user)
            except rest.HTTPNotFound:
                await ctx.respond("I'm unable to find this user :(", ephemeral=True)

        await ctx.respond(f"**{resolved.name}**s **Avatar**\n{resolved.avatar_url}", ephemeral=True)

    # @dc.Module.command()
    async def user(self, ctx, user: CommandOptionType.USER):
        """
        Get information about a user
        """
        resolved = ctx.resolved.users.get(user)
        if resolved is None:
            try:
                resolved = await ctx.bot.http.get_user(user)
            except rest.HTTPNotFound:
                await ctx.respond("I'm unable to find this user :(", ephemeral=True)

        await ctx.respond()

    # @dc.Module.command()
    async def role(self, ctx, role: CommandOptionType.ROLE):
        """
        Get information about a role
        """
        print(ctx.resolved)

    # @dc.Module.command()
    async def channel(self):
        """
        Get information about a channel
        """

    # @dc.Module.command()
    async def server(self):
        """
        Get information about a server
        """
