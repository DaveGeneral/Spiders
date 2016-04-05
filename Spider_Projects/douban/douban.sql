--  Preparation before running the python code

--  Use root permission to enter mysql
mysql -uroot -p

-- Create new user 'spider' with password 'pwd123456'
CREATE USER 'spider'@'localhost' IDENTIFIED BY 'pwd123456';

--  Grant all privileges to the new user
GRANT ALL PRIVILEGES ON * . * TO 'spider'@'localhost';

--  Reload all privileges and change will be in effect
FLUSH PRIVILEGES;

--  Exit root user and enter with new user and password
mysql -uspider -p

-- Create new database 'Movie' for use latter
CREATE DATABASE Movie
