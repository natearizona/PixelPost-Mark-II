FROM php:5.6-apache

RUN set -eux; \
    if grep -Eq "jessie|stretch" /etc/apt/sources.list; then \
      sed -i \
        -e 's/deb.debian.org/archive.debian.org/g' \
        -e 's/security.debian.org/archive.debian.org/g' \
        -e 's|stretch/updates|stretch|g' \
        -e 's|jessie/updates|jessie|g' \
        -e '/debian-security/d' \
        -e '/stretch-updates/d' \
        -e '/jessie-updates/d' \
        /etc/apt/sources.list; \
    fi; \
    apt-get \
      -o Acquire::Check-Valid-Until=false \
      -o Acquire::AllowInsecureRepositories=true \
      -o APT::Get::AllowUnauthenticated=true \
      update; \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
      libfreetype6-dev \
      libjpeg62-turbo-dev \
      libpng-dev; \
    docker-php-ext-configure gd \
      --with-freetype-dir=/usr/include/ \
      --with-jpeg-dir=/usr/include/; \
    docker-php-ext-install mysql mysqli gd exif; \
    a2enmod rewrite; \
    rm -rf /var/lib/apt/lists/*

COPY php.ini /usr/local/etc/php/conf.d/pixelpost-historical.ini
COPY apache-vhost.conf /etc/apache2/sites-available/000-default.conf

WORKDIR /var/www/html
