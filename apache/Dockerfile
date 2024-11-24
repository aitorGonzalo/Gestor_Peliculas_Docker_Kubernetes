FROM php:8.1-apache


RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    libcurl4-openssl-dev \
    procps \
    psmisc \ 
    && docker-php-ext-install curl \
    && rm -rf /var/lib/apt/lists/*


COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

RUN a2enmod rewrite

# Copiar la aplicación y los archivos adicionales
COPY app/ /var/www/html/
COPY kubernetes/index-kuber.html /var/www/html/index.html
COPY kubernetes/kubernetes.conf /etc/apache2/conf-available/kubernetes.conf


RUN a2enconf kubernetes


WORKDIR /var/www/html


RUN composer require fakerphp/faker


EXPOSE 80


CMD ["apache2-foreground"]
