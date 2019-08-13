docker build -t itest/main.app -f Dockerfile .
docker build -t itest/mysql.app -f Dockerfile.mysql .
docker build -t itest/dataservice.app -f Dockerfile.dataservice .
