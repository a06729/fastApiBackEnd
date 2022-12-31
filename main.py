from typing import Union

import uuid
from router.fileApi import router as fileRouter
from fastapi import FastAPI,UploadFile
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles


import cv2
import lips

app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")


app.include_router(fileRouter,prefix='/file')

@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, R: Union[str, None] = None,
#              G: Union[str, None] = None,
#              B: Union[str, None] = None):
#     return {"item_id": item_id, "RGB": {'R':R,'G':G,'B':B}}


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile,R: Union[str, None] = None,
#              G: Union[str, None] = None,
#              B: Union[str, None] = None):
    
#     #이미지 파일에 립스틱 색 색칠후 정보 저장하는 객체
#     lipsFileResult={}

#     file_location=f"./{file.filename}"
#     #저장할 파일이름
#     saveFileName=f"{uuid.uuid4()}-{file.filename}"
    
#     with open(file_location,"wb+") as file_object:
#         #원본이미지 파일 저장
#         file_object.write(await file.read())
#         img=cv2.imread(f'./{file.filename}')
#         lipsFileResult=lips.imglips(saveFileName=saveFileName,img=img)

#     return FileResponse(lipsFileResult['fileLocation'], media_type='application/octet-stream',filename=lipsFileResult['fileName'])