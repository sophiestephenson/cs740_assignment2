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


@app.before_first_request
def init():
    node.join()


@app.route("/")
def summary():
    node.join()
    pprint(node.summary())
    return (
        "Welcome to Chord!"
        + "<ul><li>My node ID is "
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
    """ID is a hex string identifier for a specific piece of data"""
    id_mod = int(id, 16) % 2**M
    host_node_ip = node.find_successor(id_mod)
    return "The data with ID=" + id + " can be found at " + host_node_ip


@app.route("/successor")
def successor():
    pprint(node.summary())
    return jsonify(successor=node.successor())


@app.route("/predecessor")
def predecessor():
    pprint(node.summary())
    return jsonify(predecessor=node.predecessor)


@app.route("/closestprecedingfinger/<id>")
def closest_preceding_finger(id: int):
    pprint(node.summary())
    return jsonify(finger=node.closest_preceding_finger(int(id)))


@app.route("/findsuccessor/<id>")
def find_id_successor(id: int):
    pprint(node.summary())
    return jsonify(id_successor=node.find_successor(int(id)))


@app.route("/setpredecessor/<predecessor>")
def set_predecessor(predecessor: str):
    pprint(node.summary())
    node.predecessor = predecessor
    return "Predecessor set to " + predecessor


@app.route("/updatefingertable/<s>/<i>")
def update_finger_table(s: str, i: int):
    pprint(node.summary())
    node.update_finger_table(s, int(i))
    pprint(node.finger_table.table)
    return "Finger table updated\n\n" + str(node.finger_table.table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run a new chord node")
    parser.add_argument(
        "-p", required=True, type=int, help="the port to run the node on"
    )
    args = parser.parse_args()
    port = args.p

    node = Node(port)

    app.run(host="127.0.0.1", port=port, use_reloader=False, debug=True)
