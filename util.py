from xenon import rest, Webhook


__all__ = (
    "send_webhook_response",
    "MissingWebhookPermissions"
)


class MissingWebhookPermissions(Exception):
    pass


async def send_webhook_response(ctx, content=None, username=None, avatar_url=None, **kwargs):
    await ctx.ack()
    cached = await ctx.bot.redis.get(f"webhooks:{ctx.channel_id}")
    if cached:
        id, token = cached.decode().split(" ")
        webhook = Webhook({"id": id, "token": token})

    else:
        try:
            existing = await ctx.bot.http.get_channel_webhooks(ctx.channel_id)
        except rest.HTTPForbidden:
            raise MissingWebhookPermissions

        if len(existing) != 0:
            webhook = existing[0]

        else:
            try:
                webhook = await ctx.bot.http.create_webhook(ctx.channel_id, name="Clancy")
            except:
                raise MissingWebhookPermissions

        await ctx.bot.redis.set(f"webhooks:{ctx.channel_id}", f"{webhook.id} {webhook.token}")

    username = username or ctx.author.name
    avatar_url = avatar_url or str(ctx.author.avatar_url) if ctx.author.avatar_url else None
    await ctx.bot.http.execute_webhook(
        webhook,
        content=content,
        username=username,
        avatar_url=avatar_url,
        allowed_mentions={"parse": []},
        **kwargs
    )
