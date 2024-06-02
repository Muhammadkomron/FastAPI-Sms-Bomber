from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from app.admin import create_admin
from app.config import settings
from app.database import init_db
from app.routers import student, user

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include routers
app.include_router(student.router)
app.include_router(user.router)

# Mount static files and templates
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='app/templates')


@app.on_event('startup')
async def on_startup():
    await init_db()
    create_admin(app)


@app.get('/')
async def read_root():
    return {'message': 'Hello World'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
