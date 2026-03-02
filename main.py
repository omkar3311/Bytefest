from fastapi import FastAPI, Request, Form, Query, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os
import qrcode
import re
import uuid
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
            return {"status": "not_found"}

        if res.data[0]["auth"] is False:
            return {"success": False, "message": "Not Approved"}

        elements = DEFAULT_CODES[code].replace("\n", " \n ").split()
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

def normalize(code: str):
    return [" ".join(l.split()) for l in code.splitlines() if l.strip()]

@app.post("/submit-code")
def submit_code(data: SubmitRequest):
    code = data.secret_code
    gmail = data.gmail

    if code.startswith("B-"):
        correct = DEFAULT_CODES[code].strip().splitlines()
        user = data.user_code.strip().splitlines()
        score = sum(1 for i in range(min(len(correct), len(user))) if correct[i].strip() == user[i].strip())

        supabase.table("participant").update({
            "mode": "arrange",
            "code" : code,
            "B-score": score,
            "B-time": data.time_taken
        }).eq("gmail", gmail).execute()

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
            "mode": "debug",
            "code" : code,
            "D-score": score,
            "D-time": data.time_taken
        }).eq("gmail", gmail).execute()

        return {"success": True, "score": score, "total": DEBUG_CODES[code]["bugs"]}

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

    return {"success": True}

@app.get("/qr-hunt", response_class=HTMLResponse)
def qr_page(request: Request):
    return templates.TemplateResponse("qr_hunt.html", {"request": request})

@app.post("/validate-user")
def validate_user(data: NameRequest):
    res = supabase.table("participant").select("auth").eq("gmail", data.full_name.lower()).execute()
    print(res)
    if not res.data:
        return {"status": "not_found"}

    if res.data[0]["auth"] is True:
        return {"status": "ok"}

    return {"status": "pending"}

@app.post("/get-answer")
def get_answer(data: QRScanRequest):
    return {"answer": QR_DB.get(data.qr_data, "")}

@app.post("/submit-result")
def submit_result(data: ResultRequest):
    return {"status": "saved"}

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
    if action == "approve":
        supabase.table("participant") \
            .update({"auth": True}) \
            .eq("id", user_id) \
            .execute()

    elif action == "decline":
        supabase.table("participant") \
            .delete() \
            .eq("id", user_id) \
            .execute()

    return RedirectResponse("/approve", status_code=303)

QR_DIR = "static/qr"
os.makedirs(QR_DIR, exist_ok=True)

@app.get("/generate", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("qr_genrator.html", {
        "request": request,
        "qr_path": None
    })


@app.post("/generate", response_class=HTMLResponse)
def generate_qr(request: Request, question: str = Form(...)):
    filename = f"{uuid.uuid4()}.png"
    file_path = f"{QR_DIR}/{filename}"

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )
    qr.add_data(question)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

    return templates.TemplateResponse("qr_genrator.html", {
        "request": request,
        "qr_path": f"/static/qr/{filename}"
    })


@app.get("/download/{filename}")
def download_qr(filename: str):
    return FileResponse(
        path=f"{QR_DIR}/{filename}",
        media_type="image/png",
        filename="qr_code.png"
    )