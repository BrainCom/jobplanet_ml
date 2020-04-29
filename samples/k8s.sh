#Context
kubectl config get-contexts                          # 컨텍스트 리스트 출력
kubectl config current-context              # 현재 컨텍스트 출력
kubectl config use-context gke_banded-totality-247701_asia-northeast3-a_job-recommender


#ssh
kubectl exec -it django-595cdff5db-rglss -c django /bin/bash
kubectl exec -it django-595cdff5db-rglss -c django python manage.py createsuperuser

#autoscale
kubectl autoscale deployment django --cpu-percent=50 --min=1 --max=10
kubectl autoscale deployment celery-worker --cpu-percent=50 --min=1 --max=10
kubectl autoscale statefulset redis --cpu-percent=50 --min=1 --max=10

#minikube
minikube service django
minikube service celery-flower

#cert
kubectl describe managedcertificate


#port forward
kubectl port-forward
kubectl port-forward django-68f49478b6-jt2zx 5000:5000
