from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import system_operator, genco_dashboard, disco_dashboard, market_data, user
from db.db import create_db_and_tables

app = FastAPI(title="Onction Disco dashboard", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(system_operator.router)
app.include_router(genco_dashboard.router)
app.include_router(disco_dashboard.router)
app.include_router(market_data.router)
app.include_router(user.router)


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://onction-dashboard.netlify.app/genco", "*"],  # Adjust this to your frontend's origin in production
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)