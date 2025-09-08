import uuid
from typing import Dict, Any

jobs: Dict[str, Dict[str, Any]] = {} # TODO: In production, changing this to a DB

def create_job() -> str:
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "result": None,
        "error": None,
    }
    return job_id

def update_job(job_id: str, status: str, progress: int, result: Any = None, error: str = None):
    if job_id in jobs:
        jobs[job_id].update({
            "status": status,
            "progress": progress,
            "result": result,
            "error": error,
        })

def get_job(job_id: str) -> Dict[str, Any]:
    return jobs.get(job_id, {"error": "Job not found"})
