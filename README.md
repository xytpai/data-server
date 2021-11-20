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
