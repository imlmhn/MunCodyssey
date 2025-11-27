from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 파일 경로 설정
SQLALCHEMY_DATABASE_URL = 'sqlite:///./myapi.db'

# SQLite는 기본적으로 단일 스레드 통신만 허용하므로,
# FastAPI의 멀티 스레드 환경에서 사용하기 위해 check_same_thread 옵션을 False로 설정
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

# 데이터베이스 세션 생성
# autocommit=False, autoflush=False 로 설정하여 트랜잭션을 수동으로 제어
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 클래스들이 상속받을 Base 클래스 생성
Base = declarative_base()

def get_db():
    '''
    요청마다 DB 세션을 생성하고,
    요청 처리가 끝나면 세션을 종료하는 함수입니다.
    FastAPI의 Depends()로 주입하여 사용합니다.
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()