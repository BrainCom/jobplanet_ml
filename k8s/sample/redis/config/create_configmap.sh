kubectl create configmap redis-config \
	--from-file=slave.conf=./slave.conf \
	--from-file=master.conf=./master.conf \
	--from-file=sentinel.conf=./sentinel.conf \
	--from-file=init.sh=./init.sh \
	--from-file=sentinel.sh=./sentinel.sh