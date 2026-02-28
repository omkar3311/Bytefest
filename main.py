from fastapi import FastAPI, Request, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os
from utility import DEFAULT_CODES, DEBUG_CODES, QR_DB

load_dotenv()

supabase = create_client(
    os.getenv("supabase_url"),
    os.getenv("supabase_key")
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class LoadRequest(BaseModel):
    name: str
    secret_code: str

class SubmitRequest(BaseModel):
    secret_code: str
    user_code: str
    time_taken: int

class NameRequest(BaseModel):
    full_name: str

class QRScanRequest(BaseModel):
    qr_data: str
    full_name: str

class ResultRequest(BaseModel):
    full_name: str
    result: str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/load-code")
def load_code(data: LoadRequest):
    code = data.secret_code.strip()
    name = data.name.strip()

    if code == "B-000":
        return {"success": True, "redirect": "/admin"}

    if code == "D-000":
        return {"success": True, "redirect": "/admin?mode=debug"}

    if code.startswith("B-") and code in DEFAULT_CODES:
        supabase.table("participant").insert({
            "name": name,
            "code": code,
            "mode": "arrange"
        }).execute()

        elements = DEFAULT_CODES[code].replace("\n", " \n ").split()
        return {
            "success": True,
            "mode": "arrange",
            "user_id": code,
            "code_elements": elements,
            "time_limit": 120
        }

    if code.startswith("D-") and code in DEBUG_CODES:
        supabase.table("participant").insert({
            "name": name,
            "code": code,
            "mode": "debug"
        }).execute()

        return {
            "success": True,
            "mode": "debug",
            "user_id": code,
            "description": DEBUG_CODES[code]["description"],
            "buggy_code": DEBUG_CODES[code]["buggy_code"],
            "time_limit": 120
        }

    return {"success": False, "message": "Invalid secret code"}

def normalize(code: str):
    return [" ".join(l.split()) for l in code.splitlines() if l.strip()]

@app.post("/submit-code")
def submit_code(data: SubmitRequest):
    code = data.secret_code

    if code.startswith("B-"):
        correct = DEFAULT_CODES[code].strip().splitlines()
        user = data.user_code.strip().splitlines()
        score = sum(1 for i in range(min(len(correct), len(user))) if correct[i].strip() == user[i].strip())

        supabase.table("participant").update({
            "B-score": score,
            "B-time": data.time_taken
        }).eq("code", code).execute()

        return {"success": True, "score": score, "total": len(correct)}

    if code.startswith("D-"):
        correct = normalize(DEBUG_CODES[code]["correct_code"])
        user = normalize(data.user_code)
        score = DEBUG_CODES[code]["bugs"]

        for i in range(max(len(correct), len(user))):
            if (correct[i] if i < len(correct) else "") != (user[i] if i < len(user) else ""):
                score -= 1

        score = max(score, 0)

        supabase.table("participant").update({
            "D-score": score,
            "D-time": data.time_taken
        }).eq("code", code).execute()

        return {"success": True, "score": score, "total": DEBUG_CODES[code]["bugs"]}

@app.get("/admin")
def admin_panel(request: Request, mode: str | None = Query(default=None)):
    rows = supabase.table("participant").select("*").execute().data
    rows = [r for r in rows if r["name"]]

    if mode == "debug":
        rows.sort(key=lambda x: ((x["D-score"] or 0), -(x["D-time"] or 9999)), reverse=True)
    elif mode == "arrange":
        rows.sort(key=lambda x: ((x["B-score"] or 0), -(x["B-time"] or 9999)), reverse=True)

    ranked = [{
        "rank": i + 1,
        "name": r["name"],
        "score": r["D-score"] if r["mode"] == "debug" else r["B-score"],
        "time": r["D-time"] if r["mode"] == "debug" else r["B-time"],
        "mode": r["mode"]
    } for i, r in enumerate(rows)]

    return templates.TemplateResponse("admin.html", {
        "request": request,
        "participants": ranked,
        "mode": mode or "all"
    })

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(
    fullname: str = Form(...),
    email: str = Form(...),
    contact: str = Form(...),
    utr: str = Form(...)
):
    supabase.table("participant").insert({
        "name": fullname.strip(),
        "gmail": email.strip().lower(),
        "contact": contact.strip(),
        "fee": utr.strip(),
        "auth": False
    }).execute()

    return {"success": True}

@app.get("/qr-hunt", response_class=HTMLResponse)
def qr_page(request: Request):
    return templates.TemplateResponse("qr_hunt.html", {"request": request})

@app.post("/validate-user")
def validate_user(data: NameRequest):
    print("qr")
    res = supabase.table("participant").select("id").ilike("name", f"%{data.full_name}%").execute()
    return {"status": "ok"} if res.data else {"status": "not_found"}

@app.post("/get-answer")
def get_answer(data: QRScanRequest):
    return {"answer": QR_DB.get(data.qr_data, "")}

@app.post("/submit-result")
def submit_result(data: ResultRequest):
    return {"status": "saved"}