# CS740 Assignment 2: Chord

I have implemented a simplified version of Chord in Python using Flask apps for each node. 

## Setup
Ensure you have all requirements installed by running

    $ pip install -r requirements.txt

To set up a Chord network with 10 nodes (M=5), run

    $ ./setup.sh

This script will initialize 10 Flask apps, then join each node into the Chord network one by one. 

Once you are done, run

    $ ./cleanup.sh

to kill all running nodes.

## Interacting with the nodes
Once you've got the Chord network up and running, you can interact with the nodes by visiting the IP of the node on your browser (or using cURL). 
- Visit ```127.0.0.1:[port]/``` to see details about the node's ID, successor, predecessor, and finger table. 
- Use ```127.0.0.1:[port]/lookup/[key]``` to get the location of data with a specific key value (modulo 2^M). There is no actual data in this implementation, so this path simply returns where the data *would* be. This only works when *key* is an integer modulo 2^M.
- Use ```127.0.0.1:[port]/lookuphex/[key]``` to get the location of data with a specific hexidecimal key value. Internally, this function maps the key value to an ID modulo 2^M.

## Adding nodes
You can also add your own nodes to see how they interact with everybody. To do so, follow these steps:
1. Choose a port in the list [5014, 5015, 5018, 5019]. These nodes will not generate IDs that conflict with existing nodes.
2. Run ```$ python chord.py -p [port] &``` to start the Flask app for that node.

3. Run ```$ curl 127.0.0.1:[port]/join```, or visit ```127.0.0.1:[port]/join``` in a browser, to connect the node to the Chord network.

## Testing the network
You can verify the correctness of the network by running two scripts:

    $ ./test_correctness.sh
    $ ./test_agreement.sh

```./test_correctness.sh``` tests whether all nodes have the correct successor and predecessor, and additionally whether they map keys (mod M) to the correct host node. I calculated the correct values by hand for this test. 

```./test_agreement.sh``` tests whether all successor/predecessor pairs agree, i.e. if a node N1 is the successor of node N2, then it should be that N2 is the predecessor of N1. It also tests that all nodes agree on the location of different data keys. 