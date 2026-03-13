import sys
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from fastapi import FastAPI, Request, Form, Query, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client
# from dotenv import load_dotenv

import os
import qrcode
import re
import random
import uuid
import smtplib
from email.message import EmailMessage

from utility import DEFAULT_CODES, DEBUG_CODES, QR_DB, QR_GAME

# load_dotenv()


SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(subject, body, to):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = to
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print("demo")
        print("Email sent to", to)

    except Exception as e:
        print("Email error:", e)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

class LoadRequest(BaseModel):
    name: str
    secret_code: str

class SubmitRequest(BaseModel):
    gmail : str
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
        return {"success": True, "redirect": "/admin?mode=arrange"}

    if code == "D-000":
        return {"success": True, "redirect": "/admin?mode=debug"}

    if code.startswith("B-") and code in DEFAULT_CODES:
        res = supabase.table("participant").select("auth").eq("gmail", data.name.lower()).execute()
        if not res.data:
            return {"success": False, "message": " User not found"}

        if res.data[0]["auth"] is False:
            return {"success": False, "message": "User Not Approved"}

        # elements = DEFAULT_CODES[code].replace("\n", " \n ").split()
        elements = DEFAULT_CODES[code].splitlines()
        return {
            "success": True,
            "mode": "arrange",
            "user_id": code,
            "code_elements": elements,
            "time_limit": 120
        }

    if code.startswith("D-") and code in DEBUG_CODES:
        res = supabase.table("participant").select("auth").eq("gmail", data.name.lower()).execute()
        if not res.data:
            return {"status": "not_found"}

        if res.data[0]["auth"] is False:
            return {"success": False, "message": "Not Approved"}

        return {
            "success": True,
            "mode": "debug",
            "user_id": code,
            "description": DEBUG_CODES[code]["description"],
            "buggy_code": DEBUG_CODES[code]["buggy_code"],
            "time_limit": 120
        }

    return {"success": False, "message": "Invalid secret code"}
def normalize_lines(code: str):
    normalized = []
    for line in code.splitlines():
        if not line.strip():
            continue
        line = line.replace(",", " , ").replace(";", " ; ")
        line = " ".join(line.split())
        line = line.replace(" ,", ",").replace(" ;", ";")
        normalized.append(line)
    return normalized
def normalize(code: str):
    return [" ".join(l.split()) for l in code.splitlines() if l.strip()]

@app.post("/submit-code")
def submit_code(data: SubmitRequest):
    code = data.secret_code
    gmail = data.gmail
    
    if code.startswith("B-"):
        correct_raw = DEFAULT_CODES[code]
        user_raw = data.user_code

        correct = normalize_lines(correct_raw)
        user = normalize_lines(user_raw)

        score = 0
        results = []

        for i in range(len(correct)):
            user_line = user[i] if i < len(user) else ""
            correct_line = correct[i]

            is_correct = user_line == correct_line
            if is_correct:
                score += 1

            results.append({
                "line_no": i + 1,
                "correct": correct_line,
                "user": user_line,
                "is_correct": is_correct
            })

        supabase.table("participant").update({
            "mode": "arrange",
            "code": code,
            "B-score": score,
            "B-time": data.time_taken
        }).eq("gmail", gmail).execute()

        return {
            "success": True,
            "score": score,
            "total": len(correct),
            "correct_code": correct,
            "lines": results
        }

    if code.startswith("D-"):
        correct = normalize(DEBUG_CODES[code]["correct_code"])
        user = normalize(data.user_code)
        max_score = DEBUG_CODES[code]["bugs"]
        results = []
        for i in range(max(len(correct), len(user))):
            if (correct[i] if i < len(correct) else "") != (user[i] if i < len(user) else ""):
                max_score -= 1

        max_score = max(max_score, 0)
        score = 0 
        for i in range(len(correct)):
            user_line = user[i] if i < len(user) else ""
            correct_line = correct[i]

            is_correct = user_line == correct_line
            if is_correct:
                score += 1

            results.append({
                "line_no": i + 1,
                "correct": correct_line,
                "user": user_line,
                "is_correct": is_correct
            })
        supabase.table("participant").update({
            "mode": "debug",
            "code" : code,
            "D-score": score,
            "D-time": data.time_taken
        }).eq("gmail", gmail).execute()

        return {"success": True,
                "score": max_score, 
                "total": DEBUG_CODES[code]["bugs"],
                "correct_code": correct,
                "lines": results
                }

@app.get("/admin")
def admin_panel(request: Request, mode: str | None = Query(default=None)):
    if mode == "arrange":
        rows = (
            supabase
            .table("participant")
            .select("name, mode, B-score, B-time")
            .eq("mode", "arrange")
            .order("B-score", desc=True)
            .order("B-time", desc=True)
            .execute()
            .data
        )

        ranked = [
            {
                "rank": i + 1,
                "name": r["name"],
                "score": r["B-score"],
                "time": r["B-time"],
                "mode": "arrange"
            }
            for i, r in enumerate(rows)
        ]

        return templates.TemplateResponse(
            "admin.html",
            {
                "request": request,
                "participants": ranked,
                "mode": "arrange"
            }
        )
        
    if mode == "debug":
        rows = (
            supabase
            .table("participant")
            .select("name, mode, D-score, D-time")
            .eq("mode", "debug")
            .order("D-score", desc=True)
            .order("D-time", desc=True)
            .execute()
            .data
        )

        ranked = [
            {
                "rank": i + 1,
                "name": r["name"],
                "score": r["D-score"],
                "time": r["D-time"],
                "mode": "debug"
            }
            for i, r in enumerate(rows)
        ]

        return templates.TemplateResponse(
            "admin.html",
            {
                "request": request,
                "participants": ranked,
                "mode": "debug"
            }
        )

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

