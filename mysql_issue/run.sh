docker run -itd --name=mysql -p 10000:80 -m 500m itest/mysql.app
docker run -itd --name=dataservice --privileged itest/dataservice.app
docker run -itd --name=myapp --network=container:mysql itest/main.app
