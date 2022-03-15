#!/bin/sh


declare -a ports=("5000" "5001" "5002" "5006" "5007" "5008" "5009" "5010" "5011" "5012")
declare -a ids=("29" "24" "23" "5" "14" "21" "9" "4" "27" "11")

echo "Setting up nodes..."
sleep 1
for port in "${ports[@]}"; do
    python3 chord.py -p $port &
done    
sleep 1

echo "Joining the network..."
for port in "${ports[@]}"; do
    curl 127.0.0.1:$port/join
    sleep 0.5
done

echo "\n*** SETUP COMPLETE ***"
echo "----------------------------"
echo "Nodes currently running on:"
for i in "${!ports[@]}"; do
    echo "- 127.0.0.1:${ports[$i]} (ID = ${ids[$i]})"
done

echo "\n*** INSTRUCTIONS ***"
echo "To interact with existing nodes, visit any node on your browser."
echo "The following paths provide information:"
echo "\t-  127.0.0.1:[port]/ gives a summary of the node: its ID, its"
echo "\t   successor and predecessor, and its finger table."
echo "\t-  127.0.0.1:[port]/lookup/[key] allows you to look up the location " 
echo "\t   of data with a given (hexadecimal) key. No data is currently"
echo "\t   stored in the nodes for simplicity, so this page returns the"
echo "\t   hypothetical location of data with that key."

echo "\nTo add a new node, do the following:"
echo "\t- Select a port from the list [5014, 5015, 5018, 5019]. These"
echo "\t  ports will not generate IDs that conflict with existing nodes."
echo "\t- Run \"python chord.py -p [port]\" to start the node."
echo "\t- Run \"curl 127.0.0.1:[port]/join\", or connect to"
echo "\t  127.0.0.1:[port]/join in a browser, to connect the node to "
echo "\t  the Chord network."

echo "\nWhen you are finished with Chord, run \"./cleanup.sh\" to"
echo "kill all running nodes."