# Self-Hosting Guide: Redis & Supabase on Dokploy

This guide walks you through deploying Redis and Supabase on your VPS using Dokploy.

## Prerequisites
- **Dokploy Installed:** You can access your Dokploy dashboard (usually `http://<your-vps-ip>:3000` or `https://dokploy.conscioustrack.my` if configured).
- **Domain Configured:** `conscioustrack.my` pointing to your VPS IP.

---

## Part 1: Deploy Redis

1.  **Login to Dokploy**.
2.  Go to **Projects** -> Create a new project (e.g., `cbcs-infra`).
3.  Click **Create Service** -> **Database**.
4.  Select **Redis**.
5.  **Configuration:**
    - **Name:** `cbcs-redis`
    - **Password:** Generate a strong password (e.g., `RedisStrongPass123!`).
    - **External Port:** Set this to `6379` (or another unused port like `30001`) to allow your local machine to connect.
6.  **Deploy:** Click Create/Deploy.
7.  **Get Connection String:**
    - Once deployed, your `REDIS_URL` for the `.env` file will be:
    - `redis://:<password>@<your-vps-ip>:<external-port>/0`
    - *Example:* `redis://:RedisStrongPass123!@123.45.67.89:6379/0`

---

## Part 2: Deploy Supabase

Supabase is a complex stack (Postgres, GoTrue, PostgREST, Realtime, Storage, etc.). Dokploy makes this easier with a template.

### Step 1: Generate Secrets
You need to generate secure keys *before* deploying.
1.  **JWT Secret:** Generate a random 32-char string.
    - *Command:* `openssl rand -hex 32`
2.  **Anon Key & Service Role Key:**
    - Go to [jwt.io](https://jwt.io).
    - **Algorithm:** HS256.
    - **Secret:** Paste your JWT Secret in the "VERIFY SIGNATURE" box.
    - **Payload (Anon):**
      ```json
      {
        "role": "anon",
        "iss": "supabase",
        "iat": 1700000000,
        "exp": 2000000000
      }
      ```
    - Copy the generated "Encoded" token. This is your `ANON_KEY`.
    - **Payload (Service Role):**
      ```json
      {
        "role": "service_role",
        "iss": "supabase",
        "iat": 1700000000,
        "exp": 2000000000
      }
      ```
    - Copy the generated "Encoded" token. This is your `SERVICE_ROLE_KEY`.
    b58aed4f9f183c34816cc27a7598fcd6

### Step 2: Deploy via Template
1.  In Dokploy, go to your Project.
2.  Click **Create Service** -> **Template** (or "Open Source Templates").
3.  Search for **Supabase**.
4.  **Configuration:**
    - You will see a list of Environment Variables. **You MUST fill these in:**
    - `POSTGRES_PASSWORD`: Generate a strong DB password.
    - `JWT_SECRET`: The 32-char string you generated.
    - `ANON_KEY`: The Anon JWT you generated.
    - `SERVICE_ROLE_KEY`: The Service Role JWT you generated.
    - `DASHBOARD_USERNAME`: `admin`
    - `DASHBOARD_PASSWORD`: Generate a password for the Studio UI.
    - `API_EXTERNAL_URL`: `https://supabase.conscioustrack.my` (or similar subdomain).
    - `SUPABASE_PUBLIC_URL`: `https://supabase.conscioustrack.my`
5.  **Deploy:** Click Deploy.

### Step 3: Configure Domain
1.  In Dokploy, go to the **Supabase** service (it might create multiple, look for the main entry or "Kong" / "API Gateway").
2.  Go to **Domains**.
3.  Add Domain: `supabase.conscioustrack.my` (Ensure you have an A record for `supabase` pointing to your VPS IP in your DNS provider).
4.  Enable **HTTPS/SSL** (Let's Encrypt).

### Step 4: Get Credentials
Once deployed and accessible at `https://supabase.conscioustrack.my`:
- **SUPABASE_URL:** `https://supabase.conscioustrack.my`
- **SUPABASE_KEY:** Use the `ANON_KEY` you generated.

---

## Part 3: Update Local .env

Update your local `d:\Work\CBCS\.env` file with these new values:

```ini
# ... other keys ...
SUPABASE_URL=https://supabase.conscioustrack.my
SUPABASE_KEY=<your-anon-key>
REDIS_URL=redis://:<redis-password>@<vps-ip>:<redis-port>/0
```
