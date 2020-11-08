<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Calescador Web</title>

        <!-- Icons -->
        <link rel="shortcut-icon" href="favicon.ico">
        <link rel="apple-touch-icon" href="apple-touch-icon.png">

        <!-- Fonts -->
        <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">

        <!-- Styles -->
        <link href="{{ asset('css/welcome.css') }}" rel="stylesheet">

        <style>
            body {
                font-family: 'Nunito';
            }
        </style>
    </head>
    <body class="antialiased">
        <div class="link-bar">
            <div class="splash">
                <div class="padded-column">
                    <img src="{{ asset('images/icon.svg') }}" class="logo">
                </div>
                <div class="padded-column content">
                    <div class="link-bar">
                        @auth
                            <a href="{{ url('/home') }}">Home</a>
                        @else
                            <a href="{{ route('login') }}">Login</a>

                            @if (Route::has('register'))
                                <a href="{{ route('register') }}">Register</a>
                            @endif
                        @endif
                    </div>

                    <h1>Calescador</h1>
                    <p>A collaborative calendaring and scheduling system.</p>
                </div>
            </div>
        </div>
    </body>
</html>
