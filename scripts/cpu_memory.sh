#!/bin/bash

mkdir -p /tmp/ns  && rm -rf /tmp/ns/*

kubectl get ns |grep -vE 'kube-system|rook-ceph|monitor|kube-public|default|NAME'|awk '{print $1}' >/tmp/ns.txt

cat /tmp/ns.txt|while read line
do

NS=$line

rm -f /tmp/ns/cpu_${NS}.txt*

for res in `kubectl -n ${NS} get deploy,sts|grep -v "NAME"|awk '{print $1}' |grep -v "^$"`
do
   cpu_request=`kubectl -n ${NS} get ${res} -o=jsonpath='{.spec.template.spec.containers[*].resources.requests.cpu}'`
   cpu_limits=`kubectl -n ${NS} get ${res} -o=jsonpath='{.spec.template.spec.containers[*].resources.limits.cpu}'`    
   memory_request=`kubectl -n ${NS} get ${res} -o=jsonpath='{.spec.template.spec.containers[*].resources.requests.memory}'`
   memory_limits=`kubectl -n ${NS} get ${res} -o=jsonpath='{.spec.template.spec.containers[*].resources.limits.memory}'`
   
   echo "${res},${cpu_request},${cpu_limits},${memory_request},${memory_limits}" >> /tmp/ns/cpu_${NS}.txt.tmp
done
  sort /tmp/ns/cpu_${NS}.txt.tmp > /tmp/ns/cpu_${NS}.txt
  rm -f /tmp/ns/cpu_${NS}.txt.tmp 

done