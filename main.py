from router.fileApi import router as fileRouter
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


# import uuid
# import cv2
# import lips


def dirCreate():
    try:
        if not os.path.exists('images'):
            os.makedirs('images')
        if not os.path.exists('lipsImages'):
            os.makedirs('lipsImages')
    except OSError:
        print ('Error: Creating directory.')
        
#프로그램 시작전 폴더생성
dirCreate()


load_dotenv()
#.env의 HOST_NAEM 값 가져옴
HOST_NAME=os.environ.get('HOST_NAME')

app = FastAPI()

#파일 접근 가능하도록 추가
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/lipsImages", StaticFiles(directory="lipsImages"), name="lipsImages")


#api 라우터 추가
app.include_router(fileRouter,prefix='/file')

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
     HOST_NAME
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

        
