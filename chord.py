#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# chord.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------

import argparse
from pprint import pprint

from flask import Flask, escape

from classes import Node

app = Flask(__name__)


@app.route("/")
def hello():
    return "the port is " + str(port) + ", and the ID is " + str(node.get_id())


@app.route("/<name>")
def name(name):
    return f"Hello, {escape(name)}!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run a new chord node")
    parser.add_argument(
        "-p", required=True, type=int, help="the port to run the app on"
    )

    args = parser.parse_args()
    port = args.p

    node = Node(port)

    app.run(port=port)
