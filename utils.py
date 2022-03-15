#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# utils.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------

import hashlib

import requests  # type: ignore[import]

from config import M


def ip_to_id(ip: str) -> int:
    """Given a node's IP, get the hash value of the IP, mod 2^M"""
    id = hashlib.sha1(ip.encode()).hexdigest()
    return int(id, 16) % 2**M


def in_mod_range(
    item: int, start: int, end: int, start_incl=False, end_incl=False
) -> bool:
    """Calculate whether item is in range (start, end) modulo M.

    Args:
        item: The item that might be in range
        start: The start of the range (mod M)
        end: The end of the range (mod M)
        start_incl: Whether the range is inclusive of the start value
        end_incl: Whether the range is inclusive of the end value

    Returns:
        True if item is in the range, False otherwise
    """

    if start == end:
        return True

    i = start
    while i != end:
        # skip the start value if we are not start inclusive
        if i == start and not start_incl:
            i = (i + 1) % (2**M)
            continue

        if i == item:
            return True

        # increment mod M
        i = (i + 1) % (2**M)

    # deal with edge case
    if end_incl and item == end:
        return True

    return False


## =================================================================
##  REQUEST HELPERS
## =================================================================


def get_node_successor(node_ip: str) -> str:
    response = requests.get("http://" + node_ip + "/successor")
    data = response.json()
    return data["successor"]


def get_node_successor_id(node_ip: str) -> int:
    successor = get_node_successor(node_ip)
    return ip_to_id(successor)


def find_successor(node_ip: str, id: int) -> str:
    """Look up the successor of a specific ID (mod M)"""
    response = requests.get("http://" + node_ip + "/findsuccessor/" + str(id))
    data = response.json()
    return data["id_successor"]


def get_node_predecessor(node_ip: str) -> str:
    response = requests.get("http://" + node_ip + "/predecessor")
    data = response.json()
    return data["predecessor"]


def get_node_closest_preceding_finger(node_ip: str, k: int) -> str:
    response = requests.get("http://" + node_ip + "/closestprecedingfinger/" + str(k))
    data = response.json()
    return data["finger"]


def set_node_predecessor(node_ip: str, predecessor: str) -> None:
    requests.get("http://" + node_ip + "/setpredecessor/" + predecessor)


def update_node_finger_table(node_ip: str, s_ip: str, i: int, sender: str) -> bool:
    response = requests.get(
        "http://" + node_ip + "/updatefingertable/" + s_ip + "/" + str(i) + "/" + sender
    )
    data = response.json()
    return data["update_my_table"]
