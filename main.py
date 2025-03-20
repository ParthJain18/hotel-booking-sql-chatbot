from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
import httpx

# Define your target NGROK URL
NGROK_URL = "https://logical-witty-ocelot.ngrok-free.app"

app = FastAPI()


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_request(request: Request, full_path: str):
    target_url = f"{NGROK_URL}/{full_path}"
    return RedirectResponse(url=target_url)


@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url=NGROK_URL)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
