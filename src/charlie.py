from __future__ import annotations

from typing import Union

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from decouple import config
from sqlalchemy.orm import Session

from .crud_tools import answer as answer_crud
from .crud_tools import settings
from .crud_tools.schemas_answer import AnswerUpdate
from .models import Answer
from .perm_train import PermTrain

chatbot: Union[ChatBot, None] = None
permtrain: Union[PermTrain, None] = None


def init():
    global chatbot

    chatbot = ChatBot(
        "Charlie",
        storage_apadter="chatterbot.storage.SQLStorageAdapter",
        database_uri=config("DATABASE_URL"),
        logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            "chatterbot.logic.BestMatch",
            "chatterbot.logic.TimeLogicAdapter",
        ],
    )

    if settings.get_settings("first_training") == None:
        trainer = ChatterBotCorpusTrainer(chatbot)

        trainer.train("chatterbot.corpus.english")

        trainer = ListTrainer(chatbot)

        trainer.train(
            [
                "Hi!",
                "Hey there!",
            ]
        )

        trainer.train(
            ["Tell me about THI", "THI is a university in Ingolstadt, Germany."]
        )

        settings.set_settings("first_training", "done")


def train_db(conversations: list[list[str]]):
    global chatbot

    if chatbot == None:
        init()

    trainer = ListTrainer(chatbot)

    for conversation in conversations:
        trainer.train(conversation)


def mark_answer_as_trained(db: Session, answer_id: int, answer: Answer):
    answer.already_trained = True
    answer_update = AnswerUpdate(**answer.__dict__)
    return answer_crud.update_answer(db, answer_id, answer_update)


def init_db_permutation_training(
    db: Session,
    method: str = "simple",
    limit: int = -1,
    batch_size: int = 100,
    max_threads: int = 5,
):
    global permtrain
    permtrain = PermTrain(
        db,
        train_db,
        mark_answer_as_trained,
        method=method,
        limit=limit,
        batch_size=batch_size,
        max_threads=max_threads,
    )

    return permtrain.prepare_conversations()


def start_train():
    # asyncio.run(permtrain.tag_db_permutation_training())
    permtrain.tag_db_permutation_training_multiprocess()


def get_answer(question):
    global chatbot

    if chatbot == None:
        init()
    response = chatbot.get_response(question)
    return response.text
