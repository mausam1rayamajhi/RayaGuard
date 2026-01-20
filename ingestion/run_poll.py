
import json
from pathlib import Path

from fetch_jobs import fetch_jobs
from cdc_engine import detect_cdc_events

BOARD_TOKEN = "airbnb"
STATE_FILE = Path("ingestion/state_store.json")
EVENTS_FILE = Path("events/emitted_events.json")

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def emit_events(events: list):
    EVENTS_FILE.parent.mkdir(exist_ok=True)
    with EVENTS_FILE.open("a") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

def main():
    prev_state = load_state()

    snapshot = fetch_jobs(BOARD_TOKEN)
    jobs = {job["id"]: job for job in snapshot["jobs"]}

    events, new_state = detect_cdc_events(
        board=BOARD_TOKEN,
        current_jobs=jobs,
        prev_state=prev_state,
    )

    emit_events(events)
    save_state(new_state)

    print(f"Emitted {len(events)} events")

if __name__ == "__main__":
    main()
