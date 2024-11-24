## Docker Hub Repository
En docker funciona con hacer docker compose up --build

--Para construir la imagen de apache desde app
docker build -t aitorgonzalo/movie_catalog_web:latest .

--la de generate movies
docker build -t generate-movies:local -f generate_movies_kuber/Dockerfile .


Para cargar datos en kubernetes
cd carpeta kubernetes

minikube start 

kubectl delete deployment --all

kubectl apply -f .

kubectl get pods

kubectl cp ../db/data.csv mysql-pod:/var/lib/mysql-files/data.csv

kubectl exec -it mysql-pod  -- mysql -u root -p --local-infile=1

SET GLOBAL local_infile = 1;(en principio deberia estar activado)

SOURCE /docker-entrypoint-initdb.d/db_init.sql;




Para probar el helthcheack

kubectl exec -it apache-web-<id> -- /bin/sh


service apache2 stop

kubectl get pods
 vemos como se ha restablecido el pod
 y si vemos los logs del contenedor vemos
 Apache Reiniciado Correctamente: El servidor Apache se reinició y volvió a operar en modo normal después del fallo simulado. Esto se refleja en los mensajes:

 [Sat Nov 23 18:37:36.014780 2024] [mpm_prefork:notice] [pid 1:tid 1] AH00163: Apache/2.4.62 (Debian) PHP/8.1.31 configured -- resuming normal operations
[Sat Nov 23 18:37:36.014831 2024] [core:notice] [pid 1:tid 1] AH00094: Command line: 'apache2 -D FOREGROUND'

Healthcheck de Kubernetes Activo: Las líneas que indican solicitudes GET / HTTP/1.1 realizadas por kube-probe/1.31 confirman que Kubernetes está ejecutando tanto el livenessProbe como el readinessProbe

10.244.0.1 - - [23/Nov/2024:18:38:06 +0000] "GET / HTTP/1.1" 200 14037 "-" "kube-probe/1.31"


"Este proceso muestra que el liveness probe está funcionando como se espera: detecta cuando el servicio Apache falla, reinicia el contenedor de manera automática y asegura la recuperación del sistema sin intervención manual.

La sonda de readiness HTTP se utiliza para garantizar que el servidor Apache esté funcionando correctamente y pueda servir solicitudes antes de recibir tráfico. Este enfoque es eficiente porque verifica directamente si Apache está listo sin introducir la complejidad de comprobar otras dependencias internas, lo que minimiza falsos positivos y asegura la disponibilidad del servicio. Además, al verificar simplemente si la página principal (/) responde, Kubernetes puede remover automáticamente el pod del balanceador si algo falla, asegurando la resiliencia y disponibilidad del sistema. En resumen, esta verificación HTTP es una práctica común y efectiva para validar la capacidad del servidor web para manejar solicitudes entrantes.