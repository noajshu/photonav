## GCP hosted kubernetes

# set a project
gcloud config set project 

# list all projects
gcloud projects list

# build container with tag for GCR
docker build -t gcr.io/PROJECT_ID/image-name:v0 .

# push image to GCR
gcloud docker push gcr.io/PROJECT_ID/image-name:v0

# list all nodes
kubectl get nodes

# ssh to a VM
gcloud compute ssh root@NODE

# list all clusters
gcloud container clusters list

# create cluster
gcloud container clusters create NAME

# describe cluster (get password for dashboard)
gcloud container clusters describe NAME

# resize cluster
gcloud container clusters resize CLUSTER_NAME --size SIZE

# get credentials (like setting env)
gcloud container clusters get-credentials NAME

# delete a cluster
gcloud container clusters delete NAME

# create a persistent disk
gcloud compute disks create --size 200GB DISK-NAME

# forcefully unmount disk from instance
gcloud compute instances detach-disk INSTANCE --disk DISK-NAME

# resize a persistent disk
gcloud compute disks resize [DISK_NAME] --size [DISK_SIZE]


## kubernetes
# get cluster info
kubectl cluster-info

# list all pods
kubectl get pods

# open bash in a pod (-- is delimiter)
kubectl exec -it PODNAME -- bash

# create a deployment (permanent pod, like replication controller)
kubectl run DEPLOYMENTNAME --image=IMAGE

# look up pods associated with a deployment (-l == --selector)
kubectl get pods -l run=DEPLOYMENTNAME

# scale a replication controller
kubectl scale rc NAME --replicas=COUNT

# describe all the details of a pod
kubectl describe pod NAME

# list all deployments
kubectl get deployments

# delete a deployment
kubectl delete deployment DEPLOYMENTNAME

# create a pod from a pod spec (in general a resource from a resource spec)
kubectl create -f SPEC.json

# rolling update the image of a RC
kubectl rolling-update frontend-v1 frontend-v2 --image=image:v2
