#Build docker image and push to GCR
docker build -t job_recommender .
docker tag job_recommender gcr.io/banded-totality-247701/job_recommender:latest
docker push gcr.io/banded-totality-247701/job_recommender:latest

# kustomize build mysql/overlays/dev > dev-mysql.yaml
# kubectl apply -f dev-mysql.yaml

#Dev Env
#Build
kustomize build django/overlays/dev > dev-django.yaml
kustomize build celery/overlays/dev > dev-celery.yaml
kustomize build redis/overlays/dev > dev-redis.yaml
kustomize build sentinel/overlays/dev > dev-sentinel.yaml
kustomize build ingress/overlays/dev > dev-ingress.yaml
#Deploy
kubectl apply -f dev-sentinel.yaml
kubectl apply -f dev-redis.yaml
kubectl apply -f dev-django.yaml
kubectl apply -f dev-celery.yaml
kubectl apply -f dev-ingress.yaml
kubectl apply -f priority_classes.yaml




#Prod Env
kustomize build django/overlays/prod > prod-django.yaml
kustomize build celery/overlays/prod > prod-celery.yaml
kustomize build redis/overlays/prod > prod-redis.yaml
kustomize build sentinel/overlays/prod > prod-sentinel.yaml
kustomize build ingress/overlays/prod > prod-ingress.yaml
#Deploy
kubectl apply -f prod-sentinel.yaml
kubectl apply -f prod-redis.yaml
kubectl apply -f prod-django.yaml
kubectl apply -f prod-celery.yaml
kubectl apply -f prod-ingress.yaml
kubectl apply -f priority_classes.yaml

#cert manager
#Kubernetes 1.15+
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.15.1/cert-manager.yaml

#ingress-nginx
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-0.32.0/deploy/static/provider/cloud/deploy.yaml

# helm install stable/cert-manager --namespace kube-system -generate-name
# kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.6/deploy/manifests/00-crds.yaml