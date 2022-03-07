#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Sophie Stephenson
# March 10, 2022
# ---------------------------------------------------------------------------
""" utils.py

    Useful functions that are not the main algorithms at play here.
    E.g., a function to print a matrix.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------


import random
from math import factorial
from typing import Any, List, Tuple


def print_matrix(M: List[List[Any]]) -> None:
    """Print a matrix in a pretty, aligned format.

       Comes from
       https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python

    Args:
        M: the matrix to print
    """
    print()
    print("\n".join(["".join(["{:10}".format(item) for item in row]) for row in M]))
    print()


def create_random_flows(n_hosts: int, density: float) -> List[Tuple[int]]:
    """Create a bunch of random flows given a number of hosts.

    Args:
        n_hosts: the number of hosts in the network
        density: the percent of total possible flows to instantiate
    """
    flows = []
    max_flows = factorial(n_hosts) / (factorial(n_hosts - 2))

    for i in range(int(max_flows * density)):
        src = random.randint(0, n_hosts - 1)
        dst = random.randint(0, n_hosts - 1)

        # no flows from src to same dst
        while dst == src:
            dst = random.randint(0, n_hosts - 1)

        flows.append((src, dst))

    return sorted(flows)
