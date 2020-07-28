ver = 2.8
build:
	docker build -t apitestplatform .
run:
	docker run -d --name apitestplatform -p 8000:8000 registry.cn-shenzhen.aliyuncs.com/zp-repository/apitestpltform:2.8 /bin/bash -c "sh /data/apitestplatform/start.sh && while true; do echo hello world; sleep 1; done"
tag:
	docker tag apitestplatform registry.cn-shenzhen.aliyuncs.com/zp-repository/apitestpltform:$(ver)
push:
	docker push registry.cn-shenzhen.aliyuncs.com/zp-repository/apitestpltform:$(ver)