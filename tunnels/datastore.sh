#!/bin/sh

source cluster_env.sh

echo "run:"
echo "psql postgresql://database_user:UnicornCanteloupe@localhost:5432/the_database"
echo "or something like that"
kubectl port-forward $(kubectl get pods --selector="app=photonav" --output="jsonpath={.items..metadata.name}") 5432:5432
