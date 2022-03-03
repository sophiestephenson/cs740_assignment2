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


from ast import List


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

    def __init__(self, num_flows: int):
        """Initialize a DemandMatrixEntry object.

        Args:
            num_flows (int) : the number of flows in this entry
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
        num_hosts (int) : the number of hosts in the network
        matrix (List[List[List[Any]]]): An NxN matrix where each entry in
        the matrix is a list of four values:
            [ num flows (int), demand (float), converged (bool), rate limited (bool)]

    """

    def __init__(self, flows: List[List[int]]):
        """Initialize a DemandMatrix object matching a layout of active flows.

        Args:
            flows (List[List[int]]): an NxN matrix where each entry Mij
                is the number of flows from host i to host j.
        """

        num_hosts = len(flows)
        self.n_hosts = num_hosts
        self.matrix = []

        for i in range(num_hosts):
            self.matrix.append([])
            for j in range(num_hosts):
                entry = DemandMatrixEntry(flows[i][j])
                self.matrix[i].append(entry)

    def n_hosts(self) -> int:
        """Get the number of hosts in the network.

        Returns:
            the number of hosts
        """
        return self.n_hosts

    def n_flows(self, src: int, dst: int) -> int:
        """Get the number of flows from this src to this dst.

        Args:
            src (int): the source host
            dst (int): the destination host

        Returns:
            the number of flows
        """
        return self.matrix[src][dst].num_flows

    def demand(self, src: int, dst: int) -> float:
        """Get the demand per flow from this src to this dst.

        Args:
            src (int): the source host
            dst (int): the destination host

        Returns:
            the demand
        """
        return self.matrix[src][dst].demand

    def set_demand(self, src: int, dst: int, demand: float) -> None:
        """Set the number of flows from this src to this dst.

        Args:
            src (int)       : the source host
            dst (int)       : the destination host
            demand (float)  : the new demand per flow
        """
        self.matrix[src][dst].demand = demand

    def converged(self, src: int, dst: int) -> bool:
        """Get the convergence status of the demand from this src to this dst.

        Args:
            src (int): the source host
            dst (int): the destination host

        Returns:
            whether the flow demand has converged

        """
        return self.matrix[src][dst].converged

    def set_converged(self, src: int, dst: int) -> None:
        """Mark demand from this src to this dst as converged.

        Args:
            src (int): the source host
            dst (int): the destination host
        """
        self.matrix[src][dst].converged = True

    def rl(self, src: int, dst: int) -> bool:
        """Get the receiver-limited status of the flows from this src to this dst.

        Args:
            src (int): the source host
            dst (int): the destination host

        Returns:
            whether the flows are receiver limited
        """
        return self.matrix[src][dst].rl

    def set_rl(self, src: int, dst: int) -> None:
        """Set the rate limited flag to True for flows from this src to this dst.

        Args:
            src (int): the source host
            dst (int): the destination host
        """
        self.matrix[src][dst].rl = True

    def remove_rl(self, src: int, dst: int) -> None:
        """Set the rate limited flag to False for flows from this src to this dst.

        Args:
            src (int): the source host
            dst (int): the destination host
        """
        self.matrix[src][dst].rl = False

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, DemandMatrix):
            for i in self.n_hosts:
                for j in self.n_hosts:
                    if self.demand(i, j) != other.demand(i, j):
                        return False
            return True
        return NotImplemented
