from fastapi import FastAPI
from src.routes.routes import router
import src.configs.settings

app = FastAPI(title="Wordrobe AI APIs")
app.include_router(router, prefix="/api", tags=["Avatar creation"])

@app.get("/")
def root():
    return {"message": "Hi from Wordrobe AI. 👕👖 Let's get you dressed up 👗👘"}
