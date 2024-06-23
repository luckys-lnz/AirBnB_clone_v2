-- Script configures MySQL server test environment

-- Creates database, if not exists
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create user, if not exists
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on hbnb_test_db to user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant select privilege on performance_schema to user
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
