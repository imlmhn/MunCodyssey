from pydantic import BaseModel

class TodoItem(BaseModel):
    '''
    Todo 항목을 정의하는 Pydantic 모델입니다.
    '''
    task: str