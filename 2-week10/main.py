from fastapi import FastAPI
from domain.question import question_router

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Welcome to Mars Bulletin Board System'}

app.include_router(question_router.router)