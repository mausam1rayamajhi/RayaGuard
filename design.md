# Designing RayaGuard

## 1 Picking Greenhouse Job board for the data

    I will be using the end point 
    ###listing offices
    Returns a list of all of your organization's departments and jobs, grouped by office
    GET https://boards-api.greenhouse.io/v1/boards/{board_token}/offices

    why I chose Greenhouse Job API 

    - public and unaunthenticated
    - stable and widely used
    - returns clean and structure JSON
    - common in real data engineering ingestion pipelines. 

    plan
    not hard coding any specific companies
    But I will use some companies as sample boards to validate the pipeline

    using greenhouse as it mirrors how real team steams data from public APIs and we design the system to scale from a few job boards to many with no architectural changes

    1. running this in my terminal to check if check if url and params work: validating the endpoint

    curl "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?content=true"

    creating ingesting with files 

    injestion
        fetch_jobs.py (to call greenhouse, fetch snapshot and return json)
        cdc_engine ( cdc logic: change detiection brain, takes previous and current snap shot and comare them and figures out new jobs, updated job, closed jobs and so on. it is to basically convert snap shot into event
        
        we implement cdc rules and create events)
        state_store.json (to persist S_prev: meaning just stores the last know snapshot)
        run_poll ( this coordinates the whole flow: loads, calls, runs, emits events and saves. //glue layer)
        
    current status:
    snapshot ingestion validated using curl
    CDC logic implemented and tested locally
    first successful run emitted 227 job_created events 
    state persistence was verified