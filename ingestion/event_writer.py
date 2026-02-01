#creating this so that it is easy to append, grep, reply
#

import json
from pathlib import Path
from datetime import datetime, timezone

def utc_date_str(ts:datetime | None = None) -> str:
    ts = ts or datetime.now(timezone.utc)
    return ts.strftime("%Y-%m-%d")

def event_path(base_dir: Path, ts:datetime | None = None)-> Path:
    day= utc_date_str(ts)
    return base_dir/day/ "events.jsonl"

def append_events_jsonl(base_dir: Path, events:list[dict],ts:datetime | None = None)-> Path:
    path = event_path(base_dir, ts)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e,ensure_ascii=False)+ "\n")
    return path