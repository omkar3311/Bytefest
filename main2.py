from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import csv
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

FILE_NAME = "users.csv"

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["Full Name", "Contact Number", "College Name"])

def user_exists(contact):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return any(row["Contact Number"] == contact for row in csv.DictReader(f))

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    success = request.query_params.get("success")
    error = request.query_params.get("error")
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "success": success == "1",
            "error": error
        }
    )

@app.post("/")
async def register(
    fullname: str = Form(...),
    contact: str = Form(...),
    college: str = Form(...)
):
    if not contact.isdigit() or len(contact) != 10:
        return RedirectResponse(
            url="/?error=Contact must be exactly 10 digits",
            status_code=303
        )

    if user_exists(contact):
        return RedirectResponse(
            url="/?error=User already registered",
            status_code=303
        )

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([fullname, contact, college])

    return RedirectResponse(url="/?success=1", status_code=303)