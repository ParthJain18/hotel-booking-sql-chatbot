import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from routes import dashboard, chat, data_entry

app = FastAPI(title="Hotel Booking Analytics")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(dashboard.router)
app.include_router(chat.router)
app.include_router(data_entry.router)

@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/dashboard")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)