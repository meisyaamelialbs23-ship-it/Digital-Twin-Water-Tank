Inisialisasi Kode — Digital Twin Tangki Air

digital-twin-tangki-air/
├── backend/ (app.py, init_db.py, requirements.txt)
├── frontend/ (index.html, style.css, app.js)
├── simulator/ (sensor_simulator.py)
├── database/ (schema.sql, seed.sql)
├── docs/
├── .gitignore
└── README.md

````markdown
# 💧 Digital Twin Tangki Air

Perancangan Digital Twin Tangki Air untuk Memantau Ketinggian dan Kondisi Air Secara Real-Time.
Boilerplate Sprint 1 — Product Release 1 (Scrum, tim 3 orang).

## Struktur Folder
```
digital-twin-tangki-air/
├── backend/        # REST API (Flask) + init_db.py
├── frontend/       # Dashboard web (HTML/JS/CSS + Chart.js)
├── simulator/      # Simulator sensor (data dummy)
├── database/       # schema.sql, seed.sql (SQLite: tangki.db dibuat otomatis)
├── docs/           # Charter, FP, backlog, wireframe, ERD
└── README.md
```

## Cara Menjalankan
```bash
# 1) Backend
cd backend
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python init_db.py          # buat database + user default
python app.py              # API di http://127.0.0.1:5000

# 2) Simulator sensor (terminal baru)
cd simulator
python sensor_simulator.py

# 3) Frontend (terminal baru)
cd frontend
python -m http.server 8000  # buka http://127.0.0.1:8000
```

User default (development saja): `admin / admin123`, `operator / operator123`.

## Endpoint API
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | `/api/health` | Cek server |
| POST | `/api/login` | Login (username, password) |
| GET | `/api/tanks` | Daftar tangki |
| POST | `/api/sensor-data` | Terima data sensor (dari simulator/ESP32) |
| GET | `/api/tanks/<id>/latest` | Data sensor terbaru |
| GET | `/api/tanks/<id>/history?limit=50` | Riwayat data sensor |
| GET / PUT | `/api/tanks/<id>/thresholds` | Baca / ubah ambang batas |
| GET | `/api/notifications?tank_id=` | Log notifikasi |

## Skema Database
`users`, `tanks`, `thresholds`, `sensor_data`, `notifications` — lihat `database/schema.sql`.

## Alur Kerja Git
- Branch: `main` (stabil), `develop`, dan `feature/<nama-fitur>`
- Task dikelola di GitHub Projects (Product Backlog & Sprint Backlog)
- Pull Request ke `develop`, direview minimal 1 anggota tim

## Anggota Tim
| Nama | NIM | Peran |
|------|-----|-------|
| ... | ... | Ketua Tim / Project Manager (Scrum Master) |
| ... | ... | System Analyst & UX Designer |
| ... | ... | Developer & Database Engineer |
````

## `.gitignore`

```text
__pycache__/
*.pyc
.venv/
venv/
*.db
.env
.DS_Store
```

## `database/schema.sql`

```sql
-- Skema database Digital Twin Tangki Air (SQLite; mudah dipindah ke MySQL/PostgreSQL)

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('admin', 'operator')),
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tanks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    location    TEXT,
    capacity_l  REAL NOT NULL,          -- kapasitas (liter)
    height_cm   REAL NOT NULL,          -- tinggi tangki (cm)
    source      TEXT NOT NULL DEFAULT 'simulator' CHECK (source IN ('simulator', 'sensor')),
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS thresholds (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    tank_id       INTEGER NOT NULL UNIQUE REFERENCES tanks(id) ON DELETE CASCADE,
    level_min_cm  REAL NOT NULL DEFAULT 40,
    level_max_cm  REAL NOT NULL DEFAULT 150,
    temp_min_c    REAL NOT NULL DEFAULT 15,
    temp_max_c    REAL NOT NULL DEFAULT 35,
    turbidity_max_ntu REAL NOT NULL DEFAULT 5,
    tds_max_ppm   REAL NOT NULL DEFAULT 500
);

CREATE TABLE IF NOT EXISTS sensor_data (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    tank_id       INTEGER NOT NULL REFERENCES tanks(id) ON DELETE CASCADE,
    level_cm      REAL NOT NULL,
    level_percent REAL NOT NULL,
    temp_c        REAL NOT NULL,
    turbidity_ntu REAL NOT NULL,
    tds_ppm       REAL NOT NULL,
    status        TEXT NOT NULL CHECK (status IN ('Normal', 'Waspada', 'Bahaya')),
    recorded_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sensor_tank_time ON sensor_data (tank_id, recorded_at);

CREATE TABLE IF NOT EXISTS notifications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tank_id     INTEGER NOT NULL REFERENCES tanks(id) ON DELETE CASCADE,
    message     TEXT NOT NULL,
    level       TEXT NOT NULL CHECK (level IN ('Info', 'Waspada', 'Bahaya')),
    channel     TEXT NOT NULL DEFAULT 'in-app',
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
```

