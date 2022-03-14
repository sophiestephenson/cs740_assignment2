#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# classes.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------


from typing import Tuple

from config import FIRST_NODE_PORT, M
from utils import (
    calculate_node_id,
    find_id_successor,
    get_initial_node_ip,
    get_node_closest_preceding_finger,
    get_node_predecessor,
    get_node_successor,
    get_node_successor_id,
    in_modulo_range,
    set_node_predecessor,
    update_node_finger_table,
)


class Node:
    def __init__(self, port: int):
        # init to basic things
        self.ip = "http://127.0.0.1:" + str(port)
        self.id = calculate_node_id(self.ip)
        self.predecessor = self.ip
        self.finger_table = FingerTable(self.ip, self.id)

        # join operations
        if port != FIRST_NODE_PORT:
            self.init_finger_table()
            self.update_others()

    def successor(self) -> str:
        return self.finger_table.node_ip(0)

    def find_successor(self, id: int) -> str:
        n = self.find_predecessor(id)
        return get_node_successor(n)

    def find_predecessor(self, id: int) -> str:
        curr_id = self.id
        curr_ip = self.ip
        while not in_modulo_range(
            id, curr_id, get_node_successor_id(curr_ip), end_incl=True
        ):
            curr_ip = get_node_closest_preceding_finger(curr_ip, id)
            curr_id = calculate_node_id(curr_ip)
        return curr_ip

    def closest_preceding_finger(self, id: int) -> str:
        for i in range(M, -1, -1):
            if in_modulo_range(self.finger_table.node_id(i), self.id, id):
                return self.finger_table.node_ip(i)
        return self.ip

    def init_finger_table(self) -> None:
        starter_node_ip = get_initial_node_ip()

        # use the existing starter node to find the first finger
        self.finger_table.set_node(
            0, find_id_successor(starter_node_ip, self.finger_table.start(0))
        )

        # this feels like it won't work
        successor_predecessor = get_node_predecessor(self.successor())
        self.predeccessor = successor_predecessor
        set_node_predecessor(successor_predecessor, self.ip)

        for i in range(M - 1):
            finger_start = self.finger_table.start(i + 1)
            if in_modulo_range(
                finger_start, self.id, self.finger_table.node_id(i), start_incl=True
            ):
                self.finger_table.set_node(i + 1, self.finger_table.node_ip(i))
            else:
                self.finger_table.set_node(
                    i + 1, get_node_successor(self.finger_table.start(i + 1))
                )

    def update_others(self) -> None:
        for i in range(M):
            p = self.find_predecessor(self.id - (2**i))
            update_node_finger_table(p, self.ip, i)

    def update_finger_table(self, s_ip: str, i: int) -> None:
        s_id = calculate_node_id(s_ip)
        if in_modulo_range(
            s_id, self.id, self.finger_table.node_id(i), start_incl=True
        ):
            self.finger_table.set_node(i, s_ip)
            p = self.predecessor
            update_node_finger_table(p, s_ip, i)


class FingerTable:
    def __init__(self, node_ip: str, node_id: str):

        self.table = []
        for i in range(M):

            start = self.calculate_start(node_id, i)
            interval = (start, self.calculate_start(node_id, (i + 1) % M))

            entry = {
                "start": start,
                "interval": interval,
                "node ip": node_ip,
                "node id": node_id,
            }
            self.table.append(entry)

    def calculate_start(self, n: int, k: int) -> int:
        return (n + (2 ** (k % M))) % (2**M)

    def start(self, k: int) -> int:
        return self.table[k]["start"]

    def interval(self, k: int) -> Tuple[int]:
        return self.table[k]["interval"]

    def node_ip(self, k: int) -> str:
        return self.table[k]["node ip"]

    def node_id(self, k: int) -> int:
        return self.table[k]["node id"]

    def set_start(self, k: int, start: int):
        self.table[k]["start"] = start

    def set_interval(self, k: int, interval: Tuple[int]):
        self.table[k]["interval"] = interval

    def set_node(self, k: int, node_ip: str):
        self.table[k]["node ip"] = node_ip
        self.table[k]["node id"] = calculate_node_id(node_ip)
