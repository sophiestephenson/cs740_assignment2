#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# classes.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------


from typing import Tuple

from config import STARTER_NODE_IP, M
from utils import (
    calculate_id_from_ip,
    find_id_successor,
    get_node_closest_preceding_finger,
    get_node_predecessor,
    get_node_successor,
    get_node_successor_id,
    hex_mod_M,
    in_modulo_range,
    set_node_predecessor,
    update_node_finger_table,
)


class Node:
    def __init__(self, port: int):
        # init to basic things
        self.ip = "http://127.0.0.1:" + str(port)
        self.id = calculate_id_from_ip(self.ip)
        self.predecessor = self.ip
        self.finger_table = FingerTable(self.ip, self.id)

        # if not the first node, do join operations
        if self.ip != STARTER_NODE_IP:
            self.init_finger_table()
            self.update_others()

    def successor(self) -> str:
        return self.finger_table.node_ip(0)

    def find_successor(self, id: str) -> str:
        n = self.find_predecessor(id)
        return get_node_successor(n)

    def find_predecessor(self, id: str) -> str:
        curr_id = self.id
        curr_ip = self.ip
        while not in_modulo_range(
            hex_mod_M(id),
            hex_mod_M(curr_id),
            hex_mod_M(get_node_successor_id(curr_ip)),
            end_incl=True,
        ):
            curr_ip = get_node_closest_preceding_finger(curr_ip, hex_mod_M(id))
            curr_id = calculate_id_from_ip(curr_ip)
        return curr_ip

    def closest_preceding_finger(self, id: str) -> str:
        for i in range(M, -1, -1):
            if in_modulo_range(
                hex_mod_M(self.finger_table.node_id(i)),
                hex_mod_M(self.id),
                hex_mod_M(id),
            ):
                return self.finger_table.node_ip(i)
        return self.ip

    def init_finger_table(self) -> None:
        # use the existing starter node to find the first finger
        self.finger_table.set_node(
            0, find_id_successor(STARTER_NODE_IP, self.finger_table.start(0))
        )
        # this feels like it won't work
        successor_predecessor = get_node_predecessor(self.successor())
        self.predeccessor = successor_predecessor
        set_node_predecessor(successor_predecessor, self.ip)

        for i in range(M - 1):
            finger_start = self.finger_table.start(i + 1)
            if in_modulo_range(
                finger_start,
                hex_mod_M(self.id),
                hex_mod_M(self.finger_table.node_id(i)),
                start_incl=True,
            ):
                self.finger_table.set_node(i + 1, self.finger_table.node_ip(i))
            else:
                self.finger_table.set_node(
                    i + 1, get_node_successor(self.finger_table.start(i + 1))
                )

    def update_others(self) -> None:
        for i in range(M):
            p = self.find_predecessor(hex_mod_M(self.id) - (2**i))
            update_node_finger_table(p, self.ip, i)

    def update_finger_table(self, s_ip: str, i: int) -> None:
        if in_modulo_range(
            hex_mod_M(calculate_id_from_ip(s_ip)),
            hex_mod_M(self.id),
            hex_mod_M(self.finger_table.node_id(i)),
            start_incl=True,
        ):
            self.finger_table.set_node(i, s_ip)
            p = self.predecessor
            update_node_finger_table(p, s_ip, i)


class FingerTable:
    def __init__(self, node_ip: str, node_id: str):

        self.table = []
        for i in range(M):

            start = self.calculate_start(hex_mod_M(node_id), i)
            interval = (start, self.calculate_start(hex_mod_M(node_id), (i + 1) % M))

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
        self.table[k]["node id"] = calculate_id_from_ip(node_ip)
