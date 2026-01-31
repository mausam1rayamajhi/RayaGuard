# cdc_engine.py
import hashlib
import json
from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def build_fingerprint(job: dict) -> str:
    """
    Creating a stable fingerprint from key job fields.
    Keep this SIMPLE to avoid false updates.
    Basically just important content of job posting
    """
    payload = {
        "title": job.get("title"),
        "location": job.get("location"),
    }

    normalized = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


def detect_cdc_events(board: str, current_jobs: dict, prev_state: dict):
    events = []
    new_state = {}
    snapshot_time = utc_now()

    # Normalizing job_id to string
    current_jobs = {str(k): v for k, v in current_jobs.items()}
    prev_state = {str(k): v for k, v in prev_state.items()}

    # --- created & updated ---
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
        else:
            if prev_state[job_id]["fingerprint"] != fingerprint:
                events.append({
                    "event_type": "job_updated",
                    "board": board,
                    "job_id": job_id,
                    "event_ts": updated_at,
                    "ingestion_ts": snapshot_time,
                })

        new_state[job_id] = {
            "fingerprint": fingerprint,
            "status": "open",
        }

    # --- closed ---
    for job_id in prev_state:
        if job_id not in current_jobs:
            events.append({
                "event_type": "job_closed",
                "board": board,
                "job_id": job_id,
                "event_ts": snapshot_time,
                "ingestion_ts": snapshot_time,
            })
            new_state[job_id] = {
                **prev_state[job_id],
                "status": "closed",
            }

    return events, new_state
