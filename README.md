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

### 2. CA

```bash
openssl genrsa -out privkey.pem 2048 # gen privkey
openssl req -new -key privkey.pem -out req.csr
openssl req -in req.csr -text # see all
openssl req -in req.csr -subject -noout # see head
openssl req -in req.csr -pubkey -noout # see pubkey
openssl req -verify -in req.csr -noout # verify OK
openssl req -x509 -key privkey.pem -in req.csr -out ca.crt -days 3650
```

