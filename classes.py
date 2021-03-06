#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# classes.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------


from pprint import pprint
from typing import Tuple, TypedDict

from config import STARTER_NODE_IP, M
from utils import (
    find_successor,
    get_node_closest_preceding_finger,
    get_node_predecessor,
    get_node_successor,
    get_node_successor_id,
    in_mod_range,
    ip_to_id,
    set_node_predecessor,
    update_node_finger_table,
)


class Node:
    def __init__(self, port: int):
        # init to basic things
        self.ip = "127.0.0.1:" + str(port)
        self.id = ip_to_id(self.ip)
        self.predecessor = self.ip
        self.finger_table = FingerTable(self.ip, self.id)
        self.joined = False

    def successor(self) -> str:
        return self.finger_table.node_ip(0)

    def successor_id(self) -> int:
        return self.finger_table.node_id(0)

    def join(self) -> None:
        # if not the first node, do join operations
        if self.ip != STARTER_NODE_IP and not self.joined:
            self.init_finger_table()
            self.update_others()
            self.joined = True

    def find_successor(self, id: int) -> str:
        """ID is mod M"""
        assert id >= 0 and id < 2**M

        n = self.find_predecessor(id)
        if n == self.ip:
            return self.successor()
        return get_node_successor(n)

    def find_predecessor(self, id: int) -> str:
        """ID is mod M"""
        assert id >= 0 and id < 2**M

        curr_id = self.id
        curr_ip = self.ip
        succ_id = self.successor_id()

        while not in_mod_range(
            id,
            curr_id,
            succ_id,
            end_incl=True,
        ):
            if curr_id == self.id:
                curr_ip = self.closest_preceding_finger(id)
            else:
                curr_ip = get_node_closest_preceding_finger(curr_ip, id)

            curr_id = ip_to_id(curr_ip)
            succ_id = get_node_successor_id(curr_ip)

        return curr_ip

    def closest_preceding_finger(self, id: int) -> str:
        """ID is mod M"""
        assert id >= 0 and id < 2**M

        for i in range(M - 1, -1, -1):
            if in_mod_range(self.finger_table.node_id(i), self.id, id):
                return self.finger_table.node_ip(i)
        return self.ip

    def init_finger_table(self) -> None:
        # use the existing starter node to find our successor
        my_successor = find_successor(STARTER_NODE_IP, self.finger_table.start(0))
        self.finger_table.set_node(0, my_successor)

        # update predecessor pointers accordingly
        successor_predecessor = get_node_predecessor(my_successor)
        self.predecessor = successor_predecessor
        set_node_predecessor(my_successor, self.ip)

        for i in range(M - 1):
            if in_mod_range(
                self.finger_table.start(i + 1),
                self.id,
                self.finger_table.node_id(i),
                start_incl=True,
            ):
                self.finger_table.set_node(i + 1, self.finger_table.node_ip(i))

            else:
                # otherwise, use the starter node to find the right finger
                next_finger = find_successor(
                    STARTER_NODE_IP, self.finger_table.start(i + 1)
                )
                self.finger_table.set_node(i + 1, next_finger)

    def update_others(self) -> None:
        for i in range(M):
            p = self.find_predecessor((self.id - (2**i)) % 2**M)
            if p != self.ip:
                response = update_node_finger_table(p, self.ip, i, self.ip)

                # deal with case where the other node sends a response right back here
                if response == True:
                    self.update_finger_table(self.ip, i, self.ip)
            else:
                self.update_finger_table(self.ip, i, self.ip)

    def update_finger_table(self, s_ip: str, i: int, orig_sender: str) -> bool:
        assert i >= 0 and i < M

        if in_mod_range(
            ip_to_id(s_ip),
            self.id,
            self.finger_table.node_id(i),
            # start_incl=True,
            end_incl=True,
        ):
            self.finger_table.set_node(i, s_ip)
            p = self.predecessor
            if p != orig_sender:
                return update_node_finger_table(p, s_ip, i, orig_sender)
            else:
                return True

        return False

    def summary(self):
        return {
            "ip": self.ip,
            "id": self.id,
            "predecessor": self.predecessor,
            "successor": self.successor(),
            "finger_table": self.finger_table.table,
        }


class FingerTableEntry(TypedDict):
    start: int
    node_ip: str
    node_id: int


class FingerTable:
    def __init__(self, node_ip: str, node_id: int):

        self.table = []
        for i in range(M):

            start = self.calculate_start(node_id, i)

            entry: FingerTableEntry = {
                "start": start,
                "node_ip": node_ip,
                "node_id": node_id,
            }
            self.table.append(entry)

    def calculate_start(self, n: int, k: int) -> int:
        return (n + (2 ** (k % M))) % (2**M)

    def start(self, k: int) -> int:
        return self.table[k]["start"]

    def node_ip(self, k: int) -> str:
        return self.table[k]["node_ip"]

    def node_id(self, k: int) -> int:
        return self.table[k]["node_id"]

    def set_start(self, k: int, start: int):
        self.table[k]["start"] = start

    def set_node(self, k: int, node_ip: str):
        self.table[k]["node_ip"] = node_ip
        self.table[k]["node_id"] = ip_to_id(node_ip)
