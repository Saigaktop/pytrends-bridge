# -*- coding: utf-8 -*-
"""
Генерирует JSON-файлы c rising-топами Google Trends и кладёт их в /public.
Запускать через GitHub Actions → schedule (каждый час).
"""

KW = [
    # ───── Accessories ─────
    "crossbody bag", "phone charm", "tote bag", "bucket hat",
    "mesh beach bag", "minimalist wallet", "belt bag",
    "travel organizer", "silk hair scrunchie", "earphone case",
    "non-slip hair clip", "puffy headband",

    # ───── Toys ─────
    "fidget toy", "sensory pop it", "building bricks set",
    "interactive plush", "mini claw machine", "water bead blaster",
    "lcd drawing tablet", "magnetic cubes", "rc stunt car",
    "mystery blind box", "collectible vinyl figure",

    # ───── Jewelry ─────
    "layered necklace", "initial pendant", "tennis bracelet",
    "ear cuff", "stackable ring", "pearl choker", "birthstone charm",
    "signet ring", "mismatched earrings", "beaded anklet",
    "hand-chain bracelet",

    # ───── Dog supplies ─────
    "no pull harness", "slow feeder bowl", "puzzle toy for dogs",
    "treat dispensing ball", "dog cooling mat", "hands free leash",
    "personalised dog tag", "dog snuffle mat", "retractable leash",
    "chew proof bed",

    # ───── Cat supplies ─────
    "interactive cat toy", "catnip kicker", "cat window perch",
    "automatic litter box", "cat fountain", "wall climbing shelf",
    "laser pointer chaser", "self grooming brush", "cat kicker fish",
    "foldable cat tunnel", "scratcher lounger",

    # ───── Sport ─────
    "pickleball paddle", "padel racket", "disc golf set",
    "training cones", "sports recovery ball", "agility ladder",
    "portable soccer goal", "foam roller", "overgrip tape",
    "inflatable kayak", "ski wax kit",

    # ───── Fitness ─────
    "resistance band set", "adjustable dumbbell", "ankle weight",
    "pilates ring", "hip thrust pad", "weighted jump rope",
    "yoga wheel", "massage gun", "smart water bottle",
    "grip strength trainer", "compact treadmill"
]

GEOS = ["US", "DE", "FR", "GB", "JP", "CN", "IN", "ES"]                          # страна
OUT = "public/rising"               # куда класть json

import os, json, time, random, datetime as dt
import pandas as pd
from itertools import product
from pytrends.request import TrendReq
pytrends = TrendReq(
    hl="en-US", tz=0,
    timeout=(10,25),              # (connect, read)  – по-тише
    retries=2, backoff_factor=0.4 # авто-повтор при 429
)

# ─── вспомогалка: безопасно тащим rising-топ ───────────────────
def get_rising(keyword:str, geo:str):
    try:
        pytrends.build_payload([keyword], geo=geo, timeframe="now 7-d")
        df = pytrends.related_topics()[keyword]["rising"]
        if isinstance(df, pd.DataFrame):
            return df.to_dict(orient="records")[:20]
    except Exception:
        pass            # любое падение → вернём пусто
    return []

# ─── основной цикл с «тормозом» ────────────────────────────────
os.makedirs(OUT, exist_ok=True)
for kw, geo in product(KW, GEOS):
    records = get_rising(kw, geo)

    fname = f"{kw.replace(' ','_')}_{geo.lower()}.json"
    with open(f"{OUT}/{fname}", "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    # ▸ пауза 1-2 сек + лёгкий джиттер
    time.sleep(1 + random.random())

# ─── метка времени ─────────────────────────────────────────────
with open(f"{OUT}/timestamp.txt", "w") as f:
    f.write(dt.datetime.utcnow().isoformat()+"Z")
