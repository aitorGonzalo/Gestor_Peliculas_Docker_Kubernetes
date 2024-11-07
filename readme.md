## Docker Hub Repository

Para la cargar de la base de datos en docker
Entramos a mysql

docker exec -it mysql_db mysql -u aitor -p --local-infile=1

 y desde mysql ejecutamos
 SOURCE /var/lib/mysql-files/db_init.sql;

--Para construir la imagen de apache
desde el directorio principal-> docker build -f apache/Dockerfile -t aitorgonzalo/apache-web:latest .


Para cargar datos en kubernetes
kubectl get pods
kubectl exec -it (pod-mysql) -- mysql -u root -p --local-infile=1
SET GLOBAL local_infile = 1;
SOURCE /docker-entrypoint-initdb.d/db_init.sql;





