FROM php:8.1-apache

RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    libcurl4-openssl-dev \
    pkg-config \
    && docker-php-ext-install curl

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Establecer el directorio de trabajo
WORKDIR /var/www/html

# Copiar la aplicación PHP al contenedor
COPY . /var/www/html/

RUN composer require fakerphp/faker

# Ejecutar el script PHP automáticamente al iniciar el contenedor
CMD ["apache2ctl", "-D", "FOREGROUND"]
