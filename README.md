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
# server
openssl genrsa -des3 -out server.key 2048
openssl req -new -key server.key -out server.csr
# ca
openssl genrsa -des3 -out ca.key 2048
openssl req -new -x509 -key ca.key -out ca.crt -days 3650
# openssl req -in server.csr -text # see all
# openssl req -in server.csr -subject -noout # see head
# openssl req -in server.csr -pubkey -noout # see pubkey
# openssl req -verify -in server.csr -noout # verify OK
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
```
 
