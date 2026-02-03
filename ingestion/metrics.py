from collections import Counter

def count_event_types(events:list[dict])-> dict[str,int]:
    c = Counter(e.get("event_type") for e in events)

    return {
        "job_created": c.get("job_created", 0),
        "job_updated": c.get("job_updated", 0),
        "job_closed": c.get("job_closed", 0),
        "job_reopened": c.get("job_reopened", 0),
    }