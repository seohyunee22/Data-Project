# 학습결과 저장관련 라이브러리
import pickle
import joblib

# 데이터 처리 라이브러리
import pandas as pd
import numpy as np

# 서빙모델 차이점 시작
# 서빙모델 서버 라이브러리
import uvicorn

# 데이터 연계 라이브러리
from fastapi import FastAPI
from pydantic import BaseModel

# 예시 Pydantic 모델
class InDataset(BaseModel):
    Founded_Year: int
    Country: str
    Industry: str
    Investment_Stage: float
    Employees: int
    Acquired_Status: int
    IPO_Status: int
    Customers: float
    Total_Investment: float
    Annual_Revenue: float
    SNS_Followers: float
    Company_Value: float

# 모델 로드
with open("model.dump", "rb") as fr:
    loaded_Model = pickle.load(fr)

# 보안 상의 이유로 CORS 해제
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ML API")

# CORS 설정 (모든 출처에 대해 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 예측 API 엔드포인트
@app.post("/predictBase", status_code=200)
async def predict_tf(x: InDataset):
    try:
        # 입력값을 DataFrame으로 변환 (순서대로 맞춰줌)
        inDf = pd.DataFrame([[
            x.Founded_Year,  # 설립연도
            x.Country,  # 국가
            x.Industry,  # 분야
            x.Investment_Stage,  # 투자단계
            x.Employees,  # 직원 수
            x.Acquired_Status,  # 인수여부
            x.IPO_Status,  # 상장여부
            x.Customers,  # 고객수(백만명)
            x.Total_Investment,  # 총 투자금(억원)
            x.Annual_Revenue,  # 연매출(억원)
            x.SNS_Followers,  # SNS 팔로워 수(백만명)
            x.Company_Value  # 기업가치(백억원)
        ]], columns=[
            'Founded_Year',
            'Country',
            'Industry',
            'Investment_Stage',
            'Employees',
            'Acquired_Status',
            'IPO_Status',
            'Customers',
            'Total_Investment',
            'Annual_Revenue',
            'SNS_Followers',
            'Company_Value'
        ])

        # 예측 수행
        groupKey = (x.Country, x.Industry)
        try:
            features, label, exact_model = loaded_Model[groupKey]
            input_data = pd.DataFrame(inDf.loc[:, features], columns=features)
            prediction = exact_model.predict(input_data)[0]

            return {"predictValue": float(prediction)}
        except:
            return {"error": "Prediction not available due to lack of sufficient data."}

    except Exception as e:
        return {"error": str(e)}

# 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "Online"}

# 서버 실행
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9999, log_level="debug", proxy_headers=True, reload=True)
