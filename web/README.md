# Calescador Web
The backend together with web, REST and calendar interfaces.

## Development

### Setup
* Set up the database:
    * Make sure to have MySQL installed and running, e.g. using `apt install mysql-server`
    * Copy `.env.example` to `.env` (if not already done)
    * Open the MySQL shell using `mysql` and make sure the user specified in your `.env` file exists. To create the sample user from `.env.example`, enter the following commands:
        * `create user 'laravel'@'localhost' identified by 'laravel';`
        * `grant all privileges on laravel.* to 'laravel'@'localhost';`
        * `create database laravel;`
* Set up the Laravel project:
    * Make sure to have a recent version of PHP and Composer installed, e.g. using `apt install php php-mbstring php-dom php-mysql`
    * Run `composer install` to install the dependencies
    * Run `php artisan key:generate` to generate an application-specific key (locally).
    * Run `php artisan migrate` to create the database tables

### Running
To run the development server, run

`php artisan serve`

This will serve the application on `http://localhost:8000`.
