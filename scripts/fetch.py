# -*- coding: utf-8 -*-
"""
Генерирует JSON-файлы c rising-топами Google Trends и кладёт их в /public.
Запускать через GitHub Actions → schedule (каждый час).
"""
import json, os, datetime as dt
from pytrends.request import TrendReq

KW = ["toy", "plush", "cup"]        # ключевые слова меняйте здесь
GEO = "RU"                          # страна
OUT = "public/rising"               # куда класть json

os.makedirs(OUT, exist_ok=True)
pytrends = TrendReq(hl="ru-RU", tz=180)

for kw in KW:
    pytrends.build_payload([kw], geo=GEO, timeframe="now 7-d")

    try:                                    # ▸ добавляем try/except
        df = pytrends.related_topics()[kw]["rising"]
        records = df.to_dict(orient="records")[:20] if isinstance(df, pd.DataFrame) else []
    except (KeyError, IndexError, TypeError):
        records = []                        # если Google вернул пусто

    with open(f"{OUT}/{kw}.json", "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


# метка времени обновления
with open(f"{OUT}/timestamp.txt", "w") as f:
    f.write(dt.datetime.utcnow().isoformat()+"Z")
