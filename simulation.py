#!/usr/bin/env python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo


def custom_topo():

    info("***Setting up network\n")
    topo = Topo()
    h1 = topo.addHost("h1")
    h2 = topo.addHost("h2")
    h3 = topo.addHost("h3")
    h4 = topo.addHost("h4")
    s1 = topo.addSwitch("s1")
    s2 = topo.addSwitch("s2")
    s3 = topo.addSwitch("s3")
    topo.addLink(h1, s1)
    topo.addLink(h2, s1)
    topo.addLink(h3, s2)
    topo.addLink(h4, s3)
    topo.addLink(s1, s2, bw=400)  # , delay='40ms')
    topo.addLink(s1, s3, bw=600)

    net = Mininet(topo=topo, link=TCLink, autoSetMacs=True, autoStaticArp=True)

    # Run network
    info("***Starting network\n")
    net.start()

    info("***Testing bandwidth between h1 and h3\n")
    h1, h4 = net.getNodeByName("h1", "h3")
    net.iperf((h1, h3), l4Type="UDP")

    info("***Testing bandwidth between h1 and h4\n")
    h1, h4 = net.getNodeByName("h1", "h4")
    net.iperf((h1, h4), l4Type="UDP")

    info("***Shutting down network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    custom_topo()
