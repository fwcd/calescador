<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:api')->get('/user', function (Request $request) {
    return $request->user();
});

// TODO: Require authentication on all routes

/** Fetch all calendar events. */
Route::get('/events', function () {
    // TODO
});

/** Create a new calendar event. */
Route::post('/events', function (Request $request) {
    // TODO
});

/** Delete an existing calendar event. */
Route::delete('/events/{id}', function ($id) {
    // TODO
});
