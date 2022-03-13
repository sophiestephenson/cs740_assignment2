#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# utils.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------

import requests


def get_node_successor(node):
    response = requests.get(node + "/successor")
    data = response.json()
    return data["successor"]


def get_node_closest_preceding_finger(node, k):
    response = requests.get(node + "/closestprecedingfinger/" + k)
    data = response.json()
    return data["finger"]


def get_node_predecessor(node):
    response = requests.get(node + "/predecessor")
    data = response.json()
    return data["predecessor"]


def set_node_predecessor(node, predecessor):
    requests.get(node + "/setpredecessor/" + predecessor)
