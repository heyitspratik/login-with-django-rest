# login-with-django-rest

Login, Registration and OTP verification using Django REST

## create virtual environment using below command and activate the same
```
python3 -m venv venv
```
## required installations
install all the python packages mentioned in requirements.txt file

## create django project and make an app inside it
```
django-admin startproject projectname
python manage.py startapp appname
```

## Database Setup
1. install mysql server using below command:
```
sudo apt install mysql-server
```
2. after successful installation just restart it
```
sudo systemctl start mysql.service
```
3. creating a dedicated mysql user and granting privileges
```
mysql -u root -p
CREATE USER 'user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' WITH GRANT OPTION;
CREATE DATABASE databasename;
exit
```
## Database Migration
Use below command for migration of tables
```
python manage.py makemigrations
python manage.py migrate
```
## create superuser to access django admin panel
```
python manage.py createsuperuser
```
## starting development server using below command
```
python manage.py runserver
```
which will run on (http://127.0.0.1:8000/)
