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


def est_src(src, flows, demands):
    """Estimates the demand at a source node.

    Args:
        src: the index of the sourc host

    Returns:
        an updated demand matrix
    """

    return demands


def est_dst(dst, flows, demands):
    """Estimates the demand at a destination node.

    Args:
        dst (int): the index of the destination host

    Returns:
        an updated demand matrix
    """

    return demands


def estimate_demands(flows):
    """Estimate the natural bandwidth demand of all flows in a network.

    Args:
        flows: an N x N matrix (N = the number of hosts in the network).
            M[i][j] indicates the number of flows going from host i to host j.

    Returns:
        demands: an N x N matrix where M[i][j] indicates the demand per flow
            as a fraction of NIC bandwidth.
    """

    num_hosts = len(flows)

    # initialize demand matrix of zeroes
    demands = []
    old_demands = demands

    for i in range(num_hosts):
        demands[i] = []
        for j in range(num_hosts):
            demands[i].append(0)

    # run loop until it converges
    while old_demands != demands:

        for h in num_hosts:
            est_src(i)

        for h in num_hosts:
            est_dst(i)

    return demands
