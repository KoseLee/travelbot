from fastapi import FastAPI, HTTPException
from main import chain
from model.rag_query import QueryInput
from utils.async_utils import async_retry
import uvicorn

app = FastAPI(
    title="Travel_Bot",
    description="Endpoints of a system RAG chatbot"
)

@async_retry(max_retries=10, delay=1)
async def invoke_rag_with_retry(query: str):
    """Retry the agent if a tool fails to run.
    This can help when there are intermittent connection issues
    to external APIs.
    """
    return await chain.ainvoke(query)

@app.get("/")
async def get_status():
    return {"status": "running"}

@app.post("/travel-rag", response_model=str)
async def query_hospital_agent(query: QueryInput) -> str:
    try:
        query_response = await invoke_rag_with_retry(query.text)
        # Đảm bảo rằng query_response là một chuỗi và trả về
        return query_response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run("Api:app", host="127.0.0.1", port=8001, reload=True)
