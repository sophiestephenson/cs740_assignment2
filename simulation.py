#!/usr/bin/env python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo


def custom_topo():

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
    net.start()
    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    custom_topo()
