create user 'XX'@'%'
  identified by '*';

CREATE DATABASE `happyenglish`
  CHARACTER SET 'utf8'
  COLLATE 'utf8_general_ci';

GRANT ALL PRIVILEGES ON happyenglish.* to 'XX'@'%'
with grant option;

flush PRIVILEGES;