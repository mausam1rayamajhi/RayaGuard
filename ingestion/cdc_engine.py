#comparing S_now and S_prev and emitting CDC events

import hashlib
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def _normalize_list(items):
    """
    items might be list[dict] or list[str]. Make ordering stable.
    """
    if not items:
        return []
    if isinstance(items[0], dict):
        # sorting by id if present, else name, else whole dict
        def keyfn(x):
            return (str(x.get("id", "")), str(x.get("name", "")), json.dumps(x, sort_keys=True))
        return sorted(items, key=keyfn)
    return sorted([str(x) for x in items])

def build_fingerprint(job:dict) -> str:
    """
    building a stable fingerprint for job
    """
    relevent_fields = {
        "title":job.get("title"),
        "location":job.get("location"),
        "departments":job.get("departments"),
        "offices":job.get("offices"),
        "content":job.get("content"),
    }
    normalized = str(relevent_fields).encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()

def detect_cdc_events(board:str, current_jobs:dict, prev_state:dict):

    events = []
    new_state = {}

    snapshot_time = utc_now()

    for job_id, job in current_jobs.items():
        fingerprint = build_fingerprint(job)
        updated_at = job.get("updated_at")

        if job_id not in prev_state:
            events.append({
                "event_type": "job_created",
                "board": board,
                "job_id": job_id,
                "event_ts": updated_at,
                "ingestion_ts": snapshot_time,
            })

            status = "open"

        else:
            prev = prev_state[job_id]
            status = prev["status"]

            if (
                prev["updated_at"] != updated_at
                or prev["fingerprint"] != fingerprint
            ):
                events.append({
                    "event_type": "job_updated",
                    "board": board,
                    "job_id": job_id,
                    "event_ts": updated_at,
                    "ingestion_ts": snapshot_time,
                })

        new_state[job_id] = {
            "updated_at": updated_at,
            "fingerprint": fingerprint,
            "status": "open",
        }

    # --- job_closed ---
    for job_id, prev in prev_state.items():
        if job_id not in current_jobs and prev["status"] == "open":
            events.append({
                "event_type": "job_closed",
                "board": board,
                "job_id": job_id,
                "event_ts": snapshot_time,
                "ingestion_ts": snapshot_time,
            })

            new_state[job_id] = {
                **prev,
                "status": "closed",
            }

    return events, new_state