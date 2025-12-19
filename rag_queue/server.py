from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.woker import process_query


app = FastAPI()


@app.get("/")
def root():
    return{
        "status" : "Server is up and running"
    }

@app.post("/chat")
def chat(
        query : str = Query(..., description="The chat query of user")
):
    # Enqueue
    job = queue.enqueue(process_query, query)
    # This return ID of job

    return {
        "status" : "queued", 
        "job_id" : job.id
    }


@app.get("/job-status")
def get_result(
        job_id : str = Query(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {
        "result" : result
    }