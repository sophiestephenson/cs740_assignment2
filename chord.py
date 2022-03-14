#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# chord.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------

import argparse
from pprint import pprint

from flask import Flask, jsonify

from classes import Node

app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to chord! My node ID is " + str(node.id)


@app.route("/lookup/<id>")
def lookup(id: str):
    host_node_ip = node.find_successor(id)
    return "The data with ID=" + id + " can be found at " + host_node_ip


@app.route("/successor")
def successor():
    return jsonify(successor=node.successor())


@app.route("/predecessor")
def predecessor():
    return jsonify(predecessor=node.predecessor)


@app.route("/closestprecedingfinger/<id>")
def closest_preceding_finger(id: str):
    return jsonify(finger=node.closest_preceding_finger(id))


@app.route("/findidsuccessor/<id>")
def find_id_successor(id: str):
    return jsonify(id_successor=node.find_successor(id))


@app.route("/setpredecessor/<predecessor>")
def set_predecessor(predecessor: str):
    node.predecessor = predecessor
    return "Predecessor set to " + predecessor


@app.route("/updatefingertable/<s>&<i>")
def update_finger_table(s: str, i: int):
    i = int(i)
    node.update_finger_table(s, i)
    pprint(node.finger_table.table)
    return "Finger table updated"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run a new chord node")
    parser.add_argument(
        "-p", required=True, type=int, help="the port to run the app on"
    )
    args = parser.parse_args()

    node = Node(args.p)
    pprint(node.finger_table.table)

    app.run(port=args.p)
