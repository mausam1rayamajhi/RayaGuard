
import json
from pathlib import Path
from datetime import datetime, timezone
from fetch_jobs import fetch_jobs
from cdc_engine import detect_cdc_events
from ingestion.event_writer import append_events_jsonl


BOARD_TOKEN = "airbnb"
STATE_FILE = Path("ingestion/state_store.json")
EVENTS_FILE = Path("events/emitted_events.json")

def load_state():
    '''
    loading the previous state from state_store.json. if the file does not exist, then return empty state
    '''
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state: dict):
    '''
    saving the new state so next run can be compared against it 
    '''
    STATE_FILE.write_text(json.dumps(state, indent=2))

def emit_events(events: list):
    EVENTS_FILE.parent.mkdir(exist_ok=True)
    with EVENTS_FILE.open("a") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

def main():
    #loading the previous state
    prev_state = load_state()

    snapshot = fetch_jobs(BOARD_TOKEN)
    jobs = {job["id"]: job for job in snapshot["jobs"]}

    events, new_state = detect_cdc_events(
        board=BOARD_TOKEN,
        current_jobs=jobs,
        prev_state=prev_state,
    )

    EVENTS_DIR = Path("ingestion/events")
    now_ts = datetime.now(timezone.utc)
    events_file = append_events_jsonl(EVENTS_DIR, events, now_ts)
    print(f"Wrote {len(events)} events to {events_file}")

    save_state(new_state)

    print(f"Emitted {len(events)} events")

if __name__ == "__main__":
    main()
