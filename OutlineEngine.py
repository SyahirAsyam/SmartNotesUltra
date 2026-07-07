
import json
import os

OUTLINE_FILE = "outline.json"


def load_outline():

    if os.path.exists(OUTLINE_FILE):

        with open(OUTLINE_FILE, "r") as f:

            return json.load(f)

    return {

        "color": "#FFFFFF"

    }


def save_outline(data):

    with open(OUTLINE_FILE, "w") as f:

        json.dump(

            data,

            f,

            indent=4

        )
