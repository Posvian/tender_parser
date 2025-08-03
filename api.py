from fastapi import FastAPI
from parser import parse_tenders

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


@app.get("/tenders")
async def get_tenders(max_count: int = 100):
    tenders = parse_tenders(max_count=max_count)
    return {"tenders": tenders}
