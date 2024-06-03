FROM php:7.4-apache

RUN apt update -y && apt install -y libjpeg-dev libpng-dev zlib1g-dev python3 python3-pip libfreetype6-dev libfontconfig1
RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-install gd
RUN python3 -m pip install pytesseract tesseract

COPY src/template /var/www/html