

GRANT SELECT,INSERT,UPDATE,DELETE,EXECUTE ON hdbpp.* TO 'hdbpprw'@'%' IDENTIFIED BY 'hdbpprw_password';
GRANT SELECT ON hdbpp.* TO 'hdbppro'@'%' IDENTIFIED BY 'hdbppro_password';
FLUSH PRIVILEGES;
