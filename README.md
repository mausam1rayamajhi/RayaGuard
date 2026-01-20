# RayaGuard
Real time data observability and quality monitoring platforms that checks pipelines for freshness, schema drift, data completeness and anomalies using event driven architectures

## Goals 
- catching pipeline failures early
- detecting silent data corruption like nulls, duplicates, schema drifts
- providing auditable quality signals like metrics and alert history

## what's implemented so far
- public API ingestion using the greenhouse Job board API
- snapshot based polling was converted into CDC style events
- detection of: job_created, job_updated, job_closed, job_reopened
- event time vs ingestion time
- detecting change

this shows how real data platforms transforms non streamoing APIs into streaming event sources. 

## local development
running a polling cycle locally

```bash 
python ingestion/run_poll.py
```
for quick verification
``` bash
grep '"event_type"' events/emitted_events.json | head  
```