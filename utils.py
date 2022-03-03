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


from typing import Any, List

from classes import Flow


def create_flows(src: int, dsts: List[int]) -> List[Flow]:
    """Create a list of flows out of a source node.

    Args:
        src: The source node for the flows
        dst: The list of destination nodes for the flows

    Returns:
        A list of flows with equal demands summing to zero

    """
    flows = []
    proportion = 1 / len(dsts)

    for d in dsts:
        f = Flow(src, d, proportion)
        flows.append(f)

    return flows


def print_matrix(M: List[List[Any]]) -> None:
    """Print a matrix in a pretty, aligned format.

       Comes from
       https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python

    Args:
        M: the matrix to print
    """
    print()
    print(
        "\n".join(
            ["".join(["{:7}".format(round(item, 3)) for item in row]) for row in M]
        )
    )
    print()
