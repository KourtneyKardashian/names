import asyncio
from fastapi import FastAPI, Query, HTTPException
from curl_cffi import requests

app = FastAPI()

async def fetch_json(url: str):
    session = requests.Session(impersonate='chrome116')
    loop = asyncio.get_running_loop()

    def get_json():
        response = session.get(url, timeout=15)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as e:
                raise ValueError("Response is not valid JSON") from e
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch URL")

    return await loop.run_in_executor(None, get_json)

@app.get("/fetch_json/")
async def fetch_json_endpoint(url: str = Query(...)):
    data = await fetch_json(url)
    return data
    
@app.get("/")
async def root():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, workers=4)
