#!/bin/sh

declare -a ports=("5000" "5001" "5002" "5006" "5007" "5008" "5009" "5010" "5011" "5012")
declare -a ids=("29" "24" "23" "5" "14" "21" "9" "4" "27" "11")

declare -a correctsuccessors=("5010" "5011" "5001" "5009" "5008" "5002" "5012" "5006" "5000" "5007")
declare -a correctpredecessors=("5011" "5002" "5008" "5010" "5012" "5007" "5006" "5000" "5001" "5009")

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


echo "*** CHECKING SUCCESSOR/PREDECESSOR AGREEMENT"
agree=0
for p in "${ports[@]}"; do
    successor=$(curl -s 127.0.0.1:$p/successor | awk '{print $2}' | cut -d"\"" -f 2 | xargs)
    successorpredecessor=$(curl -s $successor/predecessor | awk '{print $2}' | cut -d"\"" -f 2 | xargs)

    if [ "127.0.0.1:$p" == "$successorpredecessor" ]
    then
        ((agree=agree+1))
    fi
done
echo "$agree/10 correct successor/predecessor pairs\n"

echo "*** CHECKING LOOKUP AGREEMENT"
for i in {0..31}; do
    agree=0
    for p in "${ports[@]}"; do
        compareto=$(curl -s 127.0.0.1:$p/lookup/$i | awk '{print $13}')
        ip=$(curl -s 127.0.0.1:$p/lookup/$i | awk '{print $13}')
        if [ "$ip" == "$compareto" ]
        then
            ((agree=agree+1))
        fi
    done

    echo "For ID=$i, $agree/10 agree: $compareto."
done