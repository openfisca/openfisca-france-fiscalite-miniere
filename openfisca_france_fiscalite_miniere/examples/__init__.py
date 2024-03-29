import json
import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__))


def parse(file_name):
    file_path = os.path.join(DIR_PATH, file_name)

    with open(file_path, "r") as file:
        return json.loads(file.read())


article = parse("article.json")