## `database/seed.sql`

```sql
-- Data awal (dummy). User dibuat lewat backend/init_db.py agar password ter-hash.
INSERT INTO tanks (name, location, capacity_l, height_cm, source) VALUES
    ('Tangki Utama', 'Gedung A', 1000, 160, 'simulator'),
    ('Tangki B',     'Gedung B',  500, 120, 'simulator');

INSERT INTO thresholds (tank_id) VALUES (1), (2);
```

## `backend/requirements.txt`

```text
Flask>=3.0
```

## `backend/init_db.py`

```python
"""Inisialisasi database: buat tabel, isi data awal, dan buat user default."""
import os
import sqlite3
from werkzeug.security import generate_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE, "..", "database")
DB_PATH = os.path.join(DB_DIR, "tangki.db")


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    for name in ("schema.sql", "seed.sql"):
        with open(os.path.join(DB_DIR, name), encoding="utf-8") as f:
            conn.executescript(f.read())
    conn.executemany(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        [
            ("admin", generate_password_hash("admin123"), "admin"),
            ("operator", generate_password_hash("operator123"), "operator"),
        ],
    )
    conn.commit()
    conn.close()
    print("Database siap:", os.path.abspath(DB_PATH))
    print("User default: admin/admin123 dan operator/operator123 (hanya untuk development)")


if __name__ == "__main__":
    main()
```

## `backend/app.py`

