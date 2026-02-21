import os
import time
import threading
import requests
import numpy as np
from datetime import datetime
from flask import Flask, jsonify, render_template
from sklearn.linear_model import LinearRegression
from collections import deque

app = Flask(__name__)

# ─────────────────────────────────────────────
# CONFIGURAÇÕES — ajuste conforme necessário
# ─────────────────────────────────────────────
API_KEY  = os.environ.get("OWM_API_KEY", "SUA_APIKEY")
CITY     = os.environ.get("OWM_CITY", "Rio de Janeiro")
INTERVAL = 30          # segundos entre coletas reais
MAX_HISTORY = 30       # máximo de pontos na janela deslizante
FORECAST_STEPS = 6     # quantos passos à frente prever


# ─────────────────────────────────────────────
# Armazenamento em memória (thread-safe)
# ─────────────────────────────────────────────
lock = threading.Lock()

history = {
    "timestamps":   deque(maxlen=MAX_HISTORY),
    "temperature":  deque(maxlen=MAX_HISTORY),
    "humidity":     deque(maxlen=MAX_HISTORY),
    "pressure":     deque(maxlen=MAX_HISTORY),
    "wind_speed":   deque(maxlen=MAX_HISTORY),
}

forecast = {
    "timestamps":  [],
    "temperature": [],
    "humidity":    [],
}

last_reading = {}
model_status = {"trained": False, "points": 0}


# ─────────────────────────────────────────────
# Coleta de dados — OpenWeatherMap
# ─────────────────────────────────────────────
def fetch_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": CITY, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    d = r.json()
    return {
        "timestamp":   datetime.utcnow().isoformat(),
        "temperature": round(d["main"]["temp"], 2),
        "humidity":    d["main"]["humidity"],
        "pressure":    d["main"]["pressure"],
        "wind_speed":  round(d["wind"]["speed"], 2),
        "description": d["weather"][0]["description"].capitalize(),
        "icon":        d["weather"][0]["icon"],
        "city":        d["name"],
    }


# ─────────────────────────────────────────────
# Regressão Linear — Sensor Virtual
# ─────────────────────────────────────────────
def train_and_forecast():
    with lock:
        n = len(history["timestamps"])
        if n < 3:
            model_status["trained"] = False
            model_status["points"] = n
            return

        X = np.arange(n).reshape(-1, 1)
        temps = np.array(history["temperature"])
        hums  = np.array(history["humidity"])

        model_temp = LinearRegression().fit(X, temps)
        model_hum  = LinearRegression().fit(X, hums)

        # Gera previsões para os próximos FORECAST_STEPS passos
        future_X = np.arange(n, n + FORECAST_STEPS).reshape(-1, 1)
        pred_temps = model_temp.predict(future_X)
        pred_hums  = model_hum.predict(future_X)

        # Timestamps futuros (estimados com base no intervalo)
        last_ts = datetime.fromisoformat(history["timestamps"][-1])
        future_ts = [
            (last_ts.timestamp() + INTERVAL * (i + 1)) * 1000  # ms para JS
            for i in range(FORECAST_STEPS)
        ]

        forecast["timestamps"]  = future_ts
        forecast["temperature"] = [round(v, 2) for v in pred_temps]
        forecast["humidity"]    = [round(v, 2) for v in np.clip(pred_hums, 0, 100)]

        model_status["trained"] = True
        model_status["points"]  = n


# ─────────────────────────────────────────────
# Thread de coleta contínua
# ─────────────────────────────────────────────
def collector_loop():
    global last_reading
    while True:
        try:
            reading = fetch_weather()
            with lock:
                history["timestamps"].append(reading["timestamp"])
                history["temperature"].append(reading["temperature"])
                history["humidity"].append(reading["humidity"])
                history["pressure"].append(reading["pressure"])
                history["wind_speed"].append(reading["wind_speed"])
                last_reading = reading
            train_and_forecast()
            print(f"[{reading['timestamp']}] {reading['temperature']}°C | {reading['humidity']}% | OK")
        except Exception as e:
            print(f"[ERRO] {e}")
        time.sleep(INTERVAL)


# ─────────────────────────────────────────────
# Rotas Flask
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", city=CITY, interval=INTERVAL)


@app.route("/api/data")
def api_data():
    with lock:
        hist_ts = [
            datetime.fromisoformat(ts).timestamp() * 1000
            for ts in history["timestamps"]
        ]
        return jsonify({
            "history": {
                "timestamps":  hist_ts,
                "temperature": list(history["temperature"]),
                "humidity":    list(history["humidity"]),
                "pressure":    list(history["pressure"]),
                "wind_speed":  list(history["wind_speed"]),
            },
            "forecast":    forecast,
            "last":        last_reading,
            "model":       model_status,
        })


# ─────────────────────────────────────────────
# Inicialização
# ─────────────────────────────────────────────
if __name__ == "__main__":
    t = threading.Thread(target=collector_loop, daemon=True)
    t.start()
    app.run(debug=True, use_reloader=False, port=5000)
