# Service Setup & Credentials Guide

This guide explains how to obtain the necessary credentials for the `.env` file and clarifies the pricing models for each service.

## 1. Telegram Bot (Free)
**Cost:** 100% Free.
**Credentials:** `TELEGRAM_BOT_TOKEN`, `TELEGRAM_SECRET_TOKEN`

### How to Setup:
1.  Open Telegram and search for **@BotFather**.
2.  Send the command `/newbot`.
3.  Follow the prompts to name your bot.
4.  **Bot Token:** BotFather will give you a token (e.g., `123456:ABC-DEF...`). Paste this as `TELEGRAM_BOT_TOKEN`.
5.  **Secret Token:** This is a random string you create yourself (e.g., `my_super_secret_token_123`) to verify incoming webhooks. You set this in your `.env` and later tell Telegram about it when setting the webhook URL.

## 2. Supabase (Free Tier Available)
**Cost:** Generous Free Tier (500MB database, 50k monthly active users). Paid plans start at $25/mo.
**Credentials:** `SUPABASE_URL`, `SUPABASE_KEY`

### How to Setup:
1.  Go to [supabase.com](https://supabase.com) and sign up.
2.  Create a "New Project".
3.  Once the project is created, go to **Project Settings > API**.
4.  **URL:** Copy the "Project URL".
5.  **Key:** Copy the "anon" / "public" key. (Do not use the `service_role` key in the client app, but it's okay for the backend if kept secure).

## 3. Groq (Free Beta / Paid)
**Cost:** Currently offers a **Free Beta** with generous rate limits. Will likely become a paid service in the future, but is very cheap compared to GPT-4.
**Credentials:** `GROQ_API_KEY`

### How to Setup:
1.  Go to [console.groq.com](https://console.groq.com).
2.  Sign up/Login.
3.  Go to **API Keys** and click "Create API Key".
4.  Copy the key.

## 4. Redis (Free / Open Source)
**Cost:** Free to run locally. Paid if you use a managed cloud provider (like Upstash or Redis Cloud).
**Credentials:** `REDIS_URL`

### How to Setup (Local - Recommended for Dev):
The `REDIS_URL=redis://localhost:6379/0` assumes you are running Redis on your machine.

**Option A: Docker (Easiest)**
If you have Docker Desktop installed:
```bash
docker run --name cbcs-redis -p 6379:6379 -d redis
```

**Option B: WSL2 (Windows Subsystem for Linux)**
1.  Open your Ubuntu/Debian terminal in WSL.
2.  Run: `sudo apt-get install redis-server`
3.  Start it: `sudo service redis-server start`

**Option C: Memurai (Native Windows)**
1.  Download [Memurai Developer Edition](https://www.memurai.com/get-memurai) (Free for dev).
2.  Install and run. It acts as a Redis-compatible server.

### How to Setup (Cloud - Optional):
If you cannot run it locally, use [Upstash](https://upstash.com/) (Serverless Redis).
1.  Sign up for the Free Tier.
2.  Create a database.
3.  Copy the connection string (replace `redis://localhost...` with the Upstash URL).
