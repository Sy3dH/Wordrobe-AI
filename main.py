from fastapi import FastAPI
from src.routes import crop_avatar_route, create_avatar_route
import src.configs.settings

app = FastAPI(title="Wordrobe AI APIs")

app.include_router(crop_avatar_route.router)
app.include_router(create_avatar_route.router)

@app.get("/")
def root():
    return {"message": "Hi from Wordrobe AI. 👕👖 Let's get you dressed up 👗👘"}
