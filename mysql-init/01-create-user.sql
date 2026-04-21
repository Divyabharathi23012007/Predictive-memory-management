-- Create user and grant permissions
CREATE USER IF NOT EXISTS 'memoria_user'@'%' IDENTIFIED BY 'memoria_pass';
GRANT ALL PRIVILEGES ON memoria_db.* TO 'memoria_user'@'%';
FLUSH PRIVILEGES;
