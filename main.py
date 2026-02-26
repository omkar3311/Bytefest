from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os
from utility import DEFAULT_CODES

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
    if not data.name.strip():
        return {"success": False, "message": "Name is required"}
    if data.secret_code not in DEFAULT_CODES:
        return {"success": False, "message": "Invalid secret code"}
    
    result = supabase.table("participants").select("code").eq("code", data.secret_code).execute().data
    if result:
        return {
            "success": False,
            "message": "This secret code has already been used"
        }
        
    supabase.table("participants").upsert({
        "name": data.name,
        "code": data.secret_code
    }).execute()
    
    elements = DEFAULT_CODES[data.secret_code].replace("\n", " \n ").split(" ")
    elements = [e for e in elements if e.strip()]

    return {
        "success": True,
        "user_id": data.secret_code,
        "code_elements": elements,
        "time_limit": 120
    }

@app.post("/submit-code")
def submit_code(data: SubmitRequest):
    correct_lines = DEFAULT_CODES[data.secret_code].strip().splitlines()
    user_lines = data.user_code.strip().splitlines()
    
    score = 0
    for i in range(min(len(correct_lines), len(user_lines))):
        if correct_lines[i].strip() == user_lines[i].strip():
            score += 1
    supabase.table("participants").update({
        "score": score
    }).eq("code", data.secret_code).execute()

    return {
        "success": True,
        "score": score,
        "total": len(correct_lines)
    }