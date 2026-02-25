from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

DEFAULT_CODE = """#include <stdio.h>

int main() {
    printf("Hello, Bytefest!");
    return 0;
}
"""

class LoadRequest(BaseModel):
    secret_code: str

class SubmitRequest(BaseModel):
    user_code: str
    time_taken: int

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/load-code")
def load_code(data: LoadRequest):
    if data.secret_code != "123":
        return {"success": False, "message": "Invalid secret code"}

    elements = DEFAULT_CODE.replace("\n", " \n ").split(" ")
    elements = [e for e in elements if e.strip()]

    return {
        "success": True,
        "code_elements": elements,
        "time_limit": 120
    }

@app.post("/submit-code")
def submit_code(data: SubmitRequest):
    correct_lines = DEFAULT_CODE.strip().splitlines()
    user_lines = data.user_code.strip().splitlines()

    score = 0
    for i in range(min(len(correct_lines), len(user_lines))):
        if correct_lines[i].strip() == user_lines[i].strip():
            score += 1

    return {
        "success": True,
        "score": score,
        "total": len(correct_lines)
    }