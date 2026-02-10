kubectl config set-context --current --namespace=user-platform-exam

docker build -t auth-service:latest -f auth_service/Dockerfile .
docker build -t profile-service:latest -f profile_service/Dockerfile .
docker build -t notification-service:latest -f notification_service/Dockerfile .

kubectl rollout restart deployment/auth_service
kubectl rollout restart deployment/profile-service
kubectl rollout restart deployment/notification-service

kubectl get deployments -o wide
kubectl get pods -l app=explore-deploy-app
