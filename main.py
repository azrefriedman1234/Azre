
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os, time, threading, requests

app = FastAPI()

PASSWORD = os.getenv("SITE_PASSWORD", "1234")

app.mount("/static", StaticFiles(directory="static"), name="static")

def keep_alive():
    while True:
        try:
            url = os.getenv("RENDER_EXTERNAL_URL")
            if url:
                requests.get(url + "/ping")
        except:
            pass
        time.sleep(40)

threading.Thread(target=keep_alive, daemon=True).start()

@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    if request.cookies.get("auth") != PASSWORD:
        return RedirectResponse("/login")
    return "<h1>Pasiflonet Render</h1><p>Logged in.</p>"

@app.get("/login", response_class=HTMLResponse)
def login():
    return '''
    <form method="post">
        <input type="password" name="pwd" placeholder="Password"/>
        <button>Login</button>
    </form>
    '''

@app.post("/login")
def login_post(pwd: str = Form(...)):
    if pwd == PASSWORD:
        r = RedirectResponse("/", status_code=303)
        r.set_cookie("auth", pwd)
        return r
    return RedirectResponse("/login", status_code=303)
