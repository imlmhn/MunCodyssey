import csv
import os
from fastapi import FastAPI, APIRouter, HTTPException, Path
from model import TodoItem

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
    todo_list.clear()
    if not os.path.exists(CSV_FILENAME):
        return

    with open(CSV_FILENAME, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                todo_list.append(TodoItem(task=row[0]))


def save_all_to_csv():
    '''
    현재 메모리에 있는 todo_list 전체를 CSV 파일에 덮어씁니다.
    수정이나 삭제 시 호출됩니다.
    '''
    with open(CSV_FILENAME, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for item in todo_list:
            writer.writerow([item.task])


# 앱 시작 시 기존 데이터 로드
load_from_csv()


@router.post('/add_todo')
async def add_todo(todo: TodoItem) -> dict:
    '''
    todo_list에 새로운 항목을 추가합니다. (POST)
    '''
    todo_list.append(todo)
    
    # 추가는 끝에 붙이기만 하면 되므로 append 모드 사용 가능하지만
    # 일관성을 위해 전체 저장 함수를 사용하거나, 성능을 위해 append만 할 수도 있습니다.
    # 여기서는 안전하게 전체 저장을 호출합니다.
    save_all_to_csv()
    
    return {'message': 'Todo added successfully.', 'data': todo}


@router.get('/retrieve_todo')
async def retrieve_todo() -> dict:
    '''
    전체 todo_list를 가져옵니다. (GET)
    '''
    return {'todo_list': todo_list}


@router.get('/todo/{todo_id}')
async def get_single_todo(todo_id: int = Path(..., title='The ID of the todo to retrieve')) -> dict:
    '''
    ID(인덱스)를 통해 개별 Todo를 조회합니다. (GET)
    '''
    if todo_id < 0 or todo_id >= len(todo_list):
        raise HTTPException(status_code=404, detail='Todo not found')
    
    return {'todo_id': todo_id, 'todo': todo_list[todo_id]}


@router.put('/update_todo/{todo_id}')
async def update_todo(todo: TodoItem, todo_id: int = Path(..., title='The ID of the todo to update')) -> dict:
    '''
    ID(인덱스)를 통해 특정 Todo를 수정합니다. (PUT)
    '''
    if todo_id < 0 or todo_id >= len(todo_list):
        raise HTTPException(status_code=404, detail='Todo not found')
    
    # 리스트 업데이트
    todo_list[todo_id] = todo
    
    # 변경된 내용을 CSV에 반영
    save_all_to_csv()
    
    return {'message': 'Todo updated successfully.', 'todo_id': todo_id, 'data': todo}


@router.delete('/delete_single_todo/{todo_id}')
async def delete_single_todo(todo_id: int = Path(..., title='The ID of the todo to delete')) -> dict:
    '''
    ID(인덱스)를 통해 특정 Todo를 삭제합니다. (DELETE)
    '''
    if todo_id < 0 or todo_id >= len(todo_list):
        raise HTTPException(status_code=404, detail='Todo not found')
    
    # 리스트에서 삭제 (pop은 삭제된 항목을 반환함)
    deleted_item = todo_list.pop(todo_id)
    
    # 변경된 내용을 CSV에 반영
    save_all_to_csv()
    
    return {'message': 'Todo deleted successfully.', 'deleted_data': deleted_item}


app.include_router(router)