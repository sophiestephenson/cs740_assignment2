#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# classes.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------


import hashlib

from config import FIRST_NODE_PORT, M


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

    def find_successor(self, k):
        #
        # TODO: implement
        #
        return

    def find_predecessor(self, k):
        #
        # TODO: implement
        #
        return

    def init_finger_table(self):
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
