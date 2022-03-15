#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# chord.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------

import argparse
import logging

from flask import Flask, jsonify

from classes import Node
from config import M

app = Flask(__name__)
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


@app.route("/")
def summary_page():
    return (
        "Welcome to Chord!"
        + "<ul><li>ID = "
        + str(node.id)
        + "</li><li>Successor = "
        + node.successor()
        + "</li><li>Predecessor = "
        + node.predecessor
        + "</li><li>Finger table:<ul><li>"
        + str(node.finger_table.table[0])
        + "</li><li>"
        + str(node.finger_table.table[1])
        + "</li><li>"
        + str(node.finger_table.table[2])
        + "</li><li>"
        + str(node.finger_table.table[3])
        + "</li><li>"
        + str(node.finger_table.table[4])
        + "</li></li></ul>"
    )


@app.route("/join")
def init():
    node.join()
    return "Node " + str(node.id) + " successfully joined the network!\n"


@app.route("/lookup/<id>")
def lookup(id: str):
    """ID is a hex string identifier for a specific piece of data"""
    id_mod = int(id, 16) % 2**M
    host_node_ip = node.find_successor(id_mod)
    return (
        "The data with ID="
        + id
        + " maps to "
        + str(id_mod)
        + ", and can be found at "
        + host_node_ip
    )


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


@app.route("/updatefingertable/<s>/<i>/<sender>")
def update_finger_table(s: str, i: int, sender: str):
    response = node.update_finger_table(s, int(i), sender)
    return jsonify(update_my_table=response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run a new chord node")
    parser.add_argument(
        "-p", required=True, type=int, help="the port to run the node on"
    )
    args = parser.parse_args()
    port = args.p

    node = Node(port)

    app.run(host="127.0.0.1", port=port, use_reloader=False, debug=True)