```python
"""Backend REST API - Digital Twin Tangki Air (boilerplate Sprint 1)."""
import os
import sqlite3

from flask import Flask, g, jsonify, request
from werkzeug.security import check_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "..", "database", "tangki.db")

app = Flask(__name__)


@app.after_request
def add_cors(resp):
    """CORS sederhana agar frontend (file/port lain) bisa memanggil API saat development."""
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
    return resp


# ---------- Database helper ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def rows(query, args=()):
    return [dict(r) for r in get_db().execute(query, args).fetchall()]


# ---------- Logika status ----------
def _state(value, low, high, margin=0.10):
    """0 = Normal, 1 = Waspada (dekat batas), 2 = Bahaya (melewati batas)."""
    if (low is not None and value < low) or (high is not None and value > high):
        return 2
    span = (high if high is not None else value) - (low if low is not None else 0)
    tol = abs(span) * margin
    if (low is not None and value < low + tol) or (high is not None and value > high - tol):
        return 1
    return 0


def evaluate(data, th):
    checks = {
        "Ketinggian": _state(data["level_cm"], th["level_min_cm"], th["level_max_cm"]),
        "Suhu": _state(data["temp_c"], th["temp_min_c"], th["temp_max_c"]),
        "Kekeruhan": _state(data["turbidity_ntu"], None, th["turbidity_max_ntu"]),
        "TDS": _state(data["tds_ppm"], None, th["tds_max_ppm"]),
    }
    worst = max(checks.values())
    label = ["Normal", "Waspada", "Bahaya"][worst]
    problems = [k for k, v in checks.items() if v == worst and worst > 0]
    return label, problems


# ---------- Endpoint ----------
@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.post("/api/login")
def login():
    body = request.get_json(force=True, silent=True) or {}
    user = get_db().execute(
        "SELECT * FROM users WHERE username = ?", (body.get("username", ""),)
    ).fetchone()
    if user and check_password_hash(user["password_hash"], body.get("password", "")):
        # TODO Sprint 2: ganti dengan JWT/session
        return jsonify(ok=True, username=user["username"], role=user["role"])
    return jsonify(ok=False, error="Username atau password salah"), 401


@app.get("/api/tanks")
def list_tanks():
    return jsonify(rows("SELECT * FROM tanks ORDER BY id"))


@app.get("/api/tanks/<int:tank_id>/thresholds")
def get_thresholds(tank_id):
    r = rows("SELECT * FROM thresholds WHERE tank_id = ?", (tank_id,))
    return (jsonify(r[0]), 200) if r else (jsonify(error="Tangki tidak ditemukan"), 404)


@app.put("/api/tanks/<int:tank_id>/thresholds")
def update_thresholds(tank_id):
    body = request.get_json(force=True, silent=True) or {}
    fields = ["level_min_cm", "level_max_cm", "temp_min_c", "temp_max_c",
              "turbidity_max_ntu", "tds_max_ppm"]
    updates = {k: float(body[k]) for k in fields if k in body}
    if not updates:
        return jsonify(error="Tidak ada data yang diubah"), 400
    sets = ", ".join(f"{k} = ?" for k in updates)
    db = get_db()
    db.execute(f"UPDATE thresholds SET {sets} WHERE tank_id = ?", (*updates.values(), tank_id))
    db.commit()
    return jsonify(ok=True)


@app.post("/api/sensor-data")
def ingest():
    """Dipanggil simulator/sensor. Body: tank_id, level_cm, temp_c, turbidity_ntu, tds_ppm."""
    body = request.get_json(force=True, silent=True) or {}
    required = ["tank_id", "level_cm", "temp_c", "turbidity_ntu", "tds_ppm"]
    if any(k not in body for k in required):
        return jsonify(error=f"Field wajib: {', '.join(required)}"), 400

    db = get_db()
    tank = db.execute("SELECT * FROM tanks WHERE id = ?", (body["tank_id"],)).fetchone()
    th = db.execute("SELECT * FROM thresholds WHERE tank_id = ?", (body["tank_id"],)).fetchone()
    if not tank or not th:
        return jsonify(error="Tangki tidak ditemukan"), 404

    level_cm = float(body["level_cm"])
    data = {
        "level_cm": level_cm,
        "level_percent": round(level_cm / tank["height_cm"] * 100, 1),
        "temp_c": float(body["temp_c"]),
        "turbidity_ntu": float(body["turbidity_ntu"]),
        "tds_ppm": float(body["tds_ppm"]),
    }
    status, problems = evaluate(data, dict(th))

    db.execute(
        """INSERT INTO sensor_data
           (tank_id, level_cm, level_percent, temp_c, turbidity_ntu, tds_ppm, status)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (tank["id"], data["level_cm"], data["level_percent"], data["temp_c"],
         data["turbidity_ntu"], data["tds_ppm"], status),
    )

    if status != "Normal":
        msg = f"{', '.join(problems)} dalam kondisi {status.lower()}"
        last = db.execute(
            "SELECT message FROM notifications WHERE tank_id = ? ORDER BY id DESC LIMIT 1",
            (tank["id"],),
        ).fetchone()
        if not last or last["message"] != msg:  # hindari notifikasi berulang
            db.execute(
                "INSERT INTO notifications (tank_id, message, level) VALUES (?, ?, ?)",
                (tank["id"], msg, status),
            )
    db.commit()
    return jsonify(ok=True, status=status), 201


@app.get("/api/tanks/<int:tank_id>/latest")
def latest(tank_id):
    r = rows("SELECT * FROM sensor_data WHERE tank_id = ? ORDER BY id DESC LIMIT 1", (tank_id,))
    return jsonify(r[0]) if r else (jsonify(error="Belum ada data"), 404)


@app.get("/api/tanks/<int:tank_id>/history")
def history(tank_id):
    limit = min(int(request.args.get("limit", 50)), 1000)
    data = rows(
        "SELECT * FROM sensor_data WHERE tank_id = ? ORDER BY id DESC LIMIT ?",
        (tank_id, limit),
    )
    return jsonify(list(reversed(data)))


@app.get("/api/notifications")
def notifications():
    tank_id = request.args.get("tank_id")
    if tank_id:
        return jsonify(rows(
            "SELECT * FROM notifications WHERE tank_id = ? ORDER BY id DESC LIMIT 20", (tank_id,)))
    return jsonify(rows("SELECT * FROM notifications ORDER BY id DESC LIMIT 20"))


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        raise SystemExit("Database belum ada. Jalankan dulu: python init_db.py")
    app.run(debug=True, port=5000)
```

