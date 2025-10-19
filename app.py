from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, render_template
import os

app = Flask(__name__)

# Zona horaria del servidor (puedes cambiarla con APP_TIMEZONE)
DEFAULT_TZ = os.getenv("APP_TIMEZONE", "America/Santiago")

def compute_target(tz_name: str):
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    year = now.year
    christmas = datetime(year, 12, 25, 0, 0, 0, tzinfo=tz)
    if now >= christmas:
        christmas = datetime(year + 1, 12, 25, 0, 0, 0, tzinfo=tz)
    return now, christmas

@app.route("/")
def index():
    tz_name = DEFAULT_TZ
    try:
        ZoneInfo(tz_name)
    except Exception:
        tz_name = "UTC"

    now, target = compute_target(tz_name)
    delta = target - now
    total_seconds = int(delta.total_seconds())
    days = max(0, total_seconds // 86400)
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return render_template(
        "index.html",
        tz_name=tz_name,
        now_iso=now.isoformat(),
        target_iso=target.isoformat(),
        year=target.year,
        today_str=now.strftime("%Y-%m-%d"),
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))