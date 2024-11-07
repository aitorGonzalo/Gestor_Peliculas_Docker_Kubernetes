FROM httpd:latest

# Copiar la aplicación y el índice
COPY app/ /usr/local/apache2/htdocs/
COPY kubernetes/index-kuber.html /usr/local/apache2/htdocs/index.html

# Copiar el archivo de configuración adicional en conf.d en lugar de sobrescribir httpd.conf
COPY kubernetes/kubernetes.conf /usr/local/apache2/conf/conf.d/kubernetes.conf
