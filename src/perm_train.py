from __future__ import annotations

import asyncio
from itertools import combinations, permutations
from multiprocessing import get_context
from typing import Callable

from sqlalchemy.orm import Session

from .crud_tools import answer as answer_crud
from .models import Answer


class PermTrain:
    def __init__(
        self,
        db: Session,
        train_method: Callable[[list[list[str]]], None],
        mark_answer_as_trained: Callable[[Session, int, Answer], Answer],
        method: str = "simple",
        limit: int = -1,
        batch_size: int = 100,
        max_threads: int = 5,
    ):
        self.db = db
        self.method = method
        self.limit = limit
        self.batch_size = batch_size
        self.max_threads = max_threads
        self.train_method = train_method
        self.mark_answer_as_trained = mark_answer_as_trained
        self.conversations: list[list[str]] = []

    def make_batches(self, conversations: list[list[str]]) -> list[list[list[str]]]:
        batches: list[list[list[str]]] = []
        for i in range(0, len(conversations), self.batch_size):
            batches.append(conversations[i : i + self.batch_size])
        return batches

    def generate_varied_length_permutations(
        self,
        word_list,
    ) -> list[str]:
        all_permutations: list[str] = []

        limit = (
            self.limit
            if self.limit != -1 and self.limit <= len(word_list)
            else len(word_list)
        )

        # Generate permutations of varying lengths
        for r in range(1, limit + 1):
            for perm in permutations(word_list, r):
                all_permutations.append(" ".join(perm))

        return all_permutations

    def generate_combinations(self, word_list) -> list[str]:
        all_combinations: list[str] = []

        limit = (
            self.limit
            if self.limit != -1 and self.limit <= len(word_list)
            else len(word_list)
        )

        # Generate combinations of varying lengths
        for r in range(1, limit + 1):
            for combo in combinations(word_list, r):
                all_combinations.append(" ".join(combo))

        return all_combinations

    def generate_simple(self, word_list) -> list[str]:
        all_combinations: list[str] = []

        limit = (
            self.limit
            if self.limit != -1 and self.limit <= len(word_list)
            else len(word_list)
        )

        for r in range(1, limit + 1):
            for i in range(1, r + 1):
                all_combinations.append(" ".join(word_list[:i]))

        return all_combinations

    def prepare_conversations(self):
        answers_db = answer_crud.get_answers(self.db, limit=-1, trained=-1)
        if len(answers_db) == 0:
            return 0

        self.conversations: list[list[str]] = []

        for idx, answer in enumerate(answers_db):
            if self.method == "permutation":
                all_permutations = self.generate_varied_length_permutations(answer.tags)
            elif self.method == "combination":
                all_permutations = self.generate_combinations(answer.tags)
            elif self.method == "simple":
                all_permutations = self.generate_simple(answer.tags)
            else:
                raise Exception("Invalid method")

            for permutation in all_permutations:
                self.conversations.append([permutation, answer.answer])

            self.mark_answer_as_trained(self.db, answer.id, answer)

        return len(self.conversations)

    def __len__(self):
        return len(self.conversations)

    async def train_batch(self, batch: list[list[str]]):
        self.train_method(batch)

    async def tag_db_permutation_training(self):
        batches = self.make_batches(self.conversations)
        tasks = []
        completed_tasks = []
        for idx, batch in enumerate(batches):
            tasks.append(asyncio.create_task(self.train_batch(batch)))
            print(f"Training {idx+1}/{len(batches)} batches")
            if len(tasks) >= self.max_threads:
                # Wait for any completed tasks
                completed, _ = await asyncio.wait(
                    tasks, return_when=asyncio.FIRST_COMPLETED
                )

                # Remove completed tasks from the task list and add to the completed list
                for task in completed:
                    tasks.remove(task)
                    completed_tasks.append(task)
        # Wait for any remaining tasks to finish
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        # Wait for any remaining completed tasks to finish
        if completed_tasks:
            await asyncio.gather(*completed_tasks, return_exceptions=True)

        return f"Training done"

    def tag_db_permutation_training_multiprocess(self):
        batches = self.make_batches(self.conversations)
        with get_context("spawn").Pool(self.max_threads) as p:
            p.map(self.train_method, batches)
        return f"Training done"
