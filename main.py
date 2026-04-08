import sys
import torchvision.transforms.functional as F
sys.modules['torchvision.transforms.functional_tensor'] = F
import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routes import (
                        # crop_avatar_route,
                        # create_avatar_route,
                        # upscale_avatar_route,
                        # validation_avatar_pose,
                        # ai_scoring_route,
                        # status_route,
                        chat_route)
                        #vton_avatar_route)


app = FastAPI(title="Wordrobe AI APIs")
output_dir = os.path.join(os.path.dirname(__file__), "src", "output")
#
# app.include_router(crop_avatar_route.router, prefix="/avatar-onboarding")
# app.include_router(create_avatar_route.router, prefix="/avatar-onboarding")
# app.include_router(validation_avatar_pose.router, prefix="/avatar-validation")
# app.include_router(upscale_avatar_route.router, prefix="/post-processing")
# app.include_router(vton_avatar_route.router, prefix="/AI")
app.include_router(chat_route.router, prefix="/AI")
# app.include_router(ai_scoring_route.router, prefix="/AI")
# app.include_router(status_route.router, prefix="/status")

app.mount("/output", StaticFiles(directory=output_dir), name="output")

@app.get("/")
def root():
    return {"message": "Hi from Wordrobe AI. 👕👖 Let's get you dressed up 👗👘"}


if __name__ == "__main__":
    uvicorn.run(app, port=8002)