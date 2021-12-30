### 1. Install MySQL

```bash
sudo apt-get install mysql-server mysql-client
sudo snap install mysql-workbench-community
sudo snap connect mysql-workbench-community:password-manager-service :password-manager-service
# for check
sudo netstat -tap | grep mysql
# get pwd
sudo cat /etc/mysql/debian.cnf
```

### 2. OpenSSL

```bash
cd openssl
# create ca
openssl genrsa -des3 -out ca.key 2048
openssl req -new -x509 -key ca.key -out ca.crt -days 3650
# create server
openssl genrsa -des3 -out server.key 2048
openssl req -new -days 3650 -key server.key -out server.csr -config openssl.cnf
# self signature
openssl x509 -req -sha256 -days 3650 -extfile domain.ext -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
```
