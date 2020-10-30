<?php

use App\Http\Controllers\AttendanceController;
use App\Http\Controllers\EventController;
use App\Http\Controllers\UserController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use Carbon\Carbon;

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

// TODO: Require authentication on all routes

// Route::middleware('auth:api')->get('/user', function (Request $request) {

/** Fetches a list of all users. */
Route::get('/users', [UserController::class, 'all']);

/** Fetches a user by ID. */
Route::get('/users/{id}', [UserController::class, 'find']);

/** Fetches a user by Discord user ID. */
Route::get('/users/discord/{id}', [UserController::class, 'findByDiscord']);

/** Creates a new user. */
Route::post('/users', [UserController::class, 'create']);

/** Deletes a user. */
Route::delete('/users/{id}', [UserController::class, 'delete']);

/** Fetch all calendar events. */
Route::get('/events', [EventController::class, 'all']);

/** Fetch upcoming calendar events. */
Route::get('/events/upcoming', [EventController::class, 'upcoming']);

/** Fetch an event by id. */
Route::get('/events/{id}', [EventController::class, 'find']);

/** Fetch events by Discord message id. */
Route::get('/events/discord/{id}', [EventController::class, 'findByDiscord']);

/** Create a new calendar event. */
Route::post('/events', [EventController::class, 'create']);

/** Delete an existing calendar event. */
Route::delete('/events/{id}', [EventController::class, 'delete']);

/** Creates a new attendance. */
Route::put('/attendances/{user_id}/{event_id}', [AttendanceController::class, 'create']);

/** Fetches attendances. */
Route::get('/attendances', [AttendanceController::class, 'all']);

/** Fetches attendances of a user. */
Route::get('/attendances/{user_id}', [AttendanceController::class, 'findByUser']);

/** Fetches a single attendance. */
Route::get('/attendances/{user_id}/{event_id}', [AttendanceController::class, 'find']);

/** Deletes an attendance. */
Route::delete('/attendances/{user_id}/{event_id}', [AttendanceController::class, 'delete']);
