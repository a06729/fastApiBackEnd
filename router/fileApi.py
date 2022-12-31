import os
from fastapi import APIRouter
from fastapi import UploadFile,status,HTTPException
from dotenv import load_dotenv
from typing import Union
from starlette.responses import FileResponse
from loguru import logger


import cv2
import lips
import uuid

router = APIRouter()

#원본이미지 상대경로
re_Image_path='./images/'
#원본이미지 절대경로
ab_Image_path='/images/'

#.env 값을 가져오기위한 코드
#os.pardir은 상위경로의 값을 가져온다.
BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


#원본파일 이미지 저장
@router.post("/uploadImage")
async def uploadImage(file: UploadFile,status_code=status.HTTP_201_CREATED):
    
    #호스트이름 .env 파일에서 HOST_NAME 키값으로 가져온다.
    host_name= os.environ["HOST_NAME"]
    #원본파일 이름 뒤에 uuid를 넣어서 파일이름 겹치는걸 방지
    file_name=f'{uuid.uuid4()}-{file.filename}'
    
    #원본이미지 저장할 위치 변수
    # file_location=fr"{re_Image_path}{file_name}"
    file_location=os.path.join(re_Image_path,file_name)
    
    logger.info(file_location)
    
    with open(file_location,"wb") as file_object:
        file_object.write(await file.read())
    
    return {
        'status_code':status_code,#http 상태값 리턴
        're_file_location':file_location,#파일이미지 상대경로
        'fileName':file_name,
        "imgUrl":f'{host_name}{ab_Image_path}{file_name}'#이미지 파일 위치 리턴
    }
#원본이미지 립스틱 색 칠하는 라우터
@router.post("/ImageLips")
async def ImageLips(
             imageName:Union[str, None] = None,
             B: Union[int, None] = None,
             G: Union[int, None] = None,
             R: Union[int, None] = None):
    
    #이미지 파일에 립스틱 색 색칠후 정보 저장하는 객체
    lipsFileResult={}
    
    #오리지널 이미지 위치
    imagePath=f'{os.path.join(BASE_DIR,"images")}/{imageName}'
    #립스틱 색칠한 이미지저장 위치
    lipsImagePath=f'{os.path.join(BASE_DIR,"lipsImages/")}'
    
    #저장할 파일이름
    saveFileName=f"{uuid.uuid4()}-{imageName}"
    
    logger.debug(imagePath)
    logger.debug(lipsImagePath)
    
    #이미지를 opencv로 읽어온다.
    img=cv2.imread(imagePath)
    #이미지처리한 결과값 딕셔너리 객체로 정보를 리턴해 준다.
    lipsFileResult=lips.imglips(saveFileName=saveFileName,img=img,savePath=lipsImagePath)

    #이미지에 얼굴을 인식하면 status값이 True로 리턴된다.
    if lipsFileResult['status']==True:
        return FileResponse(lipsFileResult['fileLocation'], media_type='application/octet-stream',filename=lipsFileResult['fileName'])
    else:
        logger.info("이미지에서 얼굴을 찾을수 없습니다.")
        raise HTTPException(status_code=404, detail="이미지에서 얼굴을 찾을수 없습니다.")