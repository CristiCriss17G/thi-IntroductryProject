from typing import List, Optional

from pydantic import BaseModel


class AnswerBase(BaseModel):
    answer: str
    tags: List[str]


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    already_trained: Optional[bool] = None


class Answer(AnswerBase):
    id: int
    already_trained: bool = False

    class Config:
        # orm_mode = True
        from_attributes = True


Answer.model_rebuild()
