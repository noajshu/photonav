export CLUSTER=$(cat gcloud/CLUSTER)
gcloud container clusters get-credentials $CLUSTER
export NAMESPACE="photonav"
