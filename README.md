# DiscordBot
For this project i used kind cluster because its lightweight and flexible

I used it on my linux and windows machines it should work on Mac also



# Prerequisites
[docker](https://docs.docker.com/engine/install/)

[helm](https://helm.sh/docs/intro/install/)

[kubectl](https://kubernetes.io/docs/tasks/tools/)

git clone the repo

# For local Tests with docker only
```
docker compose --build --file Application/webapp up -d
```

test it
```
curl http://localhost:8080/get-repos
curl http://localhost:8080/check-repos-private
curl http://localhost:8080/ready
```

# For Local Kubernetes

## To download

Reference from https://kind.sigs.k8s.io/docs/user/quick-start/#installing-with-a-package-manager

Mac:

```
brew install kind
```

Linux:
```
# For AMD64 / x86_64
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
# For ARM64
[ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-arm64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

Windows:
```
choco install kind
```

## Create a kind cluster with the following configuration in order for us to reach the cluster from the localhost(make sure port 80 is available), on windows use git bash
```
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
EOF
```


## Then make sure to use the cluster
```
kubectl config use-context kind-kind
```


## Install nginx ingress controller with the following configuration
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update

helm upgrade --install -n kube-system ingress-nginx ingress-nginx/ingress-nginx \
    --set controller.hostPort.enabled=true \
    --set controller.admissionWebhooks.enabled=false
```

## Create secret for github token

kubectl create secret generic github-token --from-literal=GITHUB_TOKEN=you-token



## Install both services
```
kubectl apply -f Kubernetes/mongodb
helm upgrade --install webapp Kubernetes/webapp
helm upgrade --install mongo-updater Kubernetes/mongo-updater
```

## Use port forward to test the app
```
POD_NAME=$(kubectl get pods -l app=webapp -o name)

kubectl port-forward $POD_NAME 8080:8080
```

