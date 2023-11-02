from typing import List

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import charlie, healthcheck
from .charlie import init_db_permutation_training, start_train
from .crud_tools import answer as answer_crud
from .crud_tools import schemas_answer
from .database import get_db
from .healthcheck import init_healthcheck

app = FastAPI()

init_healthcheck()

charlie.init()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

app.include_router(healthcheck.router)


@app.get("/")
async def index():
    return "Flask Server is alive!"


@app.get("/chat")
async def chat(question: str):
    if question:
        answer = charlie.get_answer(question)
        return answer
    else:
        return "question parameter is missing"


@app.get("/answers/", response_model=List[schemas_answer.Answer])
async def read_answers(
    skip: int = 0, limit: int = 10, trained: int = 0, db: Session = Depends(get_db)
):
    answers = answer_crud.get_answers(db, skip=skip, limit=limit, trained=trained)
    return answers


@app.post("/answers/", response_model=List[schemas_answer.Answer])
async def create_answers(
    answers: List[schemas_answer.AnswerCreate], db: Session = Depends(get_db)
):
    try:
        db_answers = answer_crud.create_answers(db, answers)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Answer already exists"
        )
    return db_answers


@app.post("/train/simple")
async def train_simple(
    background_tasks: BackgroundTasks,
    method: str = "simple",
    limit: int = -1,
    batch_size: int = 100,
    max_threads: int = 5,
    db: Session = Depends(get_db),
):
    conversations_no = init_db_permutation_training(
        db, method=method, limit=limit, batch_size=batch_size, max_threads=max_threads
    )
    background_tasks.add_task(start_train)

    return f"Training started with {conversations_no} conversations"
