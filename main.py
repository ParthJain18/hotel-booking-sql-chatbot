from fastapi import FastAPI, Request
import httpx

# Define your target NGROK URL
NGROK_URL = "https://logical-witty-ocelot.ngrok-free.app"

app = FastAPI()

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_request(request: Request, full_path: str):
    """Forward all requests to NGROK"""
    async with httpx.AsyncClient() as client:
        url = f"{NGROK_URL}/{full_path}"
        method = request.method
        headers = dict(request.headers)
        content = await request.body()

        # Forward request
        response = await client.request(method, url, headers=headers, content=content)

        return response.json() if "application/json" in response.headers.get("content-type", "") else response.text

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
