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


from typing import List

from classes import DemandMatrix


def est_src(src: int, M: DemandMatrix) -> DemandMatrix:
    """Estimates the demand at a source node.

    Args:
        src             : the index of the source host
        flows           : the list of Flow objects coming from this source host
        M   : a DemandMatrix object with the current network stats

    Returns:
        an updated demand matrix
    """

    df = 0  # converged demand
    nu = 0  # number of unconverged flows

    for h in M.n_hosts():
        num_flows = M.n_flows(src, h)
        if M.converged(src, h):
            df += M.demand(src, h) * num_flows
        else:
            nu += num_flows

    # ADDED to deal with zero division thing
    if nu == 0:
        return M

    es = (1.0 - df) / nu  # equal share rate

    for h in M.n_hosts():
        if not M.converged(src, h):
            M.set_demand(src, h, es)

    return M


def est_dst(dst: int, M: DemandMatrix) -> DemandMatrix:
    """Estimates the demand at a destination node.

    Args:
        dst (int)   : the index of the destination host
        flows       : the list of Flow objects coming from this source host
        M   : a DemandMatrix object with the current network stats

    Returns:
        an updated demand matrix
    """

    # only get the flows to this dst

    dt = 0  # total demand
    ds = 0  # sender limited demand
    nr = 0  # number of receiver limited flows

    for i in M.n_hosts():
        num_flows = M.n_flows(i, dst)
        if num_flows > 0:
            M.set_rl(i, dst)
            dt += M.demand(i, dst) * num_flows
            nr += num_flows

    if dt <= 1.0:
        return M

    es = 1.0 / nr  # equal share rate

    while True:

        nr = 0
        some_set_to_false = False

        for i in M.n_hosts():
            num_flows = M.n_flows(i, dst)
            if M.rl(i, dst):
                if M.demand(i, dst) < es:
                    ds += M.demand(i, dst) * num_flows
                    M.remove_rl(i, dst)
                    some_set_to_false = True
                else:
                    nr += num_flows

        es = (1.0 - ds) / nr

        if not some_set_to_false:
            break

    for i in M.n_hosts():
        if M.rl(i, dst):
            M.set_demand(i, dst, es)
            M.set_converged(i, dst)

    return M


def estimate_demands(flows: List[List[int]]) -> DemandMatrix:
    """Estimate the natural bandwidth demand of all flows in a network.

    Args:
        n_hosts : the number of hosts in the network
        flows   : a list of Flow objects

    Returns:
        demand_matrix: a DemandMatrix object

    """

    # initialize demand matrix
    M = DemandMatrix(flows)

    n_hosts = len(flows)

    # run loop until it converges
    while True:

        old_M = M

        for h in range(n_hosts):
            print("est_src(", h, ")")
            M = est_src(h, M)

        for h in range(n_hosts):
            print("est_dst(", h, ")")
            M = est_dst(h, M)

        if old_M == M:
            break

    return M


if __name__ == "__main__":

    flows = [[0, 1, 1, 1], [2, 0, 1, 0], [1, 0, 0, 1], [0, 2, 0, 0]]

    estimate_demands(flows)