## `simulator/sensor_simulator.py`

```python
"""Simulator sensor tangki air: mengirim data dummy ke API secara berkala.

Pemakaian:  python sensor_simulator.py [--url http://127.0.0.1:5000] [--interval 3]
Hanya memakai library standar Python.
"""
import argparse
import json
import random
import time
import urllib.request

# id tangki -> tinggi (cm) dan level awal; harus sama dengan data di database/seed.sql
TANKS = {
    1: {"height": 160, "level": 120.0, "dir": -1},
    2: {"height": 120, "level": 80.0, "dir": -1},
}


def step(state):
    """Random walk sederhana: level naik-turun, kualitas air berfluktuasi."""
    state["level"] += state["dir"] * random.uniform(0.5, 3.0)
    if state["level"] <= 20:
        state["dir"] = 1            # mulai diisi
    elif state["level"] >= state["height"] - 5:
        state["dir"] = -1           # mulai terpakai
    state["level"] = max(0, min(state["height"], state["level"]))
    return {
        "level_cm": round(state["level"], 1),
        "temp_c": round(random.gauss(27.5, 1.0), 1),
        "turbidity_ntu": round(abs(random.gauss(3.0, 1.0)), 1),
        "tds_ppm": round(random.gauss(330, 40), 0),
    }


def post(url, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.load(resp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:5000")
    ap.add_argument("--interval", type=float, default=3.0)
    args = ap.parse_args()

    print("Simulator berjalan. Tekan Ctrl+C untuk berhenti.")
    while True:
        for tank_id, state in TANKS.items():
            payload = {"tank_id": tank_id, **step(state)}
            try:
                res = post(f"{args.url}/api/sensor-data", payload)
                print(f"[Tangki {tank_id}] {payload} -> {res.get('status')}")
            except Exception as exc:  # noqa: BLE001
                print(f"[Tangki {tank_id}] gagal kirim: {exc}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
```

## `frontend/index.html`

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Digital Twin Tangki Air</title>
  <link rel="stylesheet" href="style.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
</head>
<body>
  <header>
    <h1>💧 Digital Twin Tangki Air</h1>
    <div>
      <select id="tankSelect"></select>
      <span id="conn" class="badge">Menghubungkan…</span>
    </div>
  </header>

  <main>
    <section class="twin">
      <div class="tank"><div id="water" class="water"></div><span id="levelPct">0%</span></div>
    </section>

    <section class="cards">
      <div class="card"><h3>Ketinggian</h3><p id="vLevel">-</p></div>
      <div class="card"><h3>Suhu</h3><p id="vTemp">-</p></div>
      <div class="card"><h3>Kekeruhan</h3><p id="vTurb">-</p></div>
      <div class="card"><h3>TDS</h3><p id="vTds">-</p></div>
      <div class="card"><h3>Status Umum</h3><p><span id="sAll" class="badge">-</span></p></div>
    </section>

    <section class="panel"><h3>Tren Ketinggian (cm)</h3><canvas id="chart" height="90"></canvas></section>
    <section class="panel"><h3>Notifikasi Terbaru</h3><ul id="notif"></ul></section>
  </main>

  <script src="app.js"></script>
