kubectl config set-context --current --namespace=test

kubectl get deployments -o wide
kubectl get pods -l app=explore-deploy-app
