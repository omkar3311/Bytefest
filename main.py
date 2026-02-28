from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Query
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os
from utility import DEFAULT_CODES,DEBUG_CODES,QR_DB

load_dotenv()
SUPABASE_URL = os.getenv("supabase_url")
SUPABASE_KEY = os.getenv("supabase_key")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)    
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# DEFAULT_CODE = """#include <stdio.h>

# int main() {
#     printf("Hello, Bytefest!");
#     return 0;
# }
# """

class LoadRequest(BaseModel):
    name : str
    secret_code: str

class SubmitRequest(BaseModel):
    secret_code: str
    user_code: str
    time_taken: int
    
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/load-code")
def load_code(data: LoadRequest):
    print("Received:", data)
    if data.secret_code == "B-000":
        return {
            "success": True,
            "redirect": "/admin"
        }
    if data.secret_code == "D-000":
        return {"success": True, "redirect": "/admin?mode=debug"}
    code = data.secret_code.strip()

    if code.startswith("B-"):
        if code not in DEFAULT_CODES:
            return {"success": False, "message": "Invalid secret code"}

        # result = supabase.table("participants") \
        #     .select("code").eq("code", code).execute().data
        # if result:
        #     return {"success": False, "message": "This secret code has already been used"}

        supabase.table("participants").upsert({
            "name": data.name,
            "code": code,
            "mode": "arrange"
        }).execute()

        elements = DEFAULT_CODES[code] \
            .replace("\n", " \n ") \
            .split(" ")
        elements = [e for e in elements if e.strip()]

        return {
            "success": True,
            "mode": "arrange",
            "user_id": code,
            "code_elements": elements,
            "time_limit": 120
        }

    if code.startswith("D-"):
        if code not in DEBUG_CODES:
            return {"success": False, "message": "Invalid secret code"}

        # result = supabase.table("participants") \
        #     .select("code").eq("code", code).execute().data
        # if result:
        #     return {"success": False, "message": "This secret code has already been used"}

        supabase.table("participants").upsert({
            "name": data.name,
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

    return {"success": False, "message": "Invalid secret code format"}

def normalize_lines(code: str):
    return [
        " ".join(line.strip().split())
        for line in code.splitlines()
        if line.strip()
    ]
    
@app.post("/submit-code")
def submit_code(data: SubmitRequest):

    code = data.secret_code

    if code.startswith("B-"):
        correct_lines = DEFAULT_CODES[code].strip().splitlines()
        user_lines = data.user_code.strip().splitlines()

        score = 0
        for i in range(min(len(correct_lines), len(user_lines))):
            if correct_lines[i].strip() == user_lines[i].strip():
                score += 1

        total = len(correct_lines)

    elif code.startswith("D-"):
        correct_lines = normalize_lines(DEBUG_CODES[code]["correct_code"])
        user_lines = normalize_lines(data.user_code)

        bugs = DEBUG_CODES[code]["bugs"]
        score = bugs  

        max_lines = max(len(correct_lines), len(user_lines))

        for i in range(max_lines):
            correct_line = correct_lines[i] if i < len(correct_lines) else ""
            user_line = user_lines[i] if i < len(user_lines) else ""

            if correct_line != user_line:
                score -= 1

        score = max(score, 0)
        total = bugs

    supabase.table("participants").update({
        "score": score,
        "time": data.time_taken
    }).eq("code", code).execute()

    return {
        "success": True,
        "score": score,
        "total": total
    }
    
@app.get("/admin")
def admin_panel(request: Request, mode: str | None = Query(default=None)):

    query = supabase.table("participants") \
        .select("name, score, time, mode")

    if mode:
        query = query.eq("mode", mode)

    data = query.execute().data
    data = [d for d in data if d["name"]]

    data.sort(
        key=lambda x: (
            x["score"] if x["score"] is not None else 0,
            x["time"] if x["time"] is not None else 0
        ),
        reverse=True
    )

    ranked = []
    for i, d in enumerate(data, start=1):
        ranked.append({
            "rank": i,
            "name": d["name"],
            "score": d["score"] or 0,
            "time": d["time"] or 0,
            "mode": d["mode"]
        })

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "participants": ranked,
            "mode": mode or "all"
        }
    )
    
    
    
# ------------------------------------------------------------------------------

TABLE_NAME = "us"

def user_exists(contact: str) -> bool:
    response = (
        supabase.table(TABLE_NAME)
        .select("contact_number")
        .eq("contact_number", contact)
        .execute()
    )
    return len(response.data) > 0

@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
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

UPLOAD_DIR = "uploaded_img"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/register")
async def register_user(
    fullname: str = Form(...),
    email: str = Form(...),
    contact: str = Form(...),
    college: str = Form(...),
    payment_img: UploadFile = File(...)
):
    email = email.strip().lower()

    if not email.endswith("@gmail.com"):
        return {"success": False, "message": "Email must be Gmail"}

    if not contact.isdigit() or len(contact) != 10:
        return {"success": False, "message": "Invalid contact number"}

    ext = payment_img.filename.split(".")[-1]
    filename = f"{fullname.replace(' ','_')}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path,"wb") as f:
        f.write(await payment_img.read())

    return {"success": True}

    # if user_exists(contact):
    #     return {"success": False, "message": "User already registered"}

    # supabase.table(TABLE_NAME).insert({
    #     "full_name": fullname,
    #     "email": email,
    #     "contact_number": contact,
    #     "college_name": college
    # }).execute()



# ---------------------------------------------------------------------------------------

class QRScanRequest(BaseModel):
    qr_data: str
    full_name: str

class ResultRequest(BaseModel):
    full_name: str
    result: str

class NameRequest(BaseModel): 
    full_name: str

@app.get("/qr-hunt", response_class=HTMLResponse)
def serve_page(request: Request):
    return templates.TemplateResponse(
        "qr_hunt.html",
        {"request": request}
    )

@app.post("/validate-user")
def validate_user(data: NameRequest):
    name = data.full_name.strip()
    res = (
        supabase
        .table("participants")
        .select("id")
        .ilike("name", name)
        .execute()
    )
    print(res.data)
    if res.data:
        return {"status": "ok"}
    return {"status": "not_found"}

@app.post("/get-answer")
def get_answer(data: QRScanRequest):
    return {"answer": QR_DB.get(data.qr_data, "")}

@app.post("/submit-result")
def submit_result(data: ResultRequest):
    # supabase.table("participants").update({
    #     "round1": data.result
    # }).eq("full_name", data.full_name).execute()
    return {"status": "saved"}