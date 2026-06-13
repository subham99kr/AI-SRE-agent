#!/bin/bash

echo "Cleaning cluster..."

kubectl delete deployment broken-app --ignore-not-found
kubectl delete deployment image-pull-app --ignore-not-found
kubectl delete deployment oom-app --ignore-not-found
kubectl delete deployment dns-app --ignore-not-found
kubectl delete deployment db-app --ignore-not-found
kubectl delete deployment cpu-app --ignore-not-found
kubectl delete deployment memory-app --ignore-not-found
kubectl delete deployment frontend-app --ignore-not-found

kubectl delete service postgres --ignore-not-found

kubectl delete networkpolicy deny-all --ignore-not-found

kubectl delete pvc broken-pvc --ignore-not-found

echo "Cluster cleaned."