from __future__ import annotations
import json


def max_length_answer(data: list[dict[str, str]]):
    max_length = 0
    big_boy = {"answer": "", "tags": []}
    for answer in data:
        if len(answer["answer"]) > max_length:
            max_length = len(answer["answer"])
            big_boy = {"answer": answer["answer"], "tags": answer["tags"]}
    return max_length, big_boy


if __name__ == "__main__":
    with open("output.json", "r") as f:
        data = json.load(f)
    print(max_length_answer(data))
