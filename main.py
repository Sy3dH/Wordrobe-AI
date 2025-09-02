import sys
import torchvision.transforms.functional as F
sys.modules['torchvision.transforms.functional_tensor'] = F
import uvicorn
from fastapi import FastAPI
from src.routes import (crop_avatar_route,
                        create_avatar_route, upscale_avatar_route,
                        validation_avatar_pose, vton_avatar_route)

app = FastAPI(title="Wordrobe AI APIs")

app.include_router(crop_avatar_route.router)
app.include_router(create_avatar_route.router)
app.include_router(validation_avatar_pose.router)
app.include_router(upscale_avatar_route.router)
#app.include_router(vton_avatar_route)

@app.get("/")
def root():
    return {"message": "Hi from Wordrobe AI. 👕👖 Let's get you dressed up 👗👘"}


if __name__ == "__main__":
    uvicorn.run(app, port=8002)