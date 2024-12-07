# Final Project Group11
# Deployment of 2-tiered web application to managed K8s cluster on Amazon EKS, with pod auto-scaling and deployment automation.

# Create EKS Cluster
```sh
git clone https://github.com/dkhan0103/CLO835-Final_Project.git
cd CLO835-Final_Project/manifest

# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv -v /tmp/eksctl /usr/local/bin

# Enable eksctl bash completion
eksctl completion bash >> ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion
# create cluster
eksctl create cluster -f eks_config.yaml
```



## Commands to run the application
```sh
cd mainfest
kubectl create namespace final
kubectl apply -f service-account.yaml -n final
kubectl apply -f secret.yaml -n final
kubectl apply -f mysql_deployment.yaml -n final
kubectl apply -f mysql_clusterip.yaml -n final
kubectl apply -f ConfigMap.yaml -n final
kubectl apply -f webapp_deployment.yaml -n final
kubectl apply -f webapp_lb.yaml -n final
kubectl apply -f hpa_config.yaml -n final
```
