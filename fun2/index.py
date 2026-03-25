from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI()

import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
QUE = [
    {"q": "How many months have 28 days?", "a": "All months"},
    {"q": "If 2+2×2 = ?", "a": "6"},
    {"q": "Which weighs more: 1kg cotton or 1kg iron?", "a": "Same"},
    {"q": "A farmer has 17 sheep, all but 9 die. How many left?", "a": "9"},
    {"q": "If you overtake second place, what position are you?", "a": "Second"},
    {"q": "What comes next: 2, 4, 8, 16, ?", "a": "32"},
    {"q": "How many sides does a circle have?", "a": "2"},
    {"q": "What is half of 100?", "a": "50"},
    {"q": "What is always in front of you but can’t be seen?", "a": "Future"},
    {"q": "If 5 machines make 5 items in 5 minutes, 100 machines make 100 items in?", "a": "5 minutes"},
    
    {"q": "What has hands but can't clap?", "a": "Clock"},
    {"q": "What has one eye but can't see?", "a": "Needle"},
    {"q": "What gets wetter as it dries?", "a": "Towel"},
    {"q": "What has keys but no locks?", "a": "Keyboard"},
    {"q": "What has legs but doesn't walk?", "a": "Table"},
    {"q": "What has neck but no head?", "a": "Bottle"},
    {"q": "What has many teeth but can't bite?", "a": "Comb"},
    {"q": "What can travel around the world while staying in corner?", "a": "Stamp"},
    {"q": "What has face but no eyes?", "a": "Clock"},
    {"q": "What goes up but never comes down?", "a": "Age"}
]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    "index.html",
    {"request": request}
)


@app.get("/random")
async def random_question():
    return random.choice(QUE)


@app.post("/check")
async def check(data: dict):
    user = data["user"].lower().strip()
    correct = data["correct"].lower().strip()

    if user == correct:
        return {"result": "correct"}
    else:
        return {"result": "wrong"}
    
handler = app