BUCKET = "filestore"

@app.post("/register")
async def register_user(
    fullname: str = Form(...),
    email: str = Form(...),
    contact: str = Form(...),
    college: str = Form(...),
    payment_proof: UploadFile = File(...)
):
    if payment_proof.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return {"success": False, "message": "Invalid file type"}

    username = re.sub(r"[^a-zA-Z0-9]", "_", fullname.strip().lower())
    ext = payment_proof.filename.split(".")[-1]
    filename = f"{username}.{ext}"
    path = f"register/{filename}"

    supabase.storage.from_(BUCKET).upload(
        path,
        await payment_proof.read(),
        {"content-type": payment_proof.content_type}
    )

    file_url = supabase.storage.from_(BUCKET).get_public_url(path)

    supabase.table("participant").insert({
        "name": fullname.strip(),
        "gmail": email.strip().lower(),
        "contact": contact.strip(),
        "fee": file_url,
        "auth": False
    }).execute()
    send_email(
    "ByteFest Registration Received",
    f"""
Hello {fullname},

Your registration for ByteFest 2026 has been received.

Your application is currently under review.
Once approved, you will be able to participate in the event.

Thank you for registering!

Team ByteFest
""",
    email
)
    return {"success": True}

@app.get("/qr-hunt", response_class=HTMLResponse)
def qr_page(request: Request):
    return templates.TemplateResponse("qr_hunt.html", {"request": request})

@app.post("/validate-user")
def validate_user(data: NameRequest):
    res = supabase.table("participant") \
        .select("auth, round1") \
        .eq("gmail", data.full_name.lower()) \
        .execute()

    if not res.data:
        return {"status": "not_found"}

    user = res.data[0]

    if user["auth"] is True and user["round1"] is True:
        return {"status": "ok"}

    return {"status": "pending"} 

@app.post("/get-answer")
def get_answer(data: QRScanRequest):
    round_key = data.qr_data

    if round_key not in QR_GAME:
        return {"error": "invalid_qr"}

    round_data = QR_GAME[round_key]
    question = random.choice(round_data["questions"])

    return {
        "question": question["q"],
        "answer": question["a"],
        "destination": round_data["destination"],
        "is_last_round": round_key == "round_3"
    }

@app.post("/submit-result")
def submit_result(data: ResultRequest):
    if data.result == "fail":
        supabase.table("participant") \
            .update({"round1": False}) \
            .eq("gmail", data.full_name.lower()) \
            .execute()

        return {"status": "failed"}

    return {"status": "passed"}

@app.get("/approve")
def approve_get(request: Request):
    rows = (
        supabase
        .table("participant")
        .select("id, name, gmail, fee, auth")
        .order("id", desc=True)
        .execute()
        .data
    )

    return templates.TemplateResponse(
        "approve.html",
        {"request": request, "users": rows}
    )

@app.post("/approve")
def approve_post(
    user_id: int = Form(...),
    action: str = Form(...)
):
    user = (
        supabase
        .table("participant")
        .select("name, gmail")
        .eq("id", user_id)
        .single()
        .execute()
        .data
    )
    if action == "approve":
        supabase.table("participant") \
            .update({"auth": True}) \
            .eq("id", user_id) \
            .execute()
        send_email(
            "ByteFest Registration Approved 🎉",
            f"""
Hello {user['name']},

Your registration for ByteFest has been approved.

You can now participate in the event.

Good luck and see you at ByteFest!

Team ByteFest
""",
            user["gmail"]
        )

    elif action == "decline":
        supabase.table("participant") \
            .delete() \
            .eq("id", user_id) \
            .execute()

    return RedirectResponse("/approve", status_code=303)

QR_DIR = BASE_DIR / "static" / "qr"
os.makedirs(QR_DIR, exist_ok=True)

@app.get("/generate", response_class=HTMLResponse)
def generate_page(request: Request):
    return templates.TemplateResponse("qr_genrator.html", {
        "request": request,
        "qr_path": None
    })


@app.post("/generate", response_class=HTMLResponse)
def generate_qr(request: Request, question: str = Form(...)):
    filename = f"{uuid.uuid4()}.png"
    file_path = QR_DIR / filename

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr.add_data(question)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(str(file_path))

    return templates.TemplateResponse("qr_genrator.html", {
        "request": request,
        "qr_path": f"/static/qr/{filename}"
    })


@app.get("/download/{filename}")
def download_qr(filename: str):
    return FileResponse(
        path=str(QR_DIR / filename),
        media_type="image/png",
        filename="qr_code.png"
    )
