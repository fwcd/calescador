# Calescador Web
The backend together with web, REST and calendar interfaces.

## Development

### Setup
* First make sure to have a recent version of PHP and Composer installed, e.g. using `apt install php php-mbstring php-dom`
* Then run `composer install` to install the dependencies
* Run `php artisan key:generate` to generate an application-specific key (locally).

### Running
To run the development server, run

`php artisan serve`

This will serve the application on `http://localhost:8000`.
