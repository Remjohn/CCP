import asyncio
import random
from uuid import uuid4
from datetime import datetime, timedelta
from backend.config import get_settings
from supabase import create_client, Client

# Constants
PILLARS = ["fluid_integrator", "grounded_processor", "rhythmic_releaser", "intuitive_explorer"]

# Rich Journal Templates (>60 words)
JOURNAL_TEMPLATES = {
    "fluid_integrator": [
        "I feel like my energy is everywhere today. I started three different projects and finished none of them. It's that familiar sense of being scattered, like leaves in the wind. I want to be productive, but I just can't seem to find my center. I know I need structure, but I resist it. I'm feeling anxious about all the open loops in my life right now.",
        "My mind is racing a mile a minute. I have so many ideas but no container to hold them. I tried to sit down and focus, but my body just wanted to move. I feel overwhelmed by the sheer volume of possibilities. I need to find a way to channel this flow into something concrete before I burn out from the mental spinning.",
        "I missed my morning routine again. It feels like I'm constantly reacting to the world instead of creating my own day. The chaos is exciting in a way, but it leaves me feeling empty and tired by the evening. I'm craving a sense of grounding, but I don't know how to stop the momentum of my own distraction."
    ],
    "grounded_processor": [
        "I've been feeling incredibly stuck lately. It's like I'm rooted to the spot and can't take the first step. I analyze every option to death until I'm paralyzed. I know I'm capable, but I'm terrified of making the wrong move. I feel a heavy weight in my chest, a sense of rigid stagnation that I can't seem to shake off.",
        "My perfectionism is flaring up again. I spent hours tweaking a minor detail instead of shipping the work. I feel safe when I'm in control, but I know this control is an illusion that keeps me small. I need to learn how to move before I'm ready. I'm feeling guilty about my lack of progress despite working so hard.",
        "I'm holding onto old resentment. It's hard for me to let go and flow with the changes. I feel like a stone in a river, resisting the current. My body feels stiff and tense, especially in my shoulders. I know I need to soften, but it feels unsafe to let my guard down. I'm lonely in this fortress I've built."
    ],
    "rhythmic_releaser": [
        "I'm caught in a loop again. I keep doing the same things expecting different results. It's comfortable, but I feel a deep sense of boredom and emptiness. I'm avoiding the hard conversations by distracting myself with busy work. I need to break this rhythm, but the momentum of habit is so strong.",
        "I feel like I'm running on a hamster wheel. Lots of movement, but no destination. I'm tired of this repetitive cycle. I know there's more to life than this daily grind, but I'm afraid to step off the path. I'm feeling a low-grade depression, a sense of grayness that covers everything.",
        "I'm using my routine to hide from my feelings. If I keep moving, I don't have to feel the sadness underneath. But it's catching up to me. I feel heavy and sluggish, like I'm wading through molasses. I need to find a way to release this pent-up emotion without falling apart."
    ],
    "intuitive_explorer": [
        "I feel like I'm drifting without an anchor. One day I'm high on inspiration, the next I'm lost in the fog. I struggle to commit to anything because I'm afraid of missing out on something else. I'm feeling unmoored and disconnected from reality. I need something to hold onto.",
        "My intuition is loud, but I don't trust it enough to act. I'm floating through my days, waiting for a sign that never comes. I feel a sense of longing for a home I've never known. I'm inconsistent with my practices, and it makes me feel like a failure. I need to find my ground.",
        "I'm overwhelmed by the emotions of others. I absorb everything like a sponge until I don't know what's mine and what's theirs. I feel exhausted and drained. I need to establish better boundaries, but I'm afraid of losing connection. I'm seeking clarity in the mist."
    ]
}

NAMES = [
    ("Alice", "Smith"), ("Bob", "Jones"), ("Charlie", "Brown"), ("Diana", "Prince"),
    ("Evan", "Wright"), ("Fiona", "Gallagher"), ("George", "Michael"), ("Hannah", "Montana"),
    ("Ian", "Malcolm"), ("Julia", "Roberts"), ("Kevin", "Bacon"), ("Laura", "Croft"),
    ("Mike", "Ross"), ("Nina", "Simone"), ("Oscar", "Wilde"), ("Paula", "Abdul"),
    ("Quinn", "Fabray"), ("Rachel", "Green"), ("Steve", "Jobs"), ("Tina", "Fey"),
    ("Ursula", "Buffay"), ("Victor", "Hugo"), ("Wendy", "Darling"), ("Xander", "Cage")
]

async def seed_users():
    settings = get_settings()
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    
    print("🌱 Seeding 24 Users with Rich Data...")
    
    # Clean up existing data first (Optional, but good for "better data")
    try:
        print("   Cleaning old data...")
        supabase.table("daily_journals").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        supabase.table("profiles").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    except Exception as e:
        print(f"   Warning: Could not clear data (RLS might prevent it): {e}")

    users = []
    journals = []
    
    for i in range(24):
        first, last = NAMES[i]
        user_id = str(uuid4())
        pillar = random.choice(PILLARS)
        capacity = random.randint(20, 90)
        
        # Create Profile
        user = {
            "id": user_id,
            "first_name": first,
            "last_name": last,
            "capacity_score": capacity,
            "identity_pillar": pillar,
            "telegram_chat_id": random.randint(100000, 999999) + i
        }
        users.append(user)
        
        # Create 1-2 Rich Journals per user
        for _ in range(random.randint(1, 2)):
            template = random.choice(JOURNAL_TEMPLATES[pillar])
            
            # Determine sentiment based on pillar/text (simplified)
            if "anxious" in template or "overwhelmed" in template:
                sentiment = -0.7
            elif "stuck" in template or "paralyzed" in template:
                sentiment = -0.6
            elif "boredom" in template or "loop" in template:
                sentiment = -0.4
            elif "drifting" in template or "lost" in template:
                sentiment = -0.5
            else:
                sentiment = -0.2 # Default to slightly negative for these "problem" journals
                
            journal = {
                "user_id": user_id,
                "transcript": template,
                "sentiment_score": sentiment,
                "created_at": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat()
            }
            journals.append(journal)

    try:
        print("   Inserting Profiles...")
        supabase.table("profiles").insert(users).execute()
        
        print("   Inserting Journals...")
        supabase.table("daily_journals").insert(journals).execute()
        
        print(f"✅ Successfully seeded {len(users)} users and {len(journals)} rich journals!")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")

if __name__ == "__main__":
    asyncio.run(seed_users())
