#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# classes.py
# Sophie Stephenson
# March 15, 2022
# ---------------------------------------------------------------------------


import hashlib


class Node:
    def __init__(self, port):
        self.port = port
        self.ip = "127.0.0.1:" + str(port)
        self.successor = ""
        self.predecessor = ""
        self.finger_table = []

    def get_id(self):
        return hashlib.sha1(self.ip.encode()).hexdigest()
