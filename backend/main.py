from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import game_routes, ws_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_routes.router, prefix="/api")
app.include_router(ws_routes.router)   # this mounts /ws/<id>

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}
