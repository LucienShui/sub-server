import os
from datetime import datetime

import httpx
import uvicorn
from fastapi import FastAPI, Response

from util import get_sub_link

sub_url: str = os.environ["SUB_URL"]
sub_id: str = os.environ.get("SUB_ID", None)
api_key: str = os.environ["API_KEY"]
start_date: datetime = datetime.now()
app = FastAPI()


@app.get("/api/v1/health")
async def health():
    return {"uptime": (datetime.now() - start_date).total_seconds()}


@app.get("/api/v1/subscription")
async def get_subscription(token: str):
    if token == api_key:
        async with httpx.AsyncClient(timeout=300, transport=httpx.AsyncHTTPTransport(retries=3)) as client:
            router_response = await client.get(sub_url)
            if sub_id is None:
                return Response(content=router_response.text, media_type="text/plain")
            sub_link: str = get_sub_link(router_response.text, sub_id)
            sub_response = await client.get(sub_link)
            assert sub_response.status_code == 200, sub_response.text
            return Response(content=sub_response.text, media_type="text/plain")
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
