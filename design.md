# Designing RayaGuard

## 1 Choosing Greenhouse Job board for the data

    Rayguard uses the greehouse Job Board API as representative public data sources for ingestestion and change detection.

### API Endpoint
    This pipline uses the below endpoint to get job and organizational data:
    
    GET https://boards-api.greenhouse.io/v1/boards/{board_token}/offices
    THis Returns a list of all of your organization's offices, departments and jobs postings. 

### why I chose Greenhouse Job API 

    - It is public and unaunthenticated
    - It is stable and widely used
    - It returns clean and structure JSON
    - It shows the real world ingestion pipeline used by data engineering teams

### Design plan

    - The pipeline does not hard coding any specific companies
    - A board_token is proviced at runtime
    - multiple companies are used as sample boards to validate the system
    - Tne architecture supports scaling from one job board to many without structural changes
    
    using greenhouse shows how real team steams data from public APIs and we design the system to scale from a few job boards to many with no architectural changes

### end point validation
    1. running this in my terminal to check if check if url and params work: validating the endpoint

    curl "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?content=true"

### Architecture 
ingestion layer is implemented in ingestion directory:

    ingestion/
    ├── fetch_jobs.py
    ├── cdc_engine.py
    ├── state_store.json
    ├── run_poll.py

### component Respnsibilities

    ingestion
        fetch_jobs.py (to call greenhouse, fetch snapshot and return json)
        cdc_engine ( cdc logic: change detiection brain, takes previous and current snap shot and comare them and figures out new jobs, updated     job, closed jobs and so on. it is to basically convert snap shot into event        
        we implement cdc rules and create events)
        state_store.json (to persist S_prev: meaning just stores the last know snapshot)
        run_poll ( this coordinates the whole flow: loads, calls, runs, emits events and saves. //glue layer)
        
### current status:
    snapshot ingestion validated using curl
    CDC logic implemented and tested locally
    first successful run emitted 227 job_created events 
    state persistence was verified
