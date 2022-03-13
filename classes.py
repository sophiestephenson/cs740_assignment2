#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# classes.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------


import hashlib

import requests

from config import FIRST_NODE_PORT, M
from utils import (
    get_node_closest_preceding_finger,
    get_node_predecessor,
    get_node_successor,
    set_node_predecessor,
)


class Node:
    def __init__(self, port):
        self.port = port
        self.ip = "http://127.0.0.1:" + str(port)
        self.predecessor = self.ip
        self.finger_table = FingerTable(self.get_id(), self.ip)

        # join operations
        if port != FIRST_NODE_PORT:
            print("not my first nodeo!")
            self.init_finger_table()
            self.update_others()

    def get_id(self):
        id = hashlib.sha1(self.ip.encode()).hexdigest()
        return int(id, 16) % 2**M

    def successor(self):
        return self.finger_table.node(0)

    def find_successor(self, id):
        n = self.find_predecessor(id)
        return get_node_successor(n)

    def find_predecessor(self, id):
        curr = self.ip
        while not (id > curr and id < get_node_successor(curr)):
            curr = get_node_closest_preceding_finger(curr, id)
        return curr

    def closest_preceding_finger(self, id):
        for i in range(M - 1, -1, -1):
            if self.finger_table.node(i) > self.ip and self.finger_table.node(i) < id:
                return self.finger_table.node(i)
        return self.ip

    def init_finger_table(self):
        self.finger_table.set_node(0, get_node_successor(self.finger_table.start(0)))
        successor_predecessor = get_node_predecessor(self.successor())
        self.predeccessor = successor_predecessor
        set_node_predecessor(successor_predecessor, self.ip)

        for i in range(M - 1):
            print("do more stuff")

        #
        # TODO: implement
        #
        return

    def update_others(self):
        #
        # TODO: implement
        #
        return

    def update_finger_table(self):
        #
        # TODO: implement
        #
        return


class FingerTable:
    def __init__(self, n, ip):
        self.n = n
        self.table = []

        # table should have M entries
        for i in range(M):
            start = self.calculate_start(i)
            interval = (start, self.calculate_start((i + 1) % M))

            entry = {"start": start, "interval": interval, "node": ip}
            self.table.append(entry)

    def calculate_start(self, k):
        return (self.n + (2 ** (k % M))) % (2**M)

    def start(self, k):
        return self.table[k]["start"]

    def interval(self, k):
        return self.table[k]["interval"]

    def node(self, k):
        return self.table[k]["node"]

    def set_start(self, k, start):
        self.table[k]["start"] = start

    def set_interval(self, k, interval):
        self.table[k]["interval"] = interval

    def set_node(self, k, node):
        self.table[k]["node"] = node
