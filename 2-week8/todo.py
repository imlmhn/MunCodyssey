
# 1. 가상 환경 생성 (Windows)
## python -m venv venv

# 2. 가상 환경 활성화 (Windows)
## venv\Scripts\activate

# 3. 패키지 설치
## pip install fastapi uvicorn

# 4. 서버 실행
## uvicorn todo:app --reload

import csv
import os
from typing import Dict
from fastapi import FastAPI, APIRouter

# FastAPI 애플리케이션 생성
app = FastAPI()
router = APIRouter()

# 전역 리스트 객체 및 CSV 파일명 정의
todo_list = []
CSV_FILENAME = 'todo_list.csv'


def load_from_csv():
    '''
    서버 시작 시 CSV 파일에서 데이터를 읽어 todo_list에 적재합니다.
    '''
    global todo_list
    if not os.path.exists(CSV_FILENAME):
        return

    with open(CSV_FILENAME, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                # CSV에는 값만 저장되어 있다고 가정하고 다시 딕셔너리로 복구
                todo_list.append({'task': row[0]})


def save_to_csv(task_value):
    '''
    새로운 할 일을 CSV 파일에 추가합니다.
    '''
    with open(CSV_FILENAME, mode='a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([task_value])


# 앱 시작 시 기존 데이터 로드
load_from_csv()


@router.post('/add_todo')
async def add_todo(todo: Dict) -> Dict:
    '''
    todo_list에 새로운 항목을 추가하고 CSV에 저장합니다.
    POST 방식입니다.
    보너스 과제: 입력된 Dict가 빈 값이면 경고를 반환합니다.
    '''
    if not todo:
        return {'warning': 'Input data is empty.'}

    # 딕셔너리에 'task' 키가 있다고 가정하거나, 첫 번째 값을 사용
    # 여기서는 범용성을 위해 받은 딕셔너리 자체를 리스트에 추가하고
    # CSV에는 딕셔너리의 값(value)들만 저장하는 방식을 택합니다.
    todo_list.append(todo)
    
    # CSV 저장을 위해 값 추출 (단일 항목 가정)
    values = list(todo.values())
    if values:
        save_to_csv(values[0])

    return {'message': 'Todo added successfully.', 'data': todo}


@router.get('/retrieve_todo')
async def retrieve_todo() -> Dict:
    '''
    todo_list를 가져옵니다.
    GET 방식입니다.
    '''
    return {'todo_list': todo_list}


# APIRouter를 메인 앱에 포함
app.include_router(router)