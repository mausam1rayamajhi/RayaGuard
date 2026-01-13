# calling greenhouse api

import requests

GREENHOUSE_BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

def fetch_jobs(board_token : str, include_content: bool = True) -> dict:
    """
    fetching current snapshot of jobs from greenhouse
    returns raw Json Reponse
    """

    params = { "content": "true"} if include_content else{}
    url = f"{GREENHOUSE_BASE_URL}/{board_token}/jobs"

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()