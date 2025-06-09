# Lightweight bridge  (≈40 строк)
from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)
pytrends = TrendReq(hl="ru-RU", tz=180)

def rising_topics(keyword, geo):
    pytrends.build_payload([keyword], geo=geo, timeframe="now 7-d")
    data = pytrends.related_topics()[keyword]["rising"]
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient="records")[:20]   # топ-20
    return []

@app.route("/rising")
def rising():
    kw = request.args.get("q")
    geo = request.args.get("geo", "RU")
    if not kw:
        return jsonify({"error": "param q required"}), 400
    try:
        return jsonify(rising_topics(kw, geo))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def health():
    return "pytrends-bridge OK"
