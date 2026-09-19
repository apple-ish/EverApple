import os
import sys
import logging
import asyncio

import discord
from discord.ext import commands, tasks

# ─────────────────────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────────────────────
TOKEN = os.environ.get("DISCORD_TOKEN")
PREFIX = "a."
OWNER_ID = int(os.environ.get("OWNER_ID", "0") or 0) or None

STATUS_MAP = {
    "on":    (discord.Status.online,          "✅ Online"),
    "off":   (discord.Status.invisible,       "👻 Invisible"),
    "idle":  (discord.Status.idle,            "🌙 Idle"),
    "dnd":   (discord.Status.do_not_disturb,  "⛔ Do Not Disturb"),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("everapple")

if not TOKEN:
    log.critical("DISCORD_TOKEN not set — exiting.")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.presences = True

client = commands.Bot(command_prefix=PREFIX, self_bot=True, intents=intents)
client._current_status = None  # persists across reconnects


# ─────────────────────────────────────────────────────────────
#  EVENTS
# ─────────────────────────────────────────────────────────────
@client.event
async def on_ready():
    log.info("Logged in as %s (%s)", client.user, client.user.id)
    if client._current_status:
        await client.change_presence(status=client._current_status)
        log.info("Restored saved status after reconnect.")
    if not keep_alive_loop.is_running():
        keep_alive_loop.start()


@client.event
async def on_command(ctx):
    """Stealth mode: nuke the command message instantly."""
    try:
        await ctx.message.delete()
    except discord.HTTPException:
        pass


# ─────────────────────────────────────────────────────────────
#  KEEPALIVE — re-asserts presence every 60s
# ─────────────────────────────────────────────────────────────
@tasks.loop(seconds=60)
async def keep_alive_loop():
    if client._current_status and not client.is_closed():
        try:
            await client.change_presence(status=client._current_status)
        except Exception as e:
            log.warning("Keepalive ping failed: %s", e)


# ─────────────────────────────────────────────────────────────
#  COMMANDS — owner-locked and self-deleting
# ─────────────────────────────────────────────────────────────
def owner_only():
    async def predicate(ctx):
        if OWNER_ID and ctx.author.id != OWNER_ID:
            return False
        return True
    return commands.check(predicate)


def make_status_command(name):
    status, label = STATUS_MAP[name]

    @client.command(name=name)
    @owner_only()
    async def cmd(ctx):
        client._current_status = status
        await client.change_presence(status=status)
        log.info("Status set to %s by %s", label, ctx.author)
        await ctx.send(f"**{label}**", delete_after=2)
    return cmd


for name in STATUS_MAP:
    make_status_command(name)


@client.command(name="status")
@owner_only()
async def _status(ctx):
    label = next(
        (v[1] for v in STATUS_MAP.values() if v[0] == client._current_status),
        "Unknown",
    )
    await ctx.send(f"📊 Current: **{label}**", delete_after=5)


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────
async def main():
    async with client:
        await client.start(TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Shutting down gracefully.")