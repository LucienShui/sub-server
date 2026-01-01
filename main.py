import os
from datetime import datetime

import httpx
import uvicorn
from fastapi import FastAPI, Response

api_key: str = os.environ["API_KEY"]
start_date: datetime = datetime.now()
app = FastAPI()

DATA_DIR = "data"
filename = "subscription.txt"

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


@app.get("/api/v1/health")
async def health():
    return {"uptime": (datetime.now() - start_date).total_seconds()}


@app.post("/api/v1/subscription")
async def fetch_subscription(url: str, token: str):
    if token == api_key:
        async with httpx.AsyncClient(timeout=300, transport=httpx.AsyncHTTPTransport(retries=3)) as client:
            sub_response = await client.get(url)
            assert sub_response.status_code == 200, sub_response.text
            content: str = sub_response.text
            with open(os.path.join(DATA_DIR, filename), "w") as f:
                f.write(content)
            return Response(content=content, media_type="text/plain")
    else:
        return Response(content="Unauthorized", status_code=401)


@app.get("/api/v1/subscription")
async def get_subscription(token: str):
    if token == api_key:
        if os.path.exists(os.path.join(DATA_DIR, filename)):
            with open(os.path.join(DATA_DIR, filename)) as f:
                content: str = f.read()
            return Response(content=content, media_type="text/plain")
        else:
            return Response(content="Not Found", status_code=404)
    else:
        return Response(content="Unauthorized", status_code=401)


def main():
    uvicorn.run(
        'main:app',
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 8000)),
        workers=int(os.environ.get('WORKERS', 1))
    )


if __name__ == '__main__':
    main()
