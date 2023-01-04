from fastapi import FastAPI
from app.routers import auth, company, jobs, users


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(jobs.router)
app.include_router(users.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#routes

@app.get("/")
async def index():
    return {"response": "try different routes"}