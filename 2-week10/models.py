from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class Question(Base):
    '''
    질문 게시판을 위한 모델 클래스
    '''
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)