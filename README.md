# k8s를 이용한 django 추천 서비스 배포

k8s는 기술된 yaml 파일 정보에 따라 자동으로 인프라를 손쉽게 배포/관리할 수 있다는 장점이 있지만, 정확한 명세 기술에 실패하면 문제의 원인을 찾기가 매우 어려울 수도 있습니다. 주의하여 사용바랍니다.

## INGRESS / SERVICE
service/ingress | App | Purpose | Internal IP | External IP | etc
---- | ---- | ---- | ---- | ---- | ----
ingress | | ingress 통해 모든 외부 요청 처리.<br/>https 연결 후, 클러스터 내부는 http | O | O |
service | django | 메인 서비스 | O | X |
service | celery-flower | worker 관리 gui | O | X |
service | mysql | 잡플래닛 db 연결 서비스<br/>(하나의 hostname 혹은 고정 ip 가리키도록 설정 할 수 있음) | O | X |
service(headless) | redis | Django의 redis cache 세팅이 가리키는 곳 | X | X | redis-0 호스트가 master
service | redis-read | Django의 redis cache 세팅이 가리키는 곳 | O | X |
service(headless) | sentinel | Django의 broker세팅이 가리키는 곳 | X | X | sentinel-0 호스트가 master

*참고 이미지
kubectl get ingress | kubectl get service
---- | ----
![image](https://user-images.githubusercontent.com/16386947/119599343-c72fe300-be1f-11eb-9730-a26be8eba99b.png) | ![image](https://user-images.githubusercontent.com/16386947/119599356-cc8d2d80-be1f-11eb-83dc-1df81c055e0c.png)


## POD
deploy/statefulset | App | Purpose | initial replica | rails 앱에 비유시, 대응 요소 | autoscale
---- | ---- | ---- | ---- | ---- | ----
deployment | Django | 메인 앱 | 3 | rails | O
deployment | Celery Worker<br/>Celery Beat<br/>Celery Flower | worker<br/>scheduled worker<br/>worker 관리 뷰 | 1<br/>1<br/>1 | sidekiq | O
statefulset | Redis | worker broker<br/>cache | 3 | redis | O
statefulset | Sentinel | redis sentinel<br/>cluster failover | 3 | | X<br/>(pod 3개로 고정해둘 생각)

### [GCP cloudsql](https://cloud.google.com/sql/docs/postgres/sql-proxy?hl=ko)
- DB는 POSTGRES 사용
- 그러나, kubernetes로 메뉴얼로 구성하지 않고, GCP cloudsql 기능 사용(관리 용이할 것으로 판단)
- Django/Celery pod에서 cloudsql proxy를 통해 연결

## GCP 화면

### 작업부하: POD (Deployment/Statefulset)
![image](https://user-images.githubusercontent.com/16386947/119599431-f47c9100-be1f-11eb-9946-f7f5fec1647c.png)

### 서비스: Service/Ingress
![image](https://user-images.githubusercontent.com/16386947/119599445-fb0b0880-be1f-11eb-9f23-8a61ff6b1499.png)

### 구성: Config Map / Secret
![image](https://user-images.githubusercontent.com/16386947/119599459-00685300-be20-11eb-8bb9-a73a222fe822.png)
```
관리의 용이성을 고려해 크게 아래와 같이 3 타입으로 구성했음

1. GCP credentials: cloudsql-credentials, storage-credentials 등 용도로 따라 service account 분리
2. prefix-config (ex: django-config, redid-config) : init script나 서버 세팅 파일 등
3. Django/Celery 관련 모든 param 및 secret:
 - deployment-params: 일반 param (ex: debug=true)
 - deployment-secrets: 민감한 param (ex: db user, db password)
```

### Cloudsql
![image](https://user-images.githubusercontent.com/16386947/119599470-05c59d80-be20-11eb-88cd-475dd1b35cd0.png)

### [Monitoring](https://console.cloud.google.com/monitoring/dashboards/resourceList/kubernetes)
![image](https://user-images.githubusercontent.com/16386947/119599482-0c541500-be20-11eb-84bd-ac896f3e7f5e.png)
![image](https://user-images.githubusercontent.com/16386947/119599489-0e1dd880-be20-11eb-825f-6ddfdac91b24.png)

## 코드 작성 / 관리
*kustomize tool 사용시

### STEP1: kustomize build로 앱 별로 하나의 yaml파일로 통합
```
kustomize build django/overlays/dev > dev-django.yaml
kustomize build celery/overlays/dev > dev-celery.yaml
kustomize build mysql/overlays/dev > dev-mysql.yaml
kustomize build redis/overlays/dev > dev-redis.yaml
kustomize build sentinel/overlays/dev > dev-sentinel.yaml
```

### STEP2: 각 yaml파일들 일괄 배포
```
kubectl apply -f dev-sentinel.yaml
kubectl apply -f dev-redis.yaml
kubectl apply -f dev-mysql.yaml
kubectl apply -f dev-django.yaml
kubectl apply -f dev-celery.yaml
kubectl apply -f ingress.yaml
kubectl apply -f managed_certificate.yaml
kubectl apply -f priority_classes.yaml
```
*코드 구조
참고: 이미지의 postgres는 작성만 해두었고 실제로는 쓰지 않고 있음(대신 cloudsql  사용)

## 배포관리는 어떻게 하나
research 결과 2020년초 기준, k8s 배포에 주로 사용되는 방식은 Helm, Spinnaker 등이 있는데,
모두 별도 복잡한 구성이 필요하고 체계적인 배포 시스템 및 전담 인력이 설정되지 않으면 실제 운용에 무리가 있음.
따라서, 여기선 k8s 기본 kubectl 명령어를 이용하여 yaml파일을 직접 제출하는 형태로 배포

### 최초 클러스터 세팅: 모든 리소스 배포
```
kubectl apply -f dev-sentinel.yaml
kubectl apply -f dev-redis.yaml
kubectl apply -f dev-mysql.yaml
kubectl apply -f dev-django.yaml
kubectl apply -f dev-celery.yaml
kubectl apply -f ingress.yaml
kubectl apply -f managed_certificate.yaml
kubectl apply -f priority_classes.yaml
```

### 재배포: django, celery만 재배포
```
kubectl apply -f dev-django.yaml
kubectl apply -f dev-celery.yaml
```

### 배포 상태 확인 / 롤백
```
확인: kubectl rollout status deploy/django
내역: kubectl rollout history deploy/django
롤백: kubectl rollout undo deploy/django
롤백 to 특정 revision: kubectl rollout undo deploy/django --to-revision=2
배포 중지: kubectl rollout pause deploy/django
배포 재개: kubectl rollout resume deploy/django
```
