from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src import models
from src.crud_tools import schemas_answer

# from src.logger import logger


def get_answer(db: Session, answer_id: int):
    return db.query(models.Answer).filter_by(id=answer_id).first()


def get_answers(
    db: Session, skip: int = 0, limit: int = 10, trained: int = 0
) -> List[models.Answer]:
    if trained != 0:
        return (
            db.query(models.Answer)
            .filter(models.Answer.already_trained == (trained == 1))
            .all()
        )
    return db.query(models.Answer).offset(skip).limit(limit).all()


def create_answer(db: Session, answer: schemas_answer.AnswerCreate):
    try:
        db_answer = models.Answer(**answer.model_dump())
        db.add(db_answer)
        db.commit()
        db.refresh(db_answer)
    except IntegrityError as e:
        db.rollback()
        raise e
    return db_answer


def create_answers(db: Session, answers: List[schemas_answer.AnswerCreate]):
    try:
        db_answers = [models.Answer(**answer.model_dump()) for answer in answers]
        db.add_all(db_answers)
        db.commit()
        for answer in db_answers:
            db.refresh(answer)
    except IntegrityError as e:
        db.rollback()
        raise e
    return db_answers


def update_answer(
    db: Session,
    answer_id: int,
    answer: schemas_answer.AnswerUpdate,
):
    db_answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    for key, value in answer.model_dump().items():
        setattr(db_answer, key, value)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def delete_answer(db: Session, answer_id: int):
    db_answer = db.query(models.Answer).filter_by(id=answer_id).first()
    db.delete(db_answer)
    db.commit()
