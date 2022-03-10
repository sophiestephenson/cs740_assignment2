#!/usr/bin/env python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

import os
from subprocess import Popen

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo


def custom_topo():

    info("***Setting up network\n")
    topo = Topo()
    h1 = topo.addHost("h1")
    h2 = topo.addHost("h2")
    l1 = topo.addSwitch("l1")
    s1 = topo.addSwitch("s1")
    s2 = topo.addSwitch("s2")
    l2 = topo.addSwitch("l2")
    h3 = topo.addHost("h3")
    h4 = topo.addHost("h4")

    topo.addLink(h1, l1)
    topo.addLink(h2, l1)
    topo.addLink(h3, l2)
    topo.addLink(h4, l2)

    topo.addLink(l1, s1, bw=80)
    topo.addLink(l1, s2, bw=80)
    topo.addLink(s1, l2, bw=80)
    topo.addLink(s2, l2, bw=40)

    remote_controller = Popen(
        # "~/pox/pox.py riplpox.riplpox --topo=ft,4 --routing=random --mode=reactive"
        "~/pox/pox.py riplpox.riplpox --no-cli --routing=hashed --mode=reactive"
    )

    net = Mininet(
        topo=topo,
        link=TCLink,
        controller=RemoteController,
        autoSetMacs=True,
        autoStaticArp=True,
    )

    # Run network
    info("***Starting network\n")
    net.start()

    CLI(net)

    # info("***Testing bandwidth between h1 and h3\n")
    # h1, h4 = net.getNodeByName("h1", "h3")
    # net.iperf((h1, h3), l4Type="UDP")

    # info("***Testing bandwidth between h1 and h4\n")
    # h1, h4 = net.getNodeByName("h1", "h4")
    # net.iperf((h1, h4), l4Type="UDP")

    info("***Shutting down network\n")
    net.stop()

    remote_controller.terminate()


if __name__ == "__main__":
    setLogLevel("info")
    custom_topo()
