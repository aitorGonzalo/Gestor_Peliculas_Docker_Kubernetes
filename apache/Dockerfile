FROM httpd:latest

# Instalar herramientas necesarias: curl, mysql-client, y killall (en procps)
RUN apt-get update && \
    apt-get install -y curl default-mysql-client procps && \
    rm -rf /var/lib/apt/lists/*

# Copiar la aplicación y el índice
COPY app/ /usr/local/apache2/htdocs/
COPY kubernetes/index-kuber.html /usr/local/apache2/htdocs/index.html

# Copiar el archivo de configuración adicional en conf.d en lugar de sobrescribir httpd.conf
COPY kubernetes/kubernetes.conf /usr/local/apache2/conf/conf.d/kubernetes.conf
