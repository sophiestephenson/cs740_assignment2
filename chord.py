#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# chord.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------

import argparse

from flask import Flask, escape, jsonify

from classes import Node

app = Flask(__name__)


@app.route("/")
def hello():
    return "the port is " + str(node.port) + ", and the ID is " + str(node.get_id())


@app.route("/successor")
def successor():
    return jsonify(successor=node.successor())


@app.route("/predecessor")
def predecessor():
    return jsonify(predecessor=node.predecessor)


@app.route("/setpredecessor/<predecessor>")
def set_predecessor(predecessor):
    node.predecessor = predecessor
    return "Predecessor set to " + predecessor


@app.route("/closestprecedingfinger/<id>")
def closest_preceding_finger(id):
    return jsonify(finger=node.closest_preceding_finger(id))


@app.route("/<name>")
def name(name):
    return f"Hello, {escape(name)}!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run a new chord node")
    parser.add_argument(
        "-p", required=True, type=int, help="the port to run the app on"
    )

    args = parser.parse_args()

    node = Node(args.p)

    app.run(port=args.p)
