#!/bin/sh

declare -a ports=("5000" "5001" "5002" "5006" "5007" "5008" "5009" "5010" "5011" "5012")
declare -a ids=("29" "24" "23" "5" "14" "21" "9" "4" "27" "11")

declare -a correctsuccessors=("5010" "5011" "5001" "5009" "5008" "5002" "5012" "5006" "5000" "5007")
declare -a correctpredecessors=("5011" "5002" "5008" "5010" "5012" "5007" "5006" "5000" "5001" "5009")

# set up correct ips for each lookup
declare -a correct=("4" "4" "4" "4" "4" "5" "9" "9" "9" "9" "11" "11" "14" "14" "14" "21" "21" "21" "21" "21" "21" "21" "23" "23" "24" "27" "27" "27" "29" "29" "4" "4")
declare -a correctips=()
for i in "${!ports[@]}"; do
    for j in "${!correct[@]}"; do
        if [ "${ids[$i]}" == "${correct[$j]}" ] 
        then
            correctips[$j]="127.0.0.1:${ports[$i]}"
        fi
    done
done

echo "*** CHECKING SUCCESSORS"
correct=0
for i in "${!ports[@]}"; do
    successor=$(curl -s 127.0.0.1:${ports[$i]}/successor | awk '{print $2}')
    if [ $successor == "\"127.0.0.1:${correctsuccessors[$i]}\"" ]
    then
        ((correct=correct+1))
    fi
done
echo "$correct/10 have the correct successor\n"


echo "*** CHECKING PREDECESSORS"
correct=0
for i in "${!ports[@]}"; do
    predecessor=$(curl -s 127.0.0.1:${ports[$i]}/predecessor | awk '{print $2}')
    if [ $predecessor == "\"127.0.0.1:${correctpredecessors[$i]}\"" ]
    then
        ((correct=correct+1))
    fi
done
echo "$correct/10 have the correct predecessor\n"

echo "*** CHECKING LOOKUPS"
for p in "${ports[@]}"; do
    correct=0
    for i in {0..31}; do
        ip=$(curl -s 127.0.0.1:$p/lookup/$i | awk '{print $10}')
        if [ "$ip" == "${correctips[$i]}" ] 
        then
            ((correct=correct+1))
        fi
    done
    echo "$p: $correct/32 correct"
done