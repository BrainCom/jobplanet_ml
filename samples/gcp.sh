gcloud config set project banded-totality-247701
gcloud config set compute/zone asia-northeast3-a
gcloud container clusters create cluster-name --num-nodes=1
gcloud container clusters get-credentials cluster-name
gcloud container clusters get-credentials job-recommender --zone asia-northeast3-a --project banded-totality-247701
gcloud container clusters resize job-recommender --num-nodes=0 --zone=asia-northeast3
gcloud container clusters resize $CLUSTER --num-nodes=0 --zone=$ZONE

#클러스터 노드수 자동 확장 (서비스 중단의 내결함성이 없다면 적용하지 말것을 공식 추천하긴 함..)
gcloud container clusters create example-cluster \
  --zone us-central1-a \
  --node-locations us-central1-a,us-central1-b,us-central1-f \
  --num-nodes 2 --enable-autoscaling --min-nodes 1 --max-nodes 4

gcloud container clusters update job-recommender --enable-autoscaling --min-nodes 1 --max-nodes 10 --zone=asia-northeast3 --node-pool default-pool
gcloud container clusters update job-recommender --no-enable-autoscaling --zone=asia-northeast3 --node-pool default-pool



gcloud --project=banded-totality-247701 beta compute operations describe operation-1590374045818-5a66fd00f9ecb-d8f6bede-cf7f35f0
gcloud --project=banded-totality-247701 compute ssl-certificates list
gcloud beta compute operations describe operation-1590374978947-5a67007ae0846-b7ba0b9d-e0536d84
gcloud compute ssl-certificates delete


# https://cloud.google.com/sdk/gcloud/reference
# https://cheatsheet.dennyzhang.com/cheatsheet-gcp-a4
gcloud version
gcloud info
gcloud components list
gcloud compute zones list
gcloud compute instances list
gcloud compute disks list
gcloud compute disk-types list
gcloud compute snapshots list
gcloud compute images list
gcloud sql instances list


# gcp 인증
gcloud auth login
gcloud auth application-default login


# Display a list of credentialed accounts	
gcloud auth list

# Auth to GCP Container Registry
gcloud auth configure-docker




# GCR (docker이미지 저장소)
gcloud container images list

REPO=asia.gcr.io/banded-totality-247701
IMAGE=gcr.io/banded-totality-247701/kfp-util
DELETE_BEFORE=2020-05-01

gcloud container images list --repository=$REPO
gcloud container images delete
gcloud container images list-tags $IMAGE \
      --filter='-tags:*' \
      --filter="timestamp.datetime &lt; '${DELETE_BEFORE}'" \
      --format='get(digest)' \
      --limit=999999 --sort-by=TIMESTAMP
gcloud container images delete \
	asia.gcr.io/banded-totality-247701/train_ex@sha256:7dd0772ecbb014dd61a8dc66db1a2be750083a28e57bda3acff396a31e45047c --quiet


# GCS (storage)
# https://cloud.google.com/storage/docs/gsutil/commands/ls?hl=ko
gsutil ls [-a] [-b] [-d] [-l] [-L] [-r] [-p]
gsutil ls gs://jongkyunjung-test-files-us/
gsutil ls gs://bucket/*.txt



# cloud dns
gcloud dns managed-zones describe job-recommender
watch dig job-recommender.johnjung.shop @ns-cloud-c1.googledomains.com
watch dig +short NS job-recommender.johnjung.shop

gcloud iam service-accounts create dns01-solver --display-name "dns01-solver"
export PROJECT_ID=banded-totality-247701
gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member serviceAccount:dns01-solver@$PROJECT_ID.iam.gserviceaccount.com \
   --role roles/dns.admin






# shell set
# https://bash.cyberciti.biz/guide/Set_command
-e exit on first error
-u exit when an undefined variable such as $FO0 is accessed
-o pipefail:
 exit when | any |cmd | in | a | pipe has exitcode != 0, that is a bit excessive, no?
-x print all commands - that is mostly for debug