import time
import json
from pathlib import Path
from datetime import datetime, timezone
from fetch_jobs import fetch_jobs
from cdc_engine import detect_cdc_events
from ingestion.event_writer import append_events_jsonl
from ingestion.metrics import count_event_types


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

    t0 = time.perf_counter()

    snapshot = fetch_jobs(BOARD_TOKEN)
    jobs = {job["id"]: job for job in snapshot["jobs"]}

    events, new_state = detect_cdc_events(
        board=BOARD_TOKEN,
        current_jobs=jobs,
        prev_state=prev_state,
    )
    runtime_s = time.perf_counter() - t0

    counts = count_event_types(events)
    total_jobs = len(jobs)
    emited = len(events)
    print(
        f"Fetched {total_jobs} jobs | "
        f"created={counts['job_created']} updated={counts['job_updated']} "
        f"closed={counts['job_closed']} reopened={counts['job_reopened']} | "
        f"emitted={emitted} | runtime={runtime_s:.2f}s"
    )

    EVENTS_DIR = Path("ingestion/events")
    now_ts = datetime.now(timezone.utc)
    events_file = append_events_jsonl(EVENTS_DIR, events, now_ts)
    print(f"Wrote {len(events)} events to {events_file}")

    save_state(new_state)

    print(f"Emitted {len(events)} events")

if __name__ == "__main__":
    main()
