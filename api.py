from fastapi import FastAPI
import logging

app = FastAPI()

@app.get("/")
async def root():
    logging.info("Hello World")
    return {"message": "Hello World"}

@app.get("/introduce")
async def introduce():
    logging.info("Introduce myself")
    return {"안녕하세요. BoB 13기 보안제품개발트랙 김지윤입니다."}