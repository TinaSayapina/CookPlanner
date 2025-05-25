from fastapi import FastAPI, Request
from api.recepe_api import recepe_router
from api.users_api import user_router
from database import Base, engine
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(docs_url="/docs")

# HTML шаблоны для фронтэнда
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Homepage html
@app.get("/", response_class=HTMLResponse)
async def homepage(request:Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

# Registration html
@app.get("/register", response_class=HTMLResponse)
async def register(request:Request):
    return templates.TemplateResponse(
        request=request, name="register.html"
    )


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )

# первичная миграция
Base.metadata.create_all(bind=engine)

# регистрируем компонент(роутер)
app.include_router(recepe_router)
app.include_router(user_router)

@app.get("/ok")
async def ok_endpoint():
    return {"message":"Ok"}