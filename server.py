"""
server.py — AI-Powered Unified Disaster Command Platform
Python HTTP backend using only the standard library (no Flask needed).

Endpoints:
  POST /report    — Accept incident, assign AI priority, return JSON
  GET  /incidents — Return all in-memory incidents (demo; real data is in Firestore)

Run: python server.py
"""

import json
import math
import uuid
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# ── Port ──────────────────────────────────────────────────────────────────────
PORT = 8000

# ── In-memory store (supplements Firestore for demo) ─────────────────────────
incidents_store: list[dict] = []

# ── Simulated resource pool ───────────────────────────────────────────────────
resources = [
    {"id": "RES-001", "type": "fire truck", "latitude": 19.0820, "longitude": 72.8820, "available": True},
    {"id": "RES-002", "type": "ambulance",  "latitude": 19.0700, "longitude": 72.8700, "available": True},
    {"id": "RES-003", "type": "police car", "latitude": 19.0760, "longitude": 72.8600, "available": True},
    {"id": "RES-004", "type": "ambulance",  "latitude": 19.0900, "longitude": 72.8900, "available": True},
    {"id": "RES-005", "type": "fire truck", "latitude": 19.0600, "longitude": 72.8500, "available": True},
]


# ── AI Priority Engine ────────────────────────────────────────────────────────
HIGH_TYPES   = {"fire", "accident", "injury"}
MEDIUM_TYPES = {"flood", "damage"}

def assign_priority(incident_type: str) -> str:
    """
    Rule-based AI prioritisation:
      HIGH   → fire, accident, injury   (immediate life threat)
      MEDIUM → flood, damage            (urgent but not immediately fatal)
      LOW    → everything else          (monitoring / informational)
    """
    t = incident_type.strip().lower()
    if t in HIGH_TYPES:   return "HIGH"
    if t in MEDIUM_TYPES: return "MEDIUM"
    return "LOW"


# ── Resource Allocation ───────────────────────────────────────────────────────
def haversine(lat1, lng1, lat2, lng2) -> float:
    """Return distance in km between two GPS coordinates."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def preferred_resource_type(incident_type: str) -> str:
    t = incident_type.lower()
    if t == "fire":                     return "fire truck"
    if t in {"accident", "injury"}:     return "ambulance"
    return "police car"


def find_and_assign_resource(incident_type: str, lat: float, lng: float) -> dict | None:
    """Find nearest available preferred resource and mark it busy."""
    pref = preferred_resource_type(incident_type)
    candidates = [r for r in resources if r["available"]]
    # Prefer matching type, then fall back to any available
    preferred  = [r for r in candidates if r["type"] == pref]
    pool       = preferred if preferred else candidates
    if not pool:
        return None
    nearest = min(pool, key=lambda r: haversine(lat, lng, r["latitude"], r["longitude"]))
    nearest["available"] = False
    return nearest


# ── CORS headers helper ───────────────────────────────────────────────────────
def send_cors_headers(handler):
    handler.send_header("Access-Control-Allow-Origin",  "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")


# ── Request Handler ───────────────────────────────────────────────────────────
class DisasterHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {fmt % args}")

    # ── OPTIONS (pre-flight CORS) ──
    def do_OPTIONS(self):
        self.send_response(204)
        send_cors_headers(self)
        self.end_headers()

    # ── GET ──
    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/incidents":
            self._json_response(200, incidents_store)

        elif path == "/resources":
            self._json_response(200, resources)

        elif path == "/health":
            self._json_response(200, {"status": "ok", "incidents": len(incidents_store)})

        else:
            self._json_response(404, {"error": "Endpoint not found"})

    # ── POST ──
    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/report":
            length = int(self.headers.get("Content-Length", 0))
            body   = self.rfile.read(length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self._json_response(400, {"error": "Invalid JSON body"})
                return

            incident_type = data.get("type", "").strip()
            location      = data.get("location", "").strip()
            lat           = float(data.get("latitude",  19.0760))
            lng           = float(data.get("longitude", 72.8777))

            if not incident_type or not location:
                self._json_response(400, {"error": "Fields 'type' and 'location' are required"})
                return

            # AI prioritisation
            priority = assign_priority(incident_type)

            # Resource allocation
            resource = find_and_assign_resource(incident_type, lat, lng)

            # Build incident record
            incident = {
                "id":               str(uuid.uuid4())[:8].upper(),
                "type":             incident_type,
                "location":         location,
                "latitude":         lat,
                "longitude":        lng,
                "priority":         priority,
                "status":           "Active",
                "timestamp":        datetime.now().isoformat(),
                "assigned_resource": resource["id"] if resource else None,
            }
            incidents_store.append(incident)

            print(f"  → Incident #{incident['id']} | {incident_type.upper()} | {priority} | {location}")
            if resource:
                print(f"  → Dispatched: {resource['type']} ({resource['id']})")
            else:
                print("  → No resources available!")

            self._json_response(201, incident)

        else:
            self._json_response(404, {"error": "Endpoint not found"})

    # ── Helper ──
    def _json_response(self, code: int, payload):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type",   "application/json")
        self.send_header("Content-Length", str(len(body)))
        send_cors_headers(self)
        self.end_headers()
        self.wfile.write(body)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  🚨  AI Disaster Command Platform — Python Backend")
    print(f"      Listening on http://localhost:{PORT}")
    print("=" * 55)
    print("  Endpoints:")
    print(f"    GET  http://localhost:{PORT}/health")
    print(f"    GET  http://localhost:{PORT}/incidents")
    print(f"    GET  http://localhost:{PORT}/resources")
    print(f"    POST http://localhost:{PORT}/report")
    print("=" * 55)

    server = HTTPServer(("", PORT), DisasterHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()
