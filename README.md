# 使用python实现简单的测试工具

1. [使用命令行发送get请求并打印返回](https://github.com/easonhan007/simple_test_tools/blob/master/get.py)
2. [简单的ui测试工具](https://github.com/easonhan007/simple_test_tools/blob/master/html_assertion.py)
3. [检查页面是否有无效链接的工具](https://github.com/easonhan007/simple_test_tools/blob/master/dead_link.py)
4. [unittest动态定义用例运行](https://github.com/easonhan007/simple_test_tools/blob/master/ut.py)
4. [简单的动态配置mock server](https://github.com/easonhan007/simple_test_tools/blob/master/mock.py)


------------

### API

simple_server 

* GET /ping
* GET /user

jwt_server

```
# login
http -v --json POST localhost:8000/login username=admin password=admin

# refresh token
http -v -f GET localhost:8000/auth/refresh_token "Authorization:Bearer xxxxxxxxx"  "Content-Type: application/json"

# login success
http -f GET localhost:8000/auth/hello "Authorization:Bearer xxxxxxxxx"  "Content-Type: application/json"

# login success but authorization failed 
http -f GET localhost:8000/auth/hello "Authorization:Bearer xxxxxxxxx"  "Content-Type: application/json"
```