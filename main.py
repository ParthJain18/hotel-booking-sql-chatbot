from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
import httpx

# Define your target NGROK URL
NGROK_URL = "https://logical-witty-ocelot.ngrok-free.app"

app = FastAPI()

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_request(request: Request, full_path: str):
    """Display apology page and redirect to NGROK"""
    # HTML apology page with auto-redirect after 5 seconds
    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Service Temporarily Unavailable</title>
            <meta http-equiv="refresh" content="5;url={NGROK_URL}" />
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                h1 {{ color: #333; }}
                p {{ color: #666; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .redirect-link {{ color: #0066cc; text-decoration: none; }}
                .redirect-link:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>We apologize for the inconvenience</h1>
                <p>Our proxy service is currently unavailable.</p>
                <p>You will be redirected to the direct service in 5 seconds.</p>
                <p>If you are not redirected automatically, please click 
                   <a class="redirect-link" href="{NGROK_URL}">here</a> to continue.</p>
            </div>
        </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

# Add a root route for direct access to the homepage
@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url=NGROK_URL)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)