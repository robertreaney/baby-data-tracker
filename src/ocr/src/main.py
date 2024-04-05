from fastapi import FastAPI, File, UploadFile
import uvicorn
import logging
import os
from pathlib import Path
import json

from objects import response_model
from ocr import main

LOGLEVEL = os.getenv('LOGLEVEL')
logging.basicConfig(level=logging.getLevelName(LOGLEVEL), format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

####################
app = FastAPI()

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc: HTTPException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content=jsonable_encoder(response_model(message=str(exc.detail), errors=[{"detail": exc.detail}], status="error")),
#     )
@app.get('/')
def root():
    return {'hello': "world"}

@app.get("/health_check")
def health_check():
    return response_model(message="API is healthy!")

@app.post("/files")
async def upload_image(file: UploadFile = File(...)):

    contents = await file.read()
    
    try:
        # inspect contents object whenever you get here
        main(contents, content_type = file.content_type)
    except Exception as e:
        return response_model(status='failed', message=f'{e}')

    return response_model('processed file')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)