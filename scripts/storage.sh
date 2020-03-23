#!/bin/bash

mkdir -p /tmp/ns  && rm -rf /tmp/ns/*

kubectl get ns |grep -vE 'kube-system|rook-ceph|monitor|kube-public|default|NAME'|awk '{print $1}' >/tmp/ns.txt

cat /tmp/ns.txt|while read line
do

    NS=$line

    rm -f /tmp/ns/storage_${NS}.txt*
    kubectl -n $NS get pvc|grep -v "NAME"|awk '{print $1"   "$4}' > /tmp/ns/tmp_${NS}.txt

    cat /tmp/ns/tmp_${NS}.txt |while read line
    do
       num=`echo $line|awk '{print $2}'`
       name=`echo $line|awk '{print $1}'|awk -F '-' '{print $1"-"$2}'`
       echo "$name $num" >> /tmp/ns/storage_${NS}.txt.tmp
    done

    sort -u  /tmp/ns/storage_${NS}.txt.tmp >> /tmp/ns/storage_${NS}.txt
    rm -f /tmp/ns/storage_${NS}.txt.tmp  /tmp/ns/tmp_${NS}.txt

done
