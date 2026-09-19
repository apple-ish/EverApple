# 🍎 EverApple

A Discord selfbot that keeps your account online 24/7 — controlled entirely from Discord chat itself.

## Features

- **`a.on`** — set status to **Online** (persisted forever, auto-restored on reconnect)
- **`a.off`** — set status to **Invisible** (appears offline)
- **`a.idle`** — set status to **Idle**
- **`a.dnd`** — set status to **Do Not Disturb**
- **`a.status`** — check current status
- **Stealth mode** — every command message is auto-deleted instantly
- **Owner lock** — only your account can trigger commands (set `OWNER_ID` secret)
- **Keepalive** — re-asserts your presence every 60s so Discord can't silently drop it
- **GitHub Actions runner** — runs on GitHub's servers, no VPS or local machine needed

## Setup (fork-and-run)

1. **Fork this repo** (or use it directly if you own it)
2. Go to **Settings → Secrets and variables → Actions**
3. Add two secrets:
   - `DISCORD_TOKEN` — your Discord user token ([how to get it](https://www.zenrows.com/blog/how-to-get-discord-token))
   - `OWNER_ID` — your Discord user ID (enable Developer Mode → right-click your name → Copy ID)
4. Go to **Actions** tab → click **"I understand my workflows, go ahead and enable them"** if prompted
5. Select **EverApple Keepalive** → **Run workflow**
6. Done — the selfbot logs in and keeps your account online 24/7

## Status Persistence

Once you set a status with `a.on`, `a.off`, `a.idle`, or `a.dnd`, it stays until you change it with another command — even across:
- GitHub Actions runner restarts
- Discord reconnects
- Workflow re-runs every 6 hours

The status persists because the selfbot re-asserts it every 60 seconds while running.

## Requirements

- Python 3.11+
- `discord.py-self` (installed automatically from `requirements.txt`)

## ⚠️ Disclaimer

Selfbots violate Discord's Terms of Service. Use at your own risk — your account may be suspended or banned. This project is for educational purposes only.

## License

MIT
