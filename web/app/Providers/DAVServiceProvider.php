<?php

// Based on sample code from https://github.com/monicahq/laravel-sabre

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use LaravelSabre\LaravelSabre;
use LaravelSabre\Http\Auth\AuthBackend;
use Sabre\DAV\Auth\Plugin as AuthPlugin;
use Sabre\CalDAV\Plugin as CalDAVPlugin;

class DAVServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        LaravelSabre::plugins(function () {
            return $this->plugins();
        });
    }

    /**
     * List of Sabre plugins.
     */
    private function plugins()
    {
        // Authentication backend
        $authBackend = new AuthBackend();
        yield new AuthPlugin($authBackend);

        // CalDAV plugin
        yield new CalDAVPlugin();
    }
}