</body>
</html>
```

## `frontend/style.css`

```css
:root { --ok:#28a745; --warn:#ffc107; --bad:#dc3545; --water:#0d6efd; }
* { box-sizing: border-box; }
body { margin:0; font-family: system-ui, sans-serif; background:#f4f6f9; color:#222; }
header { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#0b3d63; color:#fff; }
header h1 { font-size:1.2rem; margin:0; }
main { max-width:1000px; margin:20px auto; padding:0 16px; display:grid; gap:16px; grid-template-columns:180px 1fr; }
.panel { grid-column:1 / -1; }
.twin { display:flex; justify-content:center; }
.tank { position:relative; width:130px; height:220px; border:4px solid #555; border-top:none; border-radius:0 0 14px 14px; background:#fff; overflow:hidden; }
.water { position:absolute; bottom:0; width:100%; height:0%; background:var(--water); opacity:.75; transition:height .8s ease; }
#levelPct { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-weight:700; }
.cards { display:grid; grid-template-columns:repeat(auto-fit, minmax(150px,1fr)); gap:12px; }
.card, .panel { background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 4px rgba(0,0,0,.08); }
.card h3, .panel h3 { margin:0 0 6px; font-size:.85rem; color:#666; }
.card p { margin:0; font-size:1.4rem; font-weight:700; }
.badge { display:inline-block; padding:2px 10px; border-radius:12px; font-size:.75rem; color:#fff; background:#888; }
.badge.Normal { background:var(--ok); }
.badge.Waspada { background:var(--warn); color:#222; }
.badge.Bahaya { background:var(--bad); }
#notif { list-style:none; margin:0; padding:0; }
#notif li { padding:6px 0; border-bottom:1px solid #eee; font-size:.9rem; }
@media (max-width:700px){ main{grid-template-columns:1fr;} }
```

## `frontend/app.js`

```javascript
const API = "http://127.0.0.1:5000/api";
const $ = (id) => document.getElementById(id);
let chart, tankId = 1;

async function get(path) {
  const r = await fetch(API + path);
  if (!r.ok) throw new Error(r.status);
  return r.json();
}

function setBadge(el, status, text) { el.textContent = text ?? status; el.className = "badge " + status; }

async function loadTanks() {
  const tanks = await get("/tanks");
  $("tankSelect").innerHTML = tanks.map(t => `<option value="${t.id}">${t.name}</option>`).join("");
  tankId = tanks[0]?.id ?? 1;
  $("tankSelect").onchange = (e) => { tankId = e.target.value; refresh(); };
}

async function refresh() {
  try {
    const d = await get(`/tanks/${tankId}/latest`);
    $("water").style.height = d.level_percent + "%";
    $("levelPct").textContent = d.level_percent + "%";
    $("vLevel").textContent = `${d.level_cm} cm`;
    $("vTemp").textContent = `${d.temp_c} °C`;
    $("vTurb").textContent = `${d.turbidity_ntu} NTU`;
    $("vTds").textContent = `${d.tds_ppm} ppm`;
    setBadge($("sAll"), d.status);
    setBadge($("conn"), "Normal", "● Terhubung");

    const h = await get(`/tanks/${tankId}/history?limit=40`);
    const labels = h.map(x => x.recorded_at.slice(11, 19));
    const values = h.map(x => x.level_cm);
    if (!chart) {
      chart = new Chart($("chart"), {
        type: "line",
        data: { labels, datasets: [{ label: "Ketinggian (cm)", data: values, borderColor: "#0d6efd", tension: .3 }] },
        options: { animation: false },
      });
    } else {
      chart.data.labels = labels;
      chart.data.datasets[0].data = values;
      chart.update();
    }

    const n = await get(`/notifications?tank_id=${tankId}`);
    $("notif").innerHTML = n.length
      ? n.map(x => `<li>${x.created_at.slice(11, 16)} — ${x.message} <span class="badge ${x.level}">${x.level}</span></li>`).join("")
      : "<li>Belum ada notifikasi</li>";
  } catch (e) {
    setBadge($("conn"), "Bahaya", "● Terputus / belum ada data");
  }
}

loadTanks().then(() => { refresh(); setInterval(refresh, 3000); });
```
