RayaGuard

Event-driven data ingestion and observability foundation that detects pipeline freshness issues, unexpected data changes, and silent dailures 
by converting API snapshots into auditable cdc events. 


what this project does
API ingestion
Change Data Capture
Event Modeling
eventlog (Bronze layer)
Observability Metrics
Local Development and execution

Architecture overview

Greenhouse API         
    |
Fetch_jobs.py          (extract)
    |
cdc_engine.py          (Transform)
    |
events/yyyy-mm-dd       (Load - Bronze)
    |
state_store.json       (Incremental State)
