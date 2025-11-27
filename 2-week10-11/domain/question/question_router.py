from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question

# 라우터 객체 생성 및 프리픽스 설정
router = APIRouter(
    prefix='/api/question',
)


@router.get('/list')
def question_list(db: Session = Depends(get_db)):
    '''
    데이터베이스에서 모든 질문 목록을 조회합니다.
    URL: /api/question/list
    '''
    # ORM을 사용하여 Question 모델의 모든 데이터를 조회
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    
    return _question_list