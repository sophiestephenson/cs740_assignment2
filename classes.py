#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Sophie Stephenson
# March 10, 2022
# ---------------------------------------------------------------------------
""" classes.py

    Custom classes for use across the program.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------


from typing import List, Tuple

from utils import print_matrix


class DemandMatrixEntry:
    """An entry in the demand matrix, which keeps track of the number of flows,
    the demand per flow, the convergence status of the flows, and the receiver
    limited status of the flows.

    Attributes:
        num_flows (int) : the number of flows in this entry
        demand (float)  : the current demand per flow
        converged (bool): whether the flows have converged
        rl (bool)       : whether the flows are receiver limited

    """

    def __init__(self, num_flows: int = 0):
        """Initialize a DemandMatrixEntry object.

        Args:
            num_flows: the number of flows in this entry
        """

        self.num_flows = num_flows
        self.demand = 0
        self.converged = False
        self.rl = False

    def __str__(self):
        """Overrides the default implementation"""
        return "{0} flows, Demand={1}, Converged={2}, RL={3}".format(
            self.num_flows, self.demand, self.converged, self.rl
        )


class DemandMatrix:
    """An NxN matrix, where N is the number of hosts in the network.
    For each Mij, the demand matrix keeps track of the
    number of flows from host i to host j, the demand of each of these
    flows, whether the demand has converged, and whether the flows
    are rate limited.

    Attributes:
        n_hosts (int) : the number of hosts in the network
        matrix (List[List[List[Any]]]): An NxN matrix where each entry in
        the matrix is a list of four values:
            [ num flows (int), demand (float), converged (bool), rate limited (bool)]

    """

    def __init__(self, n_hosts: int, flows: List[Tuple[int]]):
        """Initialize a DemandMatrix object matching a layout of active flows.

        Args:
            n_hosts: the number of hosts in the network
            flows: an NxN matrix where each entry Mij
                is the number of flows from host i to host j.
        """

        self.n_hosts = n_hosts
        self.matrix = []

        for i in range(n_hosts):
            self.matrix.append([])
            for j in range(n_hosts):
                self.matrix[i].append(DemandMatrixEntry())

        for f in flows:
            src, dst = f
            self.matrix[src][dst].num_flows += 1

    def display(self) -> None:
        """Display the current demand matrix as a matrix of demand values"""

        demands = []
        for i in range(self.n_hosts):
            demands.append([])
            for j in range(self.n_hosts):
                entry = str(self.n_flows(i, j)) + "|"
                entry += str(round(self.demand(i, j), 3))
                if self.converged(i, j):
                    entry += "*"
                demands[i].append(entry)
        print_matrix(demands)

    def n_flows(self, src: int, dst: int) -> int:
        """Get the number of flows from this src to this dst.

        Args:
            src: the source host
            dst: the destination host

        Returns:
            the number of flows
        """
        return self.matrix[src][dst].num_flows

    def demand(self, src: int, dst: int) -> float:
        """Get the demand per flow from this src to this dst.

        Args:
            src: the source host
            dst: the destination host

        Returns:
            the demand
        """
        return self.matrix[src][dst].demand

    def set_demand(self, src: int, dst: int, demand: float) -> None:
        """Set the number of flows from this src to this dst.

        Args:
            src     : the source host
            dst     : the destination host
            demand  : the new demand per flow
        """
        self.matrix[src][dst].demand = demand

    def converged(self, src: int, dst: int) -> bool:
        """Get the convergence status of the demand from this src to this dst.

        Args:
            src: the source host
            dst: the destination host

        Returns:
            whether the flow demand has converged

        """
        return self.matrix[src][dst].converged

    def set_converged(self, src: int, dst: int) -> None:
        """Mark demand from this src to this dst as converged.

        Args:
            src: the source host
            dst: the destination host
        """
        self.matrix[src][dst].converged = True

    def rl(self, src: int, dst: int) -> bool:
        """Get the receiver-limited status of the flows from this src to this dst.

        Args:
            src: the source host
            dst: the destination host

        Returns:
            whether the flows are receiver limited
        """
        return self.matrix[src][dst].rl

    def set_rl(self, src: int, dst: int) -> None:
        """Set the rate limited flag to True for flows from this src to this dst.

        Args:
            src: the source host
            dst: the destination host
        """
        self.matrix[src][dst].rl = True

    def remove_rl(self, src: int, dst: int) -> None:
        """Set the rate limited flag to False for flows from this src to this dst.

        Args:
            src: the source host
            dst: the destination host
        """
        self.matrix[src][dst].rl = False

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, DemandMatrix):
            for i in range(self.n_hosts):
                for j in range(self.n_hosts):
                    if self.demand(i, j) != other.demand(i, j):
                        return False
            return True
        return NotImplemented
