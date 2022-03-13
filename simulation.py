#!/usr/bin/env python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

import os
from subprocess import Popen
from time import sleep

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo

from ripllib.dctopo import FatTreeTopo

def custom_topo():

    info("***Setting up network\n")
    topo = Topo()
    h1 = topo.addHost("h1")
    h2 = topo.addHost("h2")
    l1 = topo.addSwitch("l1")
    s1 = topo.addSwitch("s1")
    s2 = topo.addSwitch("s2")
    l2 = topo.addSwitch("l2")
    #h3 = topo.addHost("h3")
    #h4 = topo.addHost("h4")

    topo.addLink(h1, l1)
    topo.addLink(l1, h1)
    #topo.addLink(h2, l1)
    topo.addLink(l2, h2)
    topo.addLink(h2, l2)
    #topo.addLink(h4, l2)

    topo.addLink(l1, s1, bw=80)
    topo.addLink(s1, l1, bw=80)
    topo.addLink(l1, s2, bw=80)
    topo.addLink(s2, l1, bw=80)
    topo.addLink(s1, l2, bw=80)
    topo.addLink(l2, s1, bw=80)
    topo.addLink(s2, l2, bw=40)
    topo.addLink(l2, s2, bw=40)

    topo_size = 4
    routing_alg = "st"
    mode = "proactive"

    fttopo = FatTreeTopo(topo_size)

    # let the controller get set up
    cmd = "/bin/sh -c /home/mininet/pox/pox.py controllers.riplpox --topo=ft," + str(topo_size) + " --routing=" + routing_alg + " --mode=" + mode + " &"
    riplpox = Popen(cmd.split())
    sleep(2)

    net = Mininet(
        topo=fttopo,
        link=TCLink,
        autoSetMacs=True,
        autoStaticArp=True,
    )

    net.addController(name="riplpox", controller=RemoteController)

    # Run network
    info("***Starting network\n")
    net.start()

    #net.pingAllFull()
    CLI(net)

    info("***Shutting down network\n")
    net.stop()
    riplpox.kill()

    os.system("sudo mn -c")
    os.system("sudo fuser -k 6633/tcp")

if __name__ == "__main__":
    setLogLevel("info")
    custom_topo()
