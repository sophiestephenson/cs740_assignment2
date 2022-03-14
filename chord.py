#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# chord.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------

import argparse
from pprint import pprint
from time import sleep

from flask import Flask, jsonify

from classes import Node
from config import M

app = Flask(__name__)


@app.route("/")
def hello():
    return (
        "Welcome to chord! <ul><li>My node ID is "
        + str(node.id)
        + "</li><li>My successor is "
        + node.successor()
        + "</li><li>My predecessor is "
        + node.predecessor
        + "</li><li>My finger table is"
        + str(node.finger_table.table)
        + "</li></ul>"
    )


@app.route("/lookup/<id>")
def lookup(id: str):
    id_mod = int(id, 16) % 2**M
    host_node_ip = node.find_successor(id_mod)
    return "The data with ID=" + id + " can be found at " + host_node_ip


@app.route("/successor")
def successor():
    return jsonify(successor=node.successor())


@app.route("/predecessor")
def predecessor():
    return jsonify(predecessor=node.predecessor)


@app.route("/closestprecedingfinger/<id>")
def closest_preceding_finger(id: int):
    return jsonify(finger=node.closest_preceding_finger(int(id)))


@app.route("/findsuccessor/<id>")
def find_id_successor(id: int):
    return jsonify(id_successor=node.find_successor(int(id)))


@app.route("/setpredecessor/<predecessor>")
def set_predecessor(predecessor: str):
    node.predecessor = predecessor
    return "Predecessor set to " + predecessor


@app.route("/updatefingertable/<s>/<i>")
def update_finger_table(s: str, i: int):
    node.update_finger_table(s, int(i))
    pprint(node.finger_table.table)
    return "Finger table updated\n\n" + str(node.finger_table.table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run a new chord node")
    parser.add_argument(
        "-p", required=True, type=int, help="the port to run the node on"
    )
    args = parser.parse_args()

    node = Node(args.p)

    app.run(port=args.p, use_reloader=False)
