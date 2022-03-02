#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Sophie Stephenson
# March 10, 2022
# ---------------------------------------------------------------------------
""" demand_estimation.py

    Contains code for estimating the natural bandwidth demand of flows in a
    network.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------


from pprint import pprint
from typing import Any, List
from venv import create
from xmlrpc.client import Boolean


class Flow:
    """A flow from a source to a destination.

    Attributes:
        src (int)       : The source host of the flow
        dst (int)       : The destination host of the flow
        demand (int)    : The demand of this flow
        converged (bool): True if this flow has converged
        rl (bool)       : True if this flow is receiver limited

    """

    def __init__(self, src: int, dst: int, demand: float) -> None:
        """Initialize a Flow. Flows are initially not converged and not
            receiver limited.

        Args:
            size (int): The number of hosts in the network.
        """

        self.src = src
        self.dst = dst
        self.demand = demand
        self.converged = False
        self.rl = False

    def __str__(self):
        """Overrides the default implementation"""
        return "{0} -> {1}, Demand={2}, Converged={3}, RL={4}".format(
            self.src, self.dst, self.demand, self.converged, self.rl
        )


class DemandMatrix:
    """An NxN matrix, where N is the number of hosts in the network, which
        marks the demand at each pair of hosts and whether the demand
        has converged.

    Attributes:
        demands (list[list[int]])       : A matrix of demands
        convergences (list[list[bool]]) : A matrix of convergences

    """

    def __init__(self, size: int) -> None:
        """Initialize a DemandMatrix object of a specific size. The demand
            matrix starts with all zeroes; the convergence matrix starts
            with all False.

        Args:
            size (int): The number of hosts in the network.
        """

        self.demand = []
        self.converged = []

        for i in range(size):
            self.demand.append([])
            self.converged.append([])
            for j in range(size):
                self.demand[i].append(0)
                self.converged[i].append(True)

    def __eq__(self, other) -> Boolean:
        """Overrides the default implementation"""
        if isinstance(other, DemandMatrix):
            return (self.demand == other.demand) and (self.converged == other.converged)
        return NotImplemented


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


def est_src(src: int, flows: List[Flow], demand_matrix: DemandMatrix) -> DemandMatrix:
    """Estimates the demand at a source node.

    Args:
        src             : the index of the source host
        flows           : the list of Flow objects coming from this source host
        demand_matrix   : a DemandMatrix object with the current network stats

    Returns:
        an updated demand matrix
    """

    # only get the flows from this source
    flows = [f for f in flows if f.src == src]

    df = 0  # converged demand
    nu = 0  # number of unconverged flows

    for f in flows:
        if f.converged:
            df += f.demand
        else:
            nu += 1

    es = (1.0 - df) / nu  # equal share rate

    for f in flows:
        if not f.converged:
            demand_matrix.demand[src][f.dst] = es

    return demand_matrix


def est_dst(dst: int, flows: List[Flow], demand_matrix: DemandMatrix) -> DemandMatrix:
    """Estimates the demand at a destination node.

    Args:
        dst (int)   : the index of the destination host
        flows       : the list of Flow objects coming from this source host
        demand_matrix   : a DemandMatrix object with the current network stats

    Returns:
        an updated demand matrix
    """

    # only get the flows to this dst
    flows = [f for f in flows if f.dst == dst]

    dt = 0  # total demand
    ds = 0  # sender limited demand
    nr = 0  # number of receiver limited flows

    for f in flows:
        f.rl = True
        dt += f.demand
        nr += 1

    if dt <= 1.0:
        return demand_matrix

    es = 1.0 / nr  # equal share rate
    print(es)

    while True:

        nr = 0
        some_set_to_false = False

        for f in flows:
            if f.rl:
                if f.demand <= es:  # HAD TO CHANGE TO <=
                    ds += f.demand
                    f.rl = False
                    some_set_to_false = True
                else:
                    nr += 1

        es = (1.0 - ds) / nr
        print(es)

        if not some_set_to_false:
            break

    for f in flows:
        if f.rl:
            print(f)
            demand_matrix.demand[f.src][dst] = es
            demand_matrix.converged[f.src][dst] = True
            f.converged = True  # HAD TO ADD THIS, IS IT HELPFUL?

    return demand_matrix


def estimate_demands(n_hosts: int, flows: List[Flow]) -> DemandMatrix:
    """Estimate the natural bandwidth demand of all flows in a network.

    Args:
        n_hosts : the number of hosts in the network
        flows   : a list of Flow objects

    Returns:
        demand_matrix: a DemandMatrix object

    """

    # initialize demand matrix
    demand_matrix = DemandMatrix(n_hosts)
    print_matrix(demand_matrix.demand)

    # run loop until it converges
    while True:

        old_demands = demand_matrix

        for h in range(n_hosts):
            print("est_src(", h, ")")
            demand_matrix = est_src(h, flows, demand_matrix)

        for h in range(n_hosts):
            print("est_dst(", h, ")")
            demand_matrix = est_dst(h, flows, demand_matrix)

        print_matrix(demand_matrix.demand)

        if old_demands == demand_matrix:
            break

    return demand_matrix


if __name__ == "__main__":

    flows = []
    flows += create_flows(0, [1, 2, 3])
    flows += create_flows(1, [0, 0, 2])
    flows += create_flows(2, [0, 3])
    flows += create_flows(3, [1, 1])

    estimate_demands(4, flows)
