#사전 설정
#step1: 필요 service enable
gcloud services enable sqladmin

#step2: cloud_sql_proxy 다운(local에서 k8s 배포 사용시 필요)
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
chmod +x cloud_sql_proxy

#step3: cloud_sql 인스턴스 생성(or gcp console에서 생성)
gcloud sql instances create job-recommender \
	--database-version=POSTGRES_11 \
    --cpu=2 \
	--memory=7680MiB \
    --region="asia-northeast3" \
	--gce-zone="asia-northeast3-a"] \
	--zone="asia-northeast3-a"
gcloud sql instances describe job-recommender

#step4: cloud_sql_proxy와 cloud_sql 인스턴스 연결 / postgres관련 설정
./cloud_sql_proxy -instances="banded-totality-247701:asia-northeast3:job-recommender1"=tcp:5432
psql --host 127.0.0.1 --user postgres --password postgres
CREATE DATABASE job_recommender;
CREATE USER test WITH PASSWORD 'test';
GRANT ALL PRIVILEGES ON DATABASE job_recommender TO 'test';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO 'test';





#인스턴스 중지/재시작
gcloud sql instances patch job-recommender1 --activation-policy NEVER
gcloud sql instances patch job-recommender1 --activation-policy ALWAYS
gcloud sql instances restart job-recommender1



#고정 ip생성
gcloud compute addresses create job-recommender --global
gcloud compute addresses describe job-recommender --global

#인증서
gcloud beta compute ssl-certificates create job_recommender_cert \
    --description="ml service" \
    --domains="tospic.com" \
    --global
