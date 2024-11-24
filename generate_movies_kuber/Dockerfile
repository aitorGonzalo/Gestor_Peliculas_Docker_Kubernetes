
FROM php:8.1-cli


RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    libcurl4-openssl-dev \
    && docker-php-ext-install curl \
    && rm -rf /var/lib/apt/lists/*


COPY --from=composer:latest /usr/bin/composer /usr/bin/composer


WORKDIR /app


COPY app/ /app/


RUN composer require fakerphp/faker


CMD ["php", "/app/generate_movies.php"]
