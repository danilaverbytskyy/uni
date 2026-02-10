# User Platform (Flask + PostgreSQL)

## Local run (Docker Compose)
```bash
cp .env.example .env
docker compose up --build
```
Open: http://localhost:5000/

Health:
- /health/live
- /health/ready

## Kubernetes
1) Build and push image, then set it in `k8s/30-web-deployment.yaml` as `image: ...`
2) Apply:
```bash
kubectl apply -f k8s/
kubectl -n user-platform-exam get pods,svc
```
NodePort: http://<NODE_IP>:30080/
