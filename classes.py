#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# classes.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------


from pprint import pprint
from time import sleep
from typing import Tuple, TypedDict

from config import STARTER_NODE_IP, M
from utils import (
    calculate_id_from_ip,
    find_id_successor,
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
        self.ip = "localhost:" + str(port)
        self.id = calculate_id_from_ip(self.ip)
        self.predecessor = self.ip
        self.finger_table = FingerTable(self.ip, self.id)

        # if not the first node, do join operations
        if self.ip != STARTER_NODE_IP:
            self.init_finger_table()
            self.update_others()

    def successor(self) -> str:
        return self.finger_table.node_ip(0)

    def successor_id(self) -> int:
        return self.finger_table.node_id(0)

    def find_successor(self, id: int) -> str:
        """ID is mod M"""
        n = self.find_predecessor(id)
        if n == self.ip:
            return self.successor()
        return get_node_successor(n)

    def find_predecessor(self, id: int) -> str:
        """ID is mod M"""
        curr_id = self.id
        curr_ip = self.ip
        curr_ip_successor_id = self.successor_id()

        while not in_modulo_range(
            id,
            curr_id,
            curr_ip_successor_id,
            end_incl=True,
        ):
            if curr_id == self.id:
                curr_ip = self.closest_preceding_finger(id)
            else:
                curr_ip = get_node_closest_preceding_finger(curr_ip, id)

            curr_id = calculate_id_from_ip(curr_ip)
            curr_ip_successor_id = get_node_successor_id(curr_ip)
        return curr_ip

    def closest_preceding_finger(self, id: int) -> str:
        """ID is mod M"""
        for i in range(M - 1, -1, -1):
            if in_modulo_range(
                self.finger_table.node_id(i),
                self.id,
                id,
            ):
                return self.finger_table.node_ip(i)
        return self.ip

    def init_finger_table(self) -> None:
        print("*** setting up finger table")
        # use the existing starter node to find the first finger
        self.finger_table.set_node(
            0, find_id_successor(STARTER_NODE_IP, self.finger_table.start(0))
        )
        successor_predecessor = get_node_predecessor(self.successor())
        self.predeccessor = successor_predecessor
        set_node_predecessor(successor_predecessor, self.ip)

        print("*** initing rest of finger table")
        for i in range(M - 1):
            finger_start = self.finger_table.start(i + 1)
            if in_modulo_range(
                finger_start,
                self.id,
                self.finger_table.node_id(i),
                start_incl=True,
            ):
                self.finger_table.set_node(i + 1, self.finger_table.node_ip(i))
            else:
                self.finger_table.set_node(
                    i + 1,
                    find_id_successor(STARTER_NODE_IP, self.finger_table.start(i + 1)),
                )

    def update_others(self) -> None:
        print("*** updating others' finger tables")
        for i in range(M):
            p = self.find_predecessor(self.id - (2**i))
            update_node_finger_table(p, self.ip, i)

    def update_finger_table(self, s_ip: str, i: int) -> None:
        if in_modulo_range(
            calculate_id_from_ip(s_ip),
            self.id,
            self.finger_table.node_id(i),
            start_incl=True,
        ):
            self.finger_table.set_node(i, s_ip)
            p = self.predecessor
            update_node_finger_table(p, s_ip, i)


class FingerTableEntry(TypedDict):
    start: int
    interval: Tuple[int, int]
    node_ip: str
    node_id: int


class FingerTable:
    def __init__(self, node_ip: str, node_id: int):

        self.table = []
        for i in range(M):

            start = self.calculate_start(node_id, i)
            interval = (start, self.calculate_start(node_id, (i + 1) % M))

            entry: FingerTableEntry = {
                "start": start,
                "interval": interval,
                "node_ip": node_ip,
                "node_id": node_id,
            }
            self.table.append(entry)

        pprint(self.table)

    def calculate_start(self, n: int, k: int) -> int:
        return (n + (2 ** (k % M))) % (2**M)

    def start(self, k: int) -> int:
        return self.table[k]["start"]

    def interval(self, k: int) -> Tuple[int, int]:
        return self.table[k]["interval"]

    def node_ip(self, k: int) -> str:
        return self.table[k]["node_ip"]

    def node_id(self, k: int) -> int:
        return self.table[k]["node_id"]

    def set_start(self, k: int, start: int):
        self.table[k]["start"] = start

    def set_interval(self, k: int, interval: Tuple[int, int]):
        self.table[k]["interval"] = interval

    def set_node(self, k: int, node_ip: str):
        self.table[k]["node_ip"] = node_ip
        self.table[k]["node_id"] = calculate_id_from_ip(node_ip)
