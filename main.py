from fastapi import FastAPI
from gemini_test import answer
from pydantic import BaseModel
import logging 
import time

logging.basicConfig(
    filename="queries.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    encoding="utf-8",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("google_genai").setLevel(logging.WARNING)

class QueryRequest(BaseModel):
    question: str

app = FastAPI()

@app.post("/query")
def query(request: QueryRequest):
    start = time.time()
    res = answer(request.question)
    run_time = time.time() - start
    logging.info(f"{request.question} | distance={res['distance']} | used={res['sources_used']} | {run_time:.1f}s")
    return {"answer": res["answer"],"sources_used": res["sources_used"]